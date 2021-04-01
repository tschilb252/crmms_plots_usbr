# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 07:57:58 2019

@author: buriona
"""

from datetime import datetime as dt
import numpy as np
import pandas as pd
import folium
import plotly.graph_objs as go

STATIC_URL = 'https://www.usbr.gov/uc/water/hydrodata/assets'

def get_plotly_js():
    return f'{STATIC_URL}/plotly.js'

def get_favicon():
    return f'{STATIC_URL}/img/favicon.ico'

def get_dashboard_css():
    return f'{STATIC_URL}/dashboard.css'

def get_bootstrap():
    
    return {
        'css': f'{STATIC_URL}/bootstrap/css/bootstrap.min.css',
        'js': f'{STATIC_URL}/bootstrap/js/bootstrap.bundle.js',
        'jquery': f'{STATIC_URL}/jquery.js',
        'popper': f'{STATIC_URL}/popper.js',
        'fa': f'{STATIC_URL}/font-awesome/css/font-awesome.min.css',
    }

def get_bor_seal(orient='default', grey=False):
    color = 'cmyk'
    if grey:
        color = 'grey'
    seal_dict = {
        'default': f'BofR-horiz-{color}.png',
        'shield': 'BofR-shield-cmyk.png',
        'vert': f'BofR-vert-{color}.png',
        'horz': f'BofR-horiz-{color}.png'
        }
    return f'{STATIC_URL}/img/{seal_dict[orient]}'

def get_default_js():
    
    bootstrap_dict = get_bootstrap()
    return [
        ('leaflet', 
         f'{STATIC_URL}/leaflet/js/leaflet.js'),
        ('jquery', 
         bootstrap_dict['jquery']),
        ('popper', 
         bootstrap_dict['popper']),
        ('bootstrap', 
         bootstrap_dict['js']),
        ('awesome_markers', 
         f'{STATIC_URL}/leaflet-awesome-markers/leaflet.awesome-markers.min.js'),
    ]

def get_default_css():
    
    bootstrap_dict = get_bootstrap()
    return [
        ('leaflet_css', 
         f'{STATIC_URL}/leaflet/css/leaflet.css'),
        ('bootstrap_css', 
         bootstrap_dict['css']),
        ('awesome_markers_font_css', 
          bootstrap_dict['fa']),
        ('awesome_markers_css', 
        f'{STATIC_URL}/leaflet-awesome-markers/leaflet.awesome-markers.css'),
        ('awesome_rotate_css', 
         f'{STATIC_URL}/leaflet-awesome-markers/leaflet.awesome.rotate.css'),
    ]

def get_crmms_hdb_site_map():
    return {
        'BlueMesa': 913,
        'Crystal': 915,
        'FlamingGorge': 917,
        'Fontenelle': 916,
        'Havasu': 923,
        'Mead': 921,
        'Mohave': 922,
        'MorrowPoint': 914,
        'Navajo': 920,
        'Powell': 919,
        'TaylorPark': 912,
        'Vallecito': 933
    }

def res_display_names():
    return {
        'BlueMesa': 'Blue Mesa',
        'Crystal': 'Crystal',
        'FlamingGorge': 'Flaming Gorge',
        'Fontenelle': 'Fontenelle',
        'Havasu': 'Lake Havasu',
        'Mead': 'Lake Mead',
        'Mohave': 'Lake Mohave',
        'MorrowPoint': 'Morrow Point',
        'Navajo': 'Navajo',
        'Powell': 'Lake Powell',
        'TaylorPark': 'Taylor Park',
        'Vallecito': 'Vallecito'
    }

def get_hdb_alias_map():
    return {
        'BlueMesa': 'uc',
        'Crystal': 'uc',
        'FlamingGorge': 'uc',
        'Fontenelle': 'uc',
        'Havasu': 'lc',
        'Mead': 'lc',
        'Mohave': 'lc',
        'MorrowPoint': 'uc',
        'Navajo': 'uc',
        'Powell': 'uc',
        'TaylorPark': 'uc',
        'Vallecito': 'uc'
    }

def get_crmms_hdb_datatype_map():
    return {
        'Bank Storage': 15,
        'Energy': None,
        'Evaporation': 25,
        'Inflow': 30,
        'Inflow_cfs': 29,
        'Outflow_cfs': 42,
        'Outflow': 43,
        'Peak Flow': None,
        'Pool Elevation': 49,
        'Power Plant Cap Fraction': None,
        'Spill': 46,                                                            #need to come up with scheme for converting to acre-ft, units maybe?
        'Storage': 17,
        'Surface Area': 89,
        'Unregulated Spill': 46,                                                 #get clarification on this
        'Regulated Spill': 46
    }

def map_sids(site_name):
    sids_dict = {
        'BlueMesa': 913,
        'Crystal': 915,
        'FlamingGorge': 917,
        'Fontenelle': 916,
        'Havasu': 923,
        'Mead': 921,
        'Mohave': 922,
        'MorrowPoint': 914,
        'Powell': 919,
        'Navajo': 920,
        'TaylorPark': 912,
        'Vallecito': 933
    }

    return sids_dict.get(site_name, np.nan)

def map_dids(datatype_name):
    dids_dict = {
        'Outflow': 43,
        'Outflow_cfs': 42,
        'Bank Storage': 15,
        'Inflow': 30,
        'Inflow_cfs': 29,
        'Pool Elevation': 49,
        'Storage': 17,
        'Evaporation': 25,
        'Surface Area': 89,
    }

    return dids_dict.get(datatype_name, np.nan)

def print_and_log(log_str, logger=None):
    print(log_str)
    if logger:
        logger.info(log_str)

def serial_to_trace(df, val_col='value', trace_col='trace', dt_col='datetime'):
    traces = list(df[trace_col].unique())
    dates = list(df[dt_col].unique())
    df_out = pd.DataFrame(index=dates)
    for trace in sorted(traces):
        df_temp = df[df[trace_col] == trace][val_col]
        df_out[trace] = df_temp.to_list()
        df_out.index.name = 'date'
    return df_out

def get_tiers(site_name, datatype, years):
    powell_upper_tier = {
        'elev': {
            2018: 3654, 2019: 3655, 2020: 3657, 2021: 3659, 2022: 3660,
            2023: 3662, 2024: 3663, 2025: 3664, 2026: 3666
        },
        'storage': {
            2018: 17718762, 2019: 17846128, 2020: 18102788, 2021: 18362017,
            2022: 18492595, 2023: 18755868, 2024: 18888610, 2025: 19022090,
            2026: 19291262
        }
    }
    tiers = {
        'lake powell': {
            'pool elevation': {
                'Upper Balancing Tier':
                    [powell_upper_tier['elev'].get(yr, 3666) for yr in years],
                'Mid-Elevation Balancing Tier': [3575] * len(years),
                'Lower-Elevation Balancing Tier': [3525] * len(years)
            },
            'storage': {
                'Upper Balancing Tier':
                    [powell_upper_tier['storage'].get(yr, 19291262) for yr in years],
                'Mid-Elevation Balancing Tier': [9500000] * len(years),
                'Lower-Elevation Balancing Tier': [5900000] * len(years)
            }
        },
        'lake mead': {
            'pool elevation': {
                'Domestic Surplus Condition': [1200] * len(years),
                'Normal ICS Surplus Condition': [1145] * len(years),
                'Shortage Condition 7.167': [1075] * len(years),
                'Shortage Condition 7.083': [1050] * len(years),
                'Shortage Condition 7.0': [1025] * len(years)
            },
            'storage': {
                'Domestic Surplus Condition': [22900000] * len(years),
                'Normal ICS Surplus Condition': [15900000] * len(years),
                'Shortage Condition 7.167': [9400000] * len(years),
                'Shortage Condition 7.083': [7500000] * len(years),
                'Shortage Condition 7.0': [5800000] * len(years)
            }
        }
    }
    return tiers[site_name][datatype]

def get_tier_traces(t1, t2, site_name, datatype):
    tier_datatypes = ['pool elevation', 'storage']
    tier_sites = ['lake powell', 'lake mead']
    if site_name.lower() not in tier_sites or datatype.lower() not in tier_datatypes:
        return None
    years = list(range(t1.year, t2.year+1))
    tiers = get_tiers(site_name, datatype, years)
    tier_months = {'lake powell': 10, 'lake mead': 12}
    tier_month = tier_months[site_name]
    dates = [dt(year, tier_month, 1) for year in years]
    traces = []
    hover_templates = {
        'storage': "%{text}",
        'pool elevation': "%{y:,.0f}'"
    }
    for tier_name, tier_vals  in tiers.items():
        text = [
            f'{tier_vals[i]/1000:0.0f} kaf' for i, year in enumerate(years)
        ]
        trace = go.Scatter(
            x=dates,
            y=tier_vals,
            text=text,
            name=tier_name,
            visible=True,
            showlegend=False,
            legendgroup='TIERS',
            hovertemplate=hover_templates[datatype.lower()],
            mode='lines+markers',
            marker=dict(
                symbol='triangle-down',
                color='rgba(20,20,20,0.4)',
                size = 8
            ),
            line=dict(
                color='rgba(20,20,20,0.2)',
                dash='dot',
                width=2,
                shape='hv'
            )
        )
        traces.append(trace)
    return traces


def get_fa_icon(obj_type='default'):
    fa_dict = {
        'default': 'map-pin',
        1: 'sitemap',
        2: 'umbrella',
        3: 'arrow-down',
        4: 'exchange',
        5: 'plug',
        6: 'arrows-v',
        7: 'tint',
        8: 'snowflake-o',
        9: 'tachometer',
        10: 'cogs',
        11: 'arrows-h',
        12: 'rss',
        13: 'flask',
        14: 'table',
        15: 'info',
        20: 'exchange'
    }
    fa_icon = fa_dict.get(obj_type, 'map-pin')
    return fa_icon

def get_icon_color(row):
    obj_owner = 'BOR'
    if not row.empty:
        if row['site_metadata.scs_id']:
            obj_owner = 'NRCS'
        if row['site_metadata.usgs_id']:
            obj_owner = 'USGS'
    color_dict = {
        'BOR': 'blue',
        'NRCS': 'red',
        'USGS': 'green',
    }
    icon_color = color_dict.get(obj_owner, 'black')
    return icon_color

def add_optional_tilesets(folium_map):
    tilesets = {
        "Terrain": 'Stamen Terrain',
        'Street Map': 'OpenStreetMap',
        'Toner': 'Stamen Toner',
        'Watercolor': 'Stamen Watercolor',
        'Positron': 'CartoDB positron',
        'Dark Matter': 'CartoDB dark_matter',
    }
    for name, tileset in tilesets.items():
        folium.TileLayer(tileset, name=name).add_to(folium_map)

def add_huc_layer(huc_map, level=2, huc_geojson_path=None, embed=False, 
                  show=True, huc_filter='', zoom_on_click=False):
    try:
        if type(huc_filter) == int:
            huc_filter = str(huc_filter)
        weight = -0.25 * float(level) + 2.5
        if not huc_geojson_path:
            huc_geojson_path = f'{STATIC_URL}/gis/HUC{level}.geojson'
        else:
            embed = True
        if huc_filter:
           huc_style = lambda x: {
            'fillColor': '#ffffff00', 'color': '#1f1f1faa', 
            'weight': weight if x['properties'][f'HUC{level}'].startswith(huc_filter) else 0
        } 
        else:
            huc_style = lambda x: {
                'fillColor': '#ffffff00', 'color': '#1f1f1faa', 'weight': weight
            }
        folium.GeoJson(
            huc_geojson_path,
            name=f'HUC {level}',
            embed=embed,
            style_function=huc_style,
            zoom_on_click=zoom_on_click,
            show=show
        ).add_to(huc_map)
    except Exception as err:
        print(f'Could not add HUC {level} layer to map! - {err}')

def clean_coords(coord_series, force_neg=False):
    
    coord_series = coord_series.apply(
        pd.to_numeric, 
        errors='ignore', 
        downcast='float'
    )
    if not coord_series.apply(type).eq(str).any():
        if force_neg:
            return -coord_series.abs()
        return coord_series
    results = []
    for idx, coord in coord_series.iteritems():
        if not str(coord).isnumeric():
            coord_strs = str(coord).split(' ')
            coord_digits = []
            for coord_str in coord_strs:
                coord_digit = ''.join([ch for ch in coord_str if ch.isdigit() or ch == '.'])
                coord_digits.append(float(coord_digit))
            dec = None
            coord_dec = 0
            for i in reversed(range(0, len(coord_digits))):
                if dec:
                    coord_dec = abs(coord_digits[i]) + dec
                dec = coord_digits[i] / 60
            if str(coord)[0] == '-':
                coord_dec = -1 * coord_dec
            results.append(coord_dec)
        else:
            results.append(coord)
    if force_neg:
        results[:] = [-1 * result if result > 0 else result for result  in results]
    clean_series = pd.Series(results, index=coord_series.index)
    return clean_series

def is_url_safe(partial_url):
    unsafe_char = [
        '"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`',
        ';', '/', '?', ':', '@', '=', '&'
    ]
    for char in unsafe_char:
        if char in partial_url:
            return char
    return True

def get_html_head():
    bootstrap = get_bootstrap()
    bootstrap_css = bootstrap['css']
    bor_flavicon = get_favicon()
    dashboard_css = get_dashboard_css()
    return f'''
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="{bor_flavicon}">
  <link rel="stylesheet" href="{bootstrap_css}">
  <link rel="stylesheet" href="{dashboard_css}">
</head>
'''

def get_js_refs():
    bootstrap = get_bootstrap()
    bootstrap_js = bootstrap['js']
    jquery_js = bootstrap['jquery']
    popper_js = bootstrap['popper']
    feather_js = f'{STATIC_URL}/feather/feather.min.js'
    return (f'''
<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
  <script src="{jquery_js}"></script>
  <script src="{popper_js}"></script>
  <script src="{bootstrap_js}"></script>
''' + f'''
<!-- Icons -->
  <script src="{feather_js}"></script>
  <script>
    feather.replace()
  </script>
''' + '''
<!-- to enable link to tab -->
  <script>
    $(document).ready(() => {
      let url = location.href.replace(/\/$/, "");

      if (location.hash) {
        const hash = url.split("#");
        $('#navTabs a[href="#'+hash[1]+'"]').tab("show");
        url = location.href.replace(/\/#/, "#");
        history.replaceState(null, null, url);
        setTimeout(() => {
          $(window).scrollTop(0);
        }, 400);
      }

      $('a[data-toggle="tab"]').on("click", function() {
        let newUrl;
        const hash = $(this).attr("href");
        if(hash == "#home") {
          newUrl = url.split("#")[0];
        } else {
          newUrl = url.split("#")[0] + hash;
        }
        newUrl += "/";
        history.replaceState(null, null, newUrl);
      });
    });
  </script>'''
)
            
if __name__ == '__main__':
    print('Utility file... I do nothing...  (╯︵╰,)')