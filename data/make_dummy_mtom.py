# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 13:38:41 2021

@author: buriona
"""

from pathlib import Path
import pandas as pd
from dateutil.relativedelta import relativedelta

DEFAULT_DT_FRMT = '%m-%d-%Y %H:%M:%S'

this_dir = Path().absolute()
data_dir = Path(r'C:\Users\buriona\Desktop\data\generics')
output_dir = Path(data_dir, 'output')

year_rng = list(range(2020, 2040))

for year in year_rng:
    print(f'Working on {year}')
    for csv_path in data_dir.glob('*.csv'):
        print(f'  Working on {csv_path}')
        df = pd.read_csv(
            csv_path,
            parse_dates=['Timestep'],
            infer_datetime_format=True,
        )
        min_year = df['Timestep'].min().year
        yr_offset = min_year - year
        df['Timestep'] = df['Timestep'].apply(
            lambda x: x - relativedelta(years=yr_offset)
        )
        new_csv_name = csv_path.name.replace('YY', str(year)[2:])
        new_csv_path = Path(output_dir, new_csv_name)
        df.to_csv(
            new_csv_path,
            index=False,
            date_format=DEFAULT_DT_FRMT
        )
        print(f'    Wrote {new_csv_path}')