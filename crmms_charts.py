# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 07:55:52 2019

@author: buriona
"""

import branca
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime as dt
from crmms_utils import get_tier_traces, get_bor_seal, serial_to_trace

def get_colormap():
    return branca.colormap.StepColormap(
        ["#001889","#AB1488","#D24E71","#E8853A","#ECC000"],
        [1980, 1990, 2000, 2010, 2020]
    )

def get_trace_color(wy, colormap=get_colormap()):
    wy_str = str(wy)
    color_dict = {
        '24MS MOST': '#3de12e', 
        '24MS MIN': 'red', 
        '24MS MAX': 'blue', 
        'OBSERVED': 'black'
    }
    if wy_str.isdigit():
        c = colormap.rgba_floats_tuple(int(wy_str))
        return f'rgba({c[0] * 255}, {c[1] * 255}, {c[2] * 255}, 0.5)'
    return color_dict.get(wy_str, 'black')

def get_hovertemplate(units):
    hover_dict = {
       'acre-ft': "%{text:,.0f} kaf",#"<br>%{x}",
       'acre-ft/month': "%{text:,.0f} kaf/month",#<br>%{x}",
       'ft': "%{y:,.1f}'",#<br>%{x}"
    }
    return hover_dict.get(units, "{y:,.2f}")#<br>{x}")

def get_log_scale_dd():
    log_scale_dd = [
        {
            'active': 0,
            'showactive': True,
            'x': 1.005,
            'y': -0.035,
            'xanchor': 'left',
            'yanchor': 'top',
            'bgcolor': 'rgba(0,0,0,0)',
            'type': 'buttons',
            'direction': 'down',
            'font': {
                'size': 10
            },
            'buttons': [
                {
                    'label': 'Linear Scale',
                    'method': 'relayout',
                    'args': ['yaxis', {'type': 'linear'}]
                },
                {
                    'label': 'Log Scale',
                    'method': 'relayout',
                    'args': ['yaxis', {'type': 'log'}]
                },
            ]
        }
    ]
    return log_scale_dd

def create_wy_traces(df, datatype_name, units, colormap=get_colormap()):
    show_traces = ['24MS MOST', '24MS MIN', '24MS MAX', 'OBSERVED']
    visible = {True: True, False: 'legendonly'}
    traces = []
    water_years = df.columns.tolist()
    linetype = 'solid'
    for wy in water_years:
# TODO: This is for temp removal of next WY for MTOM traces
        if wy not in show_traces:
            df_temp = df[wy]
            year = df_temp.index[1].year
            df_temp = df_temp[df_temp.index.year == year]
        else:
            df_temp = df[wy]
# TODO: move else statement to only case to revert, delete above, uncomment below
        #df_temp = df[wy]
        x_vals = df_temp.index
        y_vals = df_temp.values
        show_trace = visible[wy.upper() in show_traces]
        color = get_trace_color(wy, colormap)
        width = 2
        if not str(wy).isdigit():
            width = 3
        if get_chart_type(datatype_name, units) == 'bar':
            trace = bar_trace(
                x_vals,
                y_vals,
                show_trace,
                f'{wy}'
            )
        else:
            trace = scatter_trace(
                x_vals,
                y_vals,
                show_trace,
                f'{wy}',
                color,
                linetype,
                width,
                get_hovertemplate(units)
            )
        if not 'mtom' in f'{wy}'.lower():
            traces.append(trace)

    return traces

def create_stat_traces(df, datatype_name, units):
    show_traces = ['50%']#['10%', '50%', '90%']
    visible = {True: True, False: 'legendonly'}
    color_dict = {
        'min': 'rgba(255,36,57,0.6)',
        '90%': 'rgba(48,204,255,0.6)',
        '75%': 'rgba(46,255,166,0.6)',
        '50%': 'rgba(63,255,43,0.6)',
        '25%': 'rgba(204,255,40,0.6)',
        '10%': 'rgba(255,161,38,0.6)',
        'max': 'rgba(50,68,255,0.6)',
        'mean': 'rgba(63,255,43,0.6)'
    }
    line_types = {'mean': 'dash', '50%': 'dot'}
    traces = []
#        go.Scatter(
#            x=[df.index],
#            y=[df['50%'].values],
#            name='SHADING',
#            fill='none',
#            visible='legendonly',
#            line=dict(width=0),
#            hoverinfo='none',
#            legendgroup='stat_traces',
#            showlegend=True,
#        )
#    ]

    df.drop(columns=['count', 'std'], inplace=True)
    cols = df.columns.tolist()
    cols.insert(3, cols.pop(0))
    for col in cols:
        show_trace = visible[col.lower() in show_traces]
        color = color_dict.get(col, 'rgba(0,0,0,0.3)')
        linetype = line_types.get(col, 'dashdot')
# TODO: This is for temp removal of next WY for MTOM traces
        df_temp = df[col]
        year = df_temp.index[1].year
        df_temp = df_temp[df_temp.index.year == year]
# TODO: move else statement to only case to revert, delete above, uncomment below        
        #df_temp = df[col]
        x_vals = df_temp.index
        y_vals = df_temp.values
        trace_name = f'{col.upper()}'
        width = 2
        if '%' in col:
            exceedance = 100 - int(col.replace('%', ''))
            trace_name = f'{exceedance}%'
        chart_type = get_chart_type(datatype_name, units)
        if chart_type == 'bar':
            if col in ['90%', '75%', '50%', '25%', '10%']:
                stats_trace = stats_shaded_trace(
                    x_vals,
                    y_vals,
                    trace_name,
                    color,
                    chart_type
                )
                traces.append(stats_trace)
            trace = bar_trace(
                x_vals,
                y_vals,
                show_trace,
                trace_name,
                color
            )
        else:
            if col in ['90%', '75%', '50%', '25%', '10%']:
                stats_trace = stats_shaded_trace(
                    x_vals,
                    y_vals,
                    trace_name,
                    color,
                    chart_type
                )
                traces.append(stats_trace)
            if '50' in col:
                trace_name = 'MEDIAN'
                width = 3
                color = 'rgba(63,255,43,1)'
            trace = scatter_trace(
                x_vals,
                y_vals,
                show_trace,
                trace_name,
                color,
                linetype,
                width,
                get_hovertemplate(units)
            )
        traces.append(trace)

    return traces

def bar_stat_shading(x, y, days=14):
    width = pd.Timedelta(days=days)
    x = x.to_list()
    x = [[i - width, i - width, i + width, i + width] for i in x]
    x = [j for k in x for j in k]
    y = [[0, i, i, 0] for i in y]
    y = [j for k in y for j in k]

    return x, y

def stats_shaded_trace(x, y, name, color, chart_type):
    showlegend = False
    name = f'{name}_stats'
    fill = 'tonexty'
    shape = 'linear'
    if chart_type == 'bar':
        shape = 'vh'
        x, y = bar_stat_shading(x, y)
    if '90%' in name.upper():
        fill = 'none'
        if chart_type == 'bar':
            fill = 'tozeroy'

#    if 'MEDIAN' in name:
#        showlegend = True
#        name = 'STATS'

    trace = go.Scatter(
        x=x,
        y=y,
        name=name,
        visible=True,
        fill=fill,
        line=dict(
            width=0,
            shape=shape
        ),
        fillcolor='rgba(0,0,0,0.2)',#color.replace(',0.6)', ',0.4)'),
        hoverinfo='skip',
        legendgroup='MTOM CLOUD',
        connectgaps=True,
        showlegend=showlegend,
        stackgroup='stats',
        orientation='h'
    )
    return trace

def scatter_trace(x, y, show_trace, name, color=None, linetype='solid',
                  width=2, hovertemplate=None):
    
    trace = go.Scatter(
        x=x,
        y=y,
        text=[i/1000 if i else i for i in y],
        name=name,
        visible=show_trace,
        line=dict(
            color=color,
            dash=linetype,
            width=width
        ),
        hovertemplate=hovertemplate,
        mode='lines'
    )
    return trace

def bar_trace(x, y, show_trace, name, color=None):
    trace = go.Bar(
        x=x,
        y=y,
        text=[i/1000 if i else i for i in y],
        name=name,
        visible=show_trace,
        marker=dict(
            color=color
        )
    )
    return trace

def get_chart_type(datatype_name, units):
#    if 'acre-ft' in units.lower() and 'storage' not in datatype_name.lower():
#        return 'bar'
    return 'scatter'

def get_anno_text(df, df_stats, units):
    curr_year = max(df.columns)
    last_row = df.loc[df[curr_year].last_valid_index()]
    last_date = f'{last_row.name.strftime("%b %d")}, {curr_year}'
    last_data = round(last_row.iloc[-1], 2)
    last_year_data = round(last_row.iloc[-2], 2)
    stats_row = df_stats.loc[last_row.name]
    avg_data = stats_row['mean']
    median_data = stats_row['50%']

    if avg_data > 0:
        percent_avg = f'{round(100 * last_data / avg_data, 0):.0f}'
    else:
        percent_avg = 'N/A'

    if median_data > 0:
        percent_median = f'{round(100 * last_data / median_data, 0):.0f}'
    else:
        percent_median = 'N/A'

    if last_year_data > 0:
        percent_last_year = f'{round(100 * last_data / last_year_data, 0):.0f}'
    else:
        percent_last_year = 'N/A'

    last_data_str = f'{last_data:0,.0f}'
    if last_data > 1000000:
        last_data_str = f'{last_data / 1000:0,.2f} K'

    anno_text = (
        f'As of: {last_date}:<br>'
        f'Currently: {last_data_str} {units}<br>'
        f"% Avg. ('81-'10): {percent_avg}%<br>"
        f"% Median ('81-'10): {percent_median}%<br>"
        f'% Last Year: {percent_last_year}%'
    )
    return anno_text

def legend_heading(name, legendgroup=None, fillcolor='rgba(0,0,0,0)'):
    return [
        go.Scatter(
            x=[None], y=[None],
            name=f'<b>{name}</b>',
            line={'color': 'rgba(0, 0, 0, 0)'},
            legendgroup=legendgroup,
            fillcolor=fillcolor, 
            hoverinfo='skip'
        )
    ]

def get_comp_fig(df_slot, df_obs, site_name, datatype_name, units, date_str,
                 no_mtom=False, watermark=False):

    msg = f'  Working on {site_name} - {datatype_name} CRMMS chart...'
    print(msg)

    chart_type = get_chart_type(datatype_name, units)
    tickformat = {'scatter': "%b '%y", 'bar': "%b '%y"}
    df_trace = serial_to_trace(df_slot.copy())
    df_obs_trace = serial_to_trace(df_obs.copy())
    model_rng = df_trace.index.tolist()
    obs_rng = df_obs_trace.index.tolist()
    initial_rng = [obs_rng[0], model_rng[24]]
    percentiles = [0.10, 0.25, 0.50, 0.75, 0.90]
    non_stats_cols = [x for x in df_trace.columns if not str(x).isdigit()]
    df_stats = df_trace.drop([non_stats_cols], errors='ignore')
    df_stats = df_stats.transpose()
    df_stats = df_stats.describe(percentiles=percentiles).transpose()
    
    colormap = get_colormap()
    traces = create_wy_traces(df_trace, datatype_name, units, colormap)
    stat_traces = create_stat_traces(df_stats, datatype_name, units)
    obs_trace = create_wy_traces(df_obs_trace, datatype_name, units)

    cloud_heading = legend_heading(
            'MTOM Stats', 
            legendgroup='MTOM CLOUD',
            fillcolor='rgba(0,0,0,0)'
        )

    mtom_traces = [i for i in traces if i.name.isnumeric() or 'MTOM' in i.name]
    twenty_four_month_traces = [i for i in traces if '24MS' in i.name]
    
    traces = []
    mtom_traces = []
    mtom_traces.extend(mtom_traces)
    mtom_traces.extend(legend_heading('MTOM Traces'))
    mtom_traces.extend(stat_traces)
    mtom_traces.extend(cloud_heading)
    # )
    #     mtom_traces + legend_heading('MTOM Traces') + stat_traces + cloud_heading      
    # )
    if not no_mtom:
        traces.extend(mtom_traces)
        
    traces.extend(twenty_four_month_traces)
    traces.extend(obs_trace)

    tier_traces = get_tier_traces(
        obs_rng[0], model_rng[-1], site_name.lower(), datatype_name.lower()
    )
    if tier_traces:
        traces.extend(tier_traces)

    seal_image = [{
        'source': get_bor_seal(),
        'xref': 'paper',
        'yref': 'paper',
        'x': 0.01,
        'y': 1.00,
        'sizex': 0.135,
        'sizey': 0.3,
        'yanchor': 'top',
        'xanchor': 'left',
        'opacity': 0.3,
        'layer': 'below'
    }]

    annotation = [
        {
            'x': 1,
            'y': -0.3,
            'xref': 'paper',
            'yref': 'paper',
            'text': f"Created: {dt.utcnow().strftime('%x %I:%M %p UTC')}",
            'showarrow': False,
            'align': 'left',
            'yanchor': 'top',
            'xanchor': 'right',
            'font': {'size': 8, 'color': 'rgba(0,0,0,0.3)'}
        }
    ]
    if watermark:
        annotation.append(
            {
                'x': 0.5,
                'y': 0.5,
                'xref': 'paper',
                'yref': 'paper',
                'text': "<b>SITE UNDER DEVELOPMENT, NOT OFFICIAL</b>",
                'showarrow': False,
                'align': 'center',
                'yanchor': 'middle',
                'xanchor': 'center',
                'font': {'size': 35, 'color': 'rgba(0,0,0,0.15)'},
                'textangle': -27
            }
        )

#    if not df_stats.dropna().empty:
#        anno_text = get_anno_text(df_slot, df_stats, units)
#        annotation.append(
#            {
#                'x': 1,
#                'y': 1.04,
#                'xref': 'paper',
#                'yref': 'paper',
#                'text': anno_text,
#                'showarrow': False,
#                'align': 'left',
#                'yanchor': 'top',
#                'xanchor': 'right',
#                'bordercolor': 'black',
#                'borderpad': 5,
#                'bgcolor': 'rgba(255,255,255,0.3)',
#                'font': {'size': 10}
#            }
#        )
    
    layout = go.Layout(
        template='plotly_white',
        title=(
            f'<b>{site_name} - {datatype_name} - {date_str}</b>'.upper()
        ),
        autosize=True,
        annotations=annotation,
        images=seal_image,
        yaxis=dict(
            title=f'{datatype_name} ({units})'
        ),
        xaxis=dict(
            type='date',
            tickformat=tickformat[chart_type],
            dtick="M3",
            tickangle=-15,
            rangeslider=dict(thickness=0.1),
            range=initial_rng
        ),
        hovermode="x unified",
        legend={
            'orientation': 'v',
            'tracegroupgap': 6,
            'traceorder': 'reversed'
        },
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=50,
            pad=5
        ),
        updatemenus=get_log_scale_dd()
    )

    fig = go.Figure(
        data=traces,
        layout=layout
    )

    return fig

if __name__ == '__main__':
    print('Needs tests...')