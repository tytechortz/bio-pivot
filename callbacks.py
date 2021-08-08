import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import pandas as pd
import os
from dash.dependencies import Input, Output, State
from app import app
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
    print(region)
    cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
    print(cities)
    data = [dict(
        lat = cities['lat'],
        lon = cities['lon'],
        type = 'scattermapbox',
        marker = dict(size=7)
    )]
    # layers=[
        
    #   ]

    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39, lon=-105.5),
                # zoom = 5.6,
                zoom = 6,
                style = 'white-bg',
                # layers = layers
            ),
            hovermode = 'closest',
            height = 500,
            margin = dict(r=0, l=0, t=0, b=0),
            clickmode = 'event+select'
        )

    fig = dict(data=data, layout=layout)
    return fig

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])