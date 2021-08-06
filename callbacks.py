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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])