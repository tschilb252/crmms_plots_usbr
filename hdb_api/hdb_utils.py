# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 13:16:02 2019

@author: buriona
"""

import json
from os import path
import sqlalchemy as sql

def get_eng_config(file_name='hdb_config.json', db='uc'):
    this_dir = path.dirname(path.realpath(__file__))
    file_path = path.join(this_dir, file_name)
    with open(file_path, 'r') as read_file:
        return json.load(read_file)[db]

def get_hdb_config(file_name='.app_login'):
    this_dir = path.dirname(path.realpath(__file__))
    file_path = path.join(this_dir, file_name)
    with open(file_path, 'r') as read_file:
         json.load(read_file)
         
    return #dict of config using first three lines from a app_login file
    
def create_hdb_engine(**k):
    eng_str = (
        f"{k['dialect']}+{k['driver']}://"
        f"{k['username']}:{k['psswrd']}@"
        f"{k['host']}:{k['port']}/{k['database']}"
    )

    engine = sql.create_engine(
        eng_str,
        convert_unicode=True,
        encoding="utf-8"
    )

    return engine

def get_hdb_eng():
    config_dict = get_eng_config()
    return create_hdb_engine(**config_dict)

def get_wy(cal_dt):
    if cal_dt.month > 9:
        return cal_dt.year + 1
    return int(cal_dt.year)

def get_cal_yr(month, wy):
    if month > 9:
        return wy - 1
    return int(wy)

def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

datatype_labels = {
    17: 'STORAGE',
    49: 'POOL ELEVATION',
    30: 'INFLOW VOLUME',
    29: 'INFLOW',
    43: 'TOTAL RELEASE VOLUME',
    42: 'TOTAL RELEASE',
    34: 'UNREGULATED INFLOW VOLUME',
    33: 'UNREGULATED INFLOW',
    1198: 'BYPASS RELEASE VOLUME',
    1197: 'BYPASS RELEASE',
    40: 'POWER RELEASE VOLUME',
    39: 'POWER RELEASE',
    46: 'SPILLWAY RELEASE',
    25: 'EVAPORTAION',
    15: 'BANK STORAGE',
    123: 'MOD UNREGULATED INFLOW',
    124: 'MOD UNREGULATED INFLOW VOLUME',
    20: 'FLOW VOLUME',
    19: 'FLOW',
    47: 'DELTA STORAGE',
    1501: 'AVG SJC INFLOW VOL',
    66: 'GAGE HEIGHT',
    89: 'AREA',
    1158: 'AVE SJC RELEASE',
    2356: 'ACCURAL',
    2742: 'AVE RG RELEASE'
}

datatype_labels_strs = {}
for k, v in datatype_labels.items():
    if str(k).isnumeric():
        datatype_labels_strs[str(k)] = v
datatype_labels.update(datatype_labels_strs)  

datatype_ids = {v: k for k, v in datatype_labels.items()}

datatype_units = {
    19: 'cfs',
    20: 'acre-ft',
    17: 'acre-ft',
    49: 'ft',
    30: 'acre-ft',
    29: 'cfs',
    43: 'acre-ft',
    42: 'cfs',
    34: 'acre-ft',
    33: 'cfs',
    1198: 'acre-ft',
    1197: 'cfs',
    40: 'acre-ft',
    39: 'cfs',
    46: 'cfs',
    25: 'acre-ft',
    15: 'acre-ft',
    123: 'cfs',
    124: 'acre-ft',
    47: 'acre-ft',
    1501: 'acre-ft',
    50: 'inches',
    2: '% avg.',
    66: 'ft',
    89: 'sq. ft.',
    1158: 'cfs',
    2356: 'acre-ft',
    2742: 'cfs'
}

datatype_units_strs = {}
for k, v in datatype_units.items():
    if str(k).isnumeric():
        datatype_units_strs[str(k)] = v
datatype_units.update(datatype_units_strs)    

datatype_common_names = {
    19: 'flow',
    20: 'flow volume',
    17: 'storage',
    49: 'pool elevation',
    30: 'inflow volume',
    29: 'inflow',
    43: 'release volume',
    42: 'total release',
    34: 'unregulated inflow volume',
    33: 'unregulated inflow',
    1198: 'bypass release volume',
    1197: 'bypass release',
    40: 'power release volume',
    39: 'power release',
    46: 'spillway release',
    25: 'evaporation',
    15: 'bank storage',
    123: 'mod unregulated inflow',
    124: 'mod unregulated inflow volume',
    47: 'delta storage',
    1501: 'ave SJC inflow volume',
    2: 'swe',
    50: 'swe',
    66: 'gage height',
    89: 'area',
    1158: 'ave SJC release',
    2356: 'accural',
    2742: 'ave RG release'
}

datatype_common_names_strs = {}
for k, v in datatype_common_names.items():
    if str(k).isnumeric():
        datatype_common_names_strs[str(k)] = v
datatype_common_names.update(datatype_common_names_strs)
        
data_sources = {
    7: 'Bureau of Reclamation',
    8: 'National Weather Service',
    1: 'Bureau of Reclamation',
    6: 'U.S. Geological Survey',
    9: 'Bureau of Reclamation',
    12: 'Western Area Power Administration',
    3: 'Bureau of Reclamation',
    4: 'Bureau of Reclamation',
    11: 'U.S. Geological Survey',
    5: 'Bureau of Reclamation',
    10: 'Bureau of Reclamation',
    2: 'Natural Resources Conservation Service',
    13: 'Army Corps of Engineers',
    14: 'El Paso Quality Assured Data'
}

data_sources_strs = {}
for k, v in data_sources.items():
    if str(k).isnumeric():
        data_sources_strs[str(k)] = v
data_sources.update(data_sources_strs)
        
if __name__ == '__main__':
    print("This is a utility module, it doesn't do anything")
