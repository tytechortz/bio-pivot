import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
from datetime import datetime as dt
import dash_bootstrap_components as dbc
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


# from data import df_revenue, df_pc, df_rev
server = Flask(__name__)
app = dash.Dash(__name__)
# app.config['suppress_callback_exceptions']=True
app.config.suppress_callback_exceptions = True
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost/sites"

db = SQLAlchemy(app.server)

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

app.layout = html.Div([
        get_header(),
        html.Div([
            html.Div([
            ],
                className='col-1'
            ),
            html.Div([
                dcc.Input(
                    id='add-site',
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
                    multiple=True
                )
            ])
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.Div(id='output-data-upload'),
            ],
                className='col-6'
            ),
        ],
            className='row'
        ),
    ])



if __name__ == '__main__':
    app.run_server(port=8000, debug=True)