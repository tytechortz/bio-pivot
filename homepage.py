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

def get_emptyrow(h='15px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow

def get_header(p= 'homepage'):

    header = html.Div([
        html.Div([
            html.Img(src='/assets/Pivot-Bio-Logo-483x100.webp'),
        ],  
            className='col-6',
            style = {'padding-top' : '1%'}
        ),
        # get_emptyrow(),
        html.Div([
                dcc.Link(
                    html.H2(children='Home', style={'color':'black'}),
                    href='/homepage'
                )
            ],
                style = {'padding-top' : '2.5%'}
            ),
    ],
    className = 'row',
    style = {'height' : '4%'}
    )

    return header


def home_page_App():
    return html.Div([
        get_header(),
        html.Div([
            html.Div([
            ],
                className='col-1'
            ),
            html.Div([
                dcc.Dropdown(
                    id='region',
                    options=[
                        {'label':'All', 'value':'All'},
                        {'label':'CO', 'value':'CO'},
                    ]
                )
            ],
                className='col-2'
            ),
            
        ],
            className='row'
        ),
        html.Div([
            html.Div([
            ],
                className='col-1'
            ),
            html.Div([
                dcc.Graph('site-map')
            ],
                className='col-10'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                )
            ])
        ],
            className='row'
        ),
    ])

    app.layout = home_page_App