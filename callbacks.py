import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import pandas as pd
import os
from dash.dependencies import Input, Output, State
from app import app
import base64
import datetime
import io
import dash_table
# from data import df_revenue, sources, df_rev, df_biz, categories_table, text, df_bidness, df_pc, df_pop
# from homepage import ty_per_sec
from dotenv import load_dotenv
import plotly.graph_objs as go
# from apps.revenue import month_values
import datetime

load_dotenv()


# print(cities)


################################################################
# Map Callback
################################################################

@app.callback(
    Output('site-map', 'figure'),
    Input('region', 'value'))
def update_site_map(region):
    # print(region)
    sites = pd.read_csv("sites.csv")
    print(sites)
    data = [dict(
        lat = sites['lat'],
        lon = sites['lon'],
        type = 'scattermapbox',
        marker = dict(size=7)
    )]

    layout = dict(
        mapbox = dict(
            
        center = dict(lat=39, lon=-105.5),
        accesstoken = os.environ.get("mapbox_token"),
        zoom = 6,
        style = 'light',
        ),
        hovermode = 'closest',
        height = 500,
        margin = dict(r=0, l=0, t=0, b=0),
        clickmode = 'event+select'
    )
    fig = dict(data=data, layout=layout)
    return fig
    

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=10
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])