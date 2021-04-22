# -*- coding: utf-8 -*-
"""
Created on Thu May  2 06:33:43 2019

@author: buriona
"""

import os
from calendar import month_name
from functools import reduce
from datetime import datetime as dt
import pathlib
from pathlib import Path
import pandas as pd
from crmms_dash import create_dash
from crmms_utils import get_favicon, get_bor_seal, get_bootstrap

bor_flavicon = get_favicon()
bor_seal = get_bor_seal()
bootstrap = get_bootstrap()
bootstrap_css = bootstrap['css']
bootstrap_js = bootstrap['js']
jquery_js = bootstrap['jquery']

def get_header_str(year_str='CRMMS Modeling Results'):
    return f'''
<!DOCTYPE html>
<html>
    <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="icon" href="{bor_flavicon}">
          <link rel="stylesheet" href="{bootstrap_css}">
          <script src="{jquery_js}"></script>
          <script src="{bootstrap_js}"></script>''' + '''

    <style>
        .dropdown-submenu {
          position: relative;
        }

        .dropdown-submenu .dropdown-menu {
          top: 0;
          left: 100%;
          margin-top: -1px;
        }
    </style>
    </head>
<body>
<div class="container">
''' + f'''
<img src="{bor_seal}" style="width: 25%" class="img-responsive mx-auto d-block" alt="BOR Logo">
    <h2>{year_str}</h2>
'''

footer_str = '''

<button type="button" class="btn btn-info m-2" data-toggle="modal" data-target="#howtoModal">
  How to...
</button>
<div class="modal fade" id="howtoModal" tabindex="-1" role="dialog" aria-labelledby="howtoModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg" role="document">
    <div class="modal-content">
      <div class="modal-body mb-0 p-0">
        <div class="embed-responsive embed-responsive-16by9 z-depth-1-half">
          <iframe class="embed-responsive-item" src="./help.html" frameborder="0" allowfullscreen></iframe>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
</div>
<script>
$(document).ready(function(){
  $('.dropdown-submenu a.test').on("click", function(e){
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
  });
});

</script>

</body>
</html>
'''

def get_updt_str():
    return f'<i>Last updated: {dt.now().strftime("%x")}</i>'

def remove_items(key_list, items_dict):
    for key in key_list:
        items_dict.pop(key, None)
    return items_dict

def write_file(write_dict):
    for filepath, html_str in write_dict.items():
        with open(filepath, 'w') as f:
            f.write(html_str)

def create_chart_dd(button_label, site_id, charts, data_dir):
    chart_href = Path(data_dir, button_label, site_id, 'charts')
    chart_menu_dict = {}
    for chart_name, chart_none in charts.items():
        chart_label = chart_name.replace('.html', '')
        chart_label = chart_label.upper().replace('_', ' ')
        site_chart_href = Path(chart_href, chart_name)
        chart_menu_dict[chart_label] = site_chart_href

    charts_dd = get_sub_menus(
        'CHARTS',
        chart_href,
        chart_menu_dict,
        sub_menu_dd=''
    )

    return charts_dd

def create_data_dd(button_label, site_id, data, data_dir, meta, data_format):
    data_href = Path(data_dir, button_label, site_id, data_format)
    data_menu_dict = {}
    for data_name, data_none in data.items():
        data_id = data_name.replace(f'.{data_format}', '')
        data_label = get_datatype_name(
            data_id,
            meta
        )
        data_label = data_label.upper()
        site_data_dd_href = Path(data_href, data_name)
        data_menu_dict[data_label] = site_data_dd_href

    data_dd = get_sub_menus(
        f'{data_format.upper()} DATA',
        data_href,
        data_menu_dict,
        sub_menu_dd=''
    )

    return data_dd

def get_folders(rootdir):
    dir_dict = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir_dict)
        parent[folders[-1]] = subdir
    return dir_dict

def get_site_name(site_id, meta):
    df = meta[meta['site_id'] == int(site_id)]
    if not df.empty:
        return df['site_metadata.site_name'].iloc[0].upper()
    return str(site_id)

def get_datatype_name(datatype_id, meta):
    df = meta[meta['datatype_id'] == int(datatype_id)]
    if not df.empty:
        return df['datatype_metadata.datatype_common_name'].iloc[0]
    return datatype_id

def get_button(button_label, dropdown_str):
    nl = '\n'
    drop_down_str = (
        f'    <div class="dropdown">{nl}'
        f'        <button class="btn btn-outline-primary btn-lg '
        f'dropdown-toggle mt-3" type="button" '
        f'data-toggle="dropdown" aria-pressed="false" '
        f'autocomplete="on">{button_label}'
        f'<span class="caret"></span></button>{nl}'
        f'        <ul class="dropdown-menu">{nl}'
        f'            {dropdown_str}{nl}'
        f'        </ul>{nl}'
        f'    </div>{nl}'
    )

    return drop_down_str

def get_menu_entry(label, href):
    nl = '\n'
    return (
        f'<li><a tabindex="0" href="{href}">'
        f'<b><i>{label}</b></i></a></li>{nl}'
    )

