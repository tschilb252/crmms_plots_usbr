# -*- coding: utf-8 -*-
"""
Created on Fri May 31 07:43:40 2019

@author: buriona
"""


from os import path
import folium
import pandas as pd
from folium.plugins import FloatImage
from crmms_utils import add_optional_tilesets, add_huc_layer, clean_coords
from crmms_utils import get_bor_seal, get_favicon
from crmms_utils import get_default_js, get_default_css

pd.options.mode.chained_assignment = None

default_js = get_default_js()
default_css = get_default_css()

folium.folium.Map.default_js = default_js
folium.folium.Map.default_css = default_css

def get_bounds(meta):
    meta_no_dups = meta.drop_duplicates(subset='site_id')
    lats = []
    longs = []
    for index, row in meta_no_dups.iterrows():
        try:
            lat = float(row['site_metadata.lat'])
            lon = float(row['site_metadata.longi'])
            if 0 <= lat <= 180:
                lats.append(lat)
            if -180 <= lon <= 0:
                longs.append(lon)
        except (ValueError, TypeError):
            pass

    max_lat = max(lats)
    max_long = -1 * max([abs(i) for i in longs])
    min_lat = min(lats)
    min_long = -1 * min([abs(i) for i in longs])
    return [(min_lat, max_long), (max_lat, min_long)]

def get_embed(href):
    embed = (
        f'<div class="container embed-responsive embed-responsive-16by9" style="overflow: hidden; height: 622px; width: 1200px;">'
        f'<iframe scrolling="no" class="embed-responsive-item" src="{href}" allowfullscreen></iframe>'
        f'</div>'
    )   
    return embed

def add_markers(sitetype_map, meta):
    meta_no_dups = meta.drop_duplicates(subset='site_id')
    for index, row in meta_no_dups.iterrows():
        try:
            site_id = row['site_id']
            lat = float(row['site_metadata.lat'])
            lon = float(row['site_metadata.longi'])
            elev = row['site_metadata.elevation']
            lat_long = [lat, lon]
            site_name = row['site_metadata.site_name']
            href = f'./{site_id}/dashboard.html'
            embed = get_embed(href)

            popup_html = (
#                f'<a href="{href}" target="_blank">OPEN IN NEW WINDOW</a><br>'
                f'{embed}'
                f'Latitude: {round(lat, 3)}, '
                f'Longitude: {round(lon, 3)}, '
                f'Elevation: {elev} <br>'
            )

            icon = 'tint'
            folium.Marker(
                location=lat_long,
                popup=popup_html,
                tooltip=site_name,
                icon=folium.Icon(icon=icon, prefix='fa')
            ).add_to(sitetype_map)
        except (ValueError, TypeError):
            pass

def create_map(site_type, meta, data_dir):
    meta = meta.drop_duplicates(subset='site_id')
    meta['site_metadata.lat'] = clean_coords(meta['site_metadata.lat'])
    meta['site_metadata.longi'] = clean_coords(meta['site_metadata.longi'], True)
    
    sitetype_dir = path.join(data_dir, site_type)
    map_filename = 'site_map.html'
    map_path = path.join(sitetype_dir, map_filename)

    sitetype_map = folium.Map(tiles=None)
    bounds = get_bounds(meta.copy())
    if bounds:
        sitetype_map.fit_bounds(bounds)
        add_markers(sitetype_map, meta.copy())
        # add_huc_layer(
        #     sitetype_map, level=2, huc_filter=('14', '15'), show=True
        # )
        # add_huc_layer(sitetype_map, level=6, huc_filter=('14', '15'))
        # add_huc_layer(sitetype_map, level=8, huc_filter=('14', '15'))
        add_optional_tilesets(sitetype_map)
        folium.LayerControl().add_to(sitetype_map)
        FloatImage(
            get_bor_seal(orient='horz'),
            bottom=1,
            left=1
        ).add_to(sitetype_map)
        # MousePosition(prefix="Location: ").add_to(sitetype_map)
        sitetype_map.save(map_path)
        flavicon = (
            f'<link rel="shortcut icon" '
            f'href="{get_favicon()}"></head>'
        )
        with open(map_path, 'r') as html_file:
            chart_file_str = html_file.read()

        with open(map_path, 'w') as html_file:
            chart_file_str = chart_file_str.replace(r'</head>', flavicon)
            replace_str = (
                '''left:1%;
                    max-width:15%;
                    max-height:15%;
                    background-color:rgba(255,255,255,0.5);
                    border-radius: 10px;
                    padding: 10px;'''
            )
            chart_file_str = chart_file_str.replace(r'left:1%;', replace_str)
            html_file.write(chart_file_str)
            
        with open(path.join(sitetype_dir, 'index.html'), 'w') as index_pg:
            index_pg.write(chart_file_str)
            
        return f'  Created map for {site_type}'
    else:
        return '  Failed to create map for {site_type}, no sites with coordinates'

if __name__ == '__main__':
    this_dir = path.dirname(path.realpath(__file__))
    data_dir = path.join(this_dir, 'crmms_viz')

    site_types = ['1_2020']
    for site_type in site_types:
        site_type_dir = path.join(data_dir, site_type)
        meta_path = path.join(data_dir, site_type, 'meta.csv')
        meta = pd.read_csv(meta_path)

        create_map(site_type, meta, data_dir)
