import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
from datetime import datetime as dt
from app import app
import dash_bootstrap_components as dbc
# from data import df_revenue, df_pc, df_rev

app = dash.Dash(__name__)
# app.config['suppress_callback_exceptions']=True
app.config.suppress_callback_exceptions = True

server = app.server

def get_header():

    header = html.Div([

        # html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            # html.H1(children='Pivot Bio',
            #         style = {'textAlign' : 'center', 'color':'white'}
            # )],
            html.Img(src='/assets/Pivot-Bio-Logo-483x100.webp')],
            
            className='col-12',
            style = {'padding-top' : '1%'}
        ),
        ],
        className = 'row',
        style = {'height' : '4%'}
        )

    return header

def get_navbar(p = 'homepage'):
    navbar_homepage = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Revenue'),
                href='/apps/revenue'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per Capita Rev.'),
                href='/apps/pc_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per License Rev.'),
                href='/apps/pl_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Businesses'),
                href='/apps/biz'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2')
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
      
    if p == 'homepage':
        return navbar_homepage
    # elif p == 'revenue':
    #     return navbar_revenue
    # elif p == 'pc_rev':
    #     return navbar_pcrev
    # elif p == 'pl_rev':
    #     return navbar_plrev
    # elif p == 'biz':
    #     return navbar_biz

def home_page_App():
    return html.Div([
        get_header(),
        # get_navbar()
    ])

    app.layout = home_page_App