# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:33:39 2021

@author: buriona
"""

from pathlib import Path
from datetime import datetime as dt
import pandas as pd
import numpy as np

this_dir = Path().absolute()
DEFAULT_DATA_DIR = Path(this_dir)
DEFAULT_DT_FRMT = '%m-%d-%Y %H:%M:%S'


def get_args():

    cli_desc = 'Filters ESP results by date, defaulting to only current calendar year'
    parser = argparse.ArgumentParser(description=cli_desc)
    parser.add_argument(
        "-V", "--version", help="show program version", action="store_true"
    )
    parser.add_argument(
        "-d", "--dir",
        help="directory to filter files in",
        default=DEFAULT_DATA_DIR
    )
    parser.add_argument(
        "-f", "--file",
        help="name of file to filter, otherwise filter all .csv in --dir by default",
        default='all'
    )
    parser.add_argument(
        "-e", "--end_date",
        help="end date to filter to, by default current calendar year (YYYY-MM-DD)",
        default=f'{dt(dt.now().year + 1, 1, 1):%Y-%m-%d}'
    )
    return parser.parse_args()


if __name__ == '__main__':

    import sys
    import argparse

    args = get_args()

    if args.version:
        print('filter_dates.py v1.0')

    if Path(args.dir).is_dir():
        csv_dir = Path(args.dir)
    else:
        print(f'The directory provided ({args.dir}) is not valid, try again...')
        sys.exit(1)

    try:
        end_date = dt.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        print(f'The end_date provided ({args.end_date}) does not match the format YYYY-MM-DD, please try again...')
        sys.exit(1)

    if args.file == 'all':
        glob_pattern = '*.csv'
    else:
        filepath = Path(csv_dir, args.file)
        if filepath.is_file():
            glob_pattern = args.file
        else:
            print(f'The filename/path provided ({filepath}) is not valid, try again...')
            sys.exit(1)

    for csv_path in csv_dir.glob(glob_pattern):
        if 'dummy_ESP_data' in csv_path.as_posix():
            continue
        print(f'Filtering {csv_path}...')
        df = pd.read_csv(
            csv_path,
            parse_dates=['Timestep'],
            infer_datetime_format=True,
        )
        org_lines = len(df.index)
        df.loc[df['Timestep'] > end_date, 'Slot Value'] = np.nan
        df.to_csv(
            csv_path,
            index=False,
            date_format=DEFAULT_DT_FRMT
        )
        print(
            f'  Replaced values after {end_date:%Y-%m} with nan\n'
        )