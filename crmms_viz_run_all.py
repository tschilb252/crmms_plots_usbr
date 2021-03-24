# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:28:52 2020

@author: buriona
"""

import os
import json
import subprocess
from subprocess import PIPE
from os import path

THIS_DIR = path.dirname(path.realpath(__file__))
CONFIG_FILENAME = 'crmms_viz.config'
CONFIG_FILEPATH = path.join(THIS_DIR, CONFIG_FILENAME)
if os.name == 'nt':
    BAT_FILEPATH = path.join(THIS_DIR, 'crmms_viz_gen.bat')
else:
    BAT_FILEPATH = path.join(THIS_DIR, 'crmms_viz_gen.sh')
VENV_LOC = path.join(path.dirname(THIS_DIR), 'crmm_py')

if __name__ == '__main__':
    
    import sys
    import argparse
    
    cli_desc = 'Creates visualization suite for all CRMM results in config file'
    parser = argparse.ArgumentParser(description=cli_desc)
    parser.add_argument(
        "-V", "--version", help="show program version", action="store_true"
    )
    parser.add_argument(
        "-e", "--env", help="path to conda venv to be used", default=VENV_LOC
    )
    parser.add_argument(
        "-c", "--config", help="path to config file to be used", default=CONFIG_FILEPATH
    )
    parser.add_argument(
        "-b", "--bat", help="path to crmms_viz_gen.bat", default=BAT_FILEPATH
    )
    parser.add_argument(
        "-o", "--output", help="override default output folder", default='local'
    )
    args = parser.parse_args()
    
    if args.version:
        print('crmms_viz_gen.py v1.0')
        
    if not path.isfile(args.config):
        print(f'Config file "{args.config}" does not exist, try again.')
        sys.exit(1)
    if not path.isfile(args.bat):
        print(f'Bat file "{args.bat}" does not exist, try again.')
        sys.exit(1)
    if not args.output == 'local':
        if not path.isdir(args.output):
            print(f'Output dir "{args.output}" does not exist, try again.')
            sys.exit(1)
        
    print(
        'Refreshing all CRMM viz suites using config file found here: '
        f'{args.config}'
    )
    with open(args.config, 'r') as configs:
        all_configs = json.load(configs)
    config_names = list(set(all_configs.keys()))
    print(f' Found {len(config_names)} publication months...\n')
    results_summary = []
    for config_name in config_names:
        print(f'    Working on {config_name}...')
        run_args = [args.bat, args.env, config_name, args.output, args.config]
        result = subprocess.run(
            run_args, 
            stdout=PIPE, 
            stderr=PIPE,
            encoding='utf-8'
            # capture_output=True, 
            # text=True
        )
        results_summary.append(
            (config_name, 'Failed!' if result.returncode else 'Success!')
        )
        if result.returncode:
            err_out = result.stdout.split('\n')
            err_out = '\n'.join([f'        {i}' for i in err_out])
            print(f'      Failed!\n{err_out}\n      Continuing...')
        else:
            print('      Success!')
            
    results_str = '\n'.join([f'{i[0]}: {i[1]}' for i in results_summary])
    print(f'Summary:\n\n{results_str}')