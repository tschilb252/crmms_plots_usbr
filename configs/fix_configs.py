# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:11:35 2021

@author: buriona
"""

import sys
from pathlib import Path
import json
from calendar import month_name

DEFAULT_DT_FRMT = "%m-%d-%Y %H:%M:%S"

this_dir = Path().absolute()

for config in this_dir.glob("*.config"):
    if "models.config" in config.name or "viz.config" in config.name:
        continue

    with config.open("r") as j:
        config_dict = json.load(j)

    new_config = {}
    for k, v in config_dict.items():
        k_arr = k.split("_")
        year = k_arr[-1][2:]
        month_num = int(k_arr[0])
        month = month_name[month_num][:3].lower()
        data = f"ESPcsvOutput_{month}{year}.csv"
        mrids = v["mrids"]
        name = v["name"]
        new_config[k] = {"name": name, "mrids": mrids, "data": data}

    with config.open("w") as j:
        json.dump(new_config, j, indent=2, sort_keys=True)