def get_sub_menus(label, href, sub_menu_dict={}, sub_menu_dd=''):
    nl = '\n'
    dd_items = []
    for sub_label, sub_href in sorted(sub_menu_dict.items()):
        dd_items.append(
            f'<li><a tabindex="0" href="{sub_href}">{sub_label}</a></li>{nl}'
        )

    sub_menu_str = ''
    if sub_menu_dd:
        sub_menu_str = f'{sub_menu_dd}{nl}'

    sub_menu_str = (
        f'<li class="dropdown-submenu">{nl}'
        f'<a class="test" tabindex="0" href="{href}">'
        f'{label}<span class="caret"></span></a>{nl}'
        f'    <ul class="dropdown-menu">{nl}'
        f'        {"".join(dd_items)}{nl}'
        f'            {sub_menu_str}'
        f'    </ul>{nl}'
        f'</li>{nl}'
    )

    return sub_menu_str

def get_site_submenu_str(data_dir, site_data, site_id, button_label, meta):
    charts_dd = []
    json_dd = []
    csv_dd = []
    for datatype, charts in site_data.items():
        if 'charts' in datatype:
            charts_dd = create_chart_dd(
                button_label,
                site_id,
                charts,
                data_dir
            )

        if 'json' in datatype:
            json_dd = create_data_dd(
                button_label,
                site_id,
                charts,
                data_dir,
                meta,
                'json'
            )

        if 'csv' in datatype:
            csv_dd = create_data_dd(
                button_label,
                site_id,
                charts,
                data_dir,
                meta,
                'csv'
            )

    site_submenu_str = '\n'.join(
        [i for i in [csv_dd, json_dd, charts_dd] if i]
    )

    return site_submenu_str

def create_nav(year_str, data_dir, nav_filename=None):
    nl = '\n'
    if not nav_filename:
        nav_filename = 'crmms_nav.html'
    data_dir = data_dir.replace('/', pathlib.os.sep)
    basepath = os.path.basename(os.path.normpath(data_dir))
    walk_dict = get_folders(data_dir)[basepath]
    to_remove = ['.git', 'pau_www.usbr.gov_uc_water_crmms.csv', 'flat_files', 'assets']
    walk_dict = remove_items(to_remove, walk_dict)
    # walk_dict = sorted(walk_dict, key=lambda x: x if not x.isnumeric() else int(x.split('_')[-1]) - int(x.split('_')[0]))
    button_str_list = []
    walk_dict = {k: v for k, v in walk_dict.items() if v}
    for button_label, dd_items in sorted(walk_dict.items(), key=lambda x: int(x[0].split('_')[0])):
        if dd_items:
            button_path_abs = Path(data_dir, button_label)
            meta_path = Path(button_path_abs, 'meta.csv')
            meta = pd.read_csv(meta_path)
            button_path = Path('.', button_label)
            meta_path = Path(button_path, 'meta.csv')
            map_path = Path(button_path, 'site_map.html')
            meta_menu_entry = get_menu_entry('METADATA', meta_path)
            map_menu_entry = get_menu_entry('SITE MAP', map_path)
            site_menu_list = [meta_menu_entry, map_menu_entry]
            site_name_dict = {
                get_site_name(int(k), meta): k for k, v in dd_items.items() if v
            }

            for site_name, site_id in sorted(site_name_dict.items()):
                site_path = Path(button_path, site_id)
                site_path_abs = Path(button_path_abs, site_id)
                dash_html_str = create_dash(site_name, site_id, site_path_abs)
                dash_filename = 'dashboard.html'
                dash_path_abs = Path(site_path_abs, dash_filename)
                dash_path = Path(site_path, dash_filename)
                dash_write_dict = {
                    dash_path_abs: dash_html_str,
                    Path(site_path_abs, 'index.html'): dash_html_str
                }
                write_file(dash_write_dict)
                dash_menu_entry = get_menu_entry('DASHBOARD', dash_path)
                site_label = f'&bull; {site_name}'
                site_submenu_list = [dash_menu_entry]
                site_submenu_list.append(
                    get_site_submenu_str(
                        '.',
                        dd_items[site_id],
                        site_id,
                        button_label,
                        meta
                    )
                )
                site_submenu_str = '\n'.join(site_submenu_list)
                site_dd = get_sub_menus(
                    site_label,
                    site_path,
                    sub_menu_dd=site_submenu_str
                )
                site_menu_list.append(site_dd)
            sites_dd_str = '\n'.join(site_menu_list)
            folder_button_label = button_label.split('_')
            if folder_button_label[0].isnumeric():
                month_num = int(folder_button_label[0])
                if 0 < month_num < 13:
                    folder_button_label[0] = month_name[month_num]
            folder_button_label = (
                f'{folder_button_label[0]} {folder_button_label[1]}'
                f' CRMMS Results'
            )
            folder_button = get_button(
                folder_button_label,
                sites_dd_str
            )
            button_str_list.append(folder_button)

    if len(button_str_list) > 6:
        col_one = '\n'.join([i for i in button_str_list[:6] if i])
        col_two = '\n'.join([i for i in button_str_list[6:] if i])
        buttons_str = f'''
            <div class="row">
              <div class="col">
                {col_one}
              </div>
              <div class="col">
                {col_two}
              </div>
            </div>
        '''
    else:
        buttons_str = '\n'.join([i for i in button_str_list if i])

    nl = '\n'
    nav_html_str = (
        f'{get_header_str(year_str)}{nl}{get_updt_str()}{nl}{buttons_str}{nl}{footer_str}'
    )
    write_nav_dict = {
        Path(data_dir, nav_filename): nav_html_str,
        Path(data_dir, 'index.html'): nav_html_str
    }
    write_file(write_nav_dict)

    return '  Navigation files created.'

if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(this_dir, 'crmms_viz')
    sys_out = create_nav('CRMMS data', data_dir)
    print(sys_out)
