import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
from datetime import datetime as dt
import dash_bootstrap_components as dbc
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os


server = Flask(__name__)
app = dash.Dash(__name__)
# app.config['suppress_callback_exceptions']=True
app.config.suppress_callback_exceptions = True
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost/sites"

db = SQLAlchemy(app.server)

class Site(db.Model):
    __tablename__ = 'sites'

    site_name = db.Column(db.String(50), nullable=False, primary_key=True)
    lat = db.Column(db.Integer, nullable=False)
    lon = db.Column(db.Integer, nullable=False)

    def __init__(self, site_name, lat, lon):
        self.Site_name = site_name
        self.Lat = lat
        self.Lon = lon



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
        # html.Div([
        #         dcc.Link(
        #             html.H2(children='Home', style={'color':'black'}),
        #             href='/homepage'
        #         )
        #     ],
        #         style = {'padding-top' : '2.5%'}
        #     ),
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
                    id='adding-rows-name',
                    placeholder='Enter a column name...',
                    value='',
                    style={'padding': 10}
                ),
                html.Button('Add Row', id='editing-rows-button', n_clicks=0),
                html.Button('Save to PostgreSQL', id='save_to_postgres', n_clicks=0),
                html.Button('Add Column', id='adding-columns-button', n_clicks=0),
            ],
                className='col-6'
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
        html.Div(id='postgres_datatable'),
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
        dcc.Interval(id='interval_pg', interval=86400000*7, n_intervals=0),  # activated once/week or when page refreshed
        html.Div(id='placeholder', children=[]),
        dcc.Store(id="store", data=0),
        dcc.Interval(id='interval', interval=1000),
    ])
@app.callback(
    Output('site-map', 'figure'),
    Input('editing-rows-button', 'n_clicks'))
def update_site_map(n):
    print(n)
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

@app.callback(Output('postgres_datatable', 'children'),
              [Input('interval_pg', 'n_intervals')])
def populate_datatable(n_intervals):
    df = pd.read_sql_table('sites', con=db.engine)
    return [
        dash_table.DataTable(
            id='our-table',
            columns=[{
                         'name': str(x),
                         'id': str(x),
                         'deletable': False,
                     } if x == 'Sales' or x == 'Phone'
                     else {
                'name': str(x),
                'id': str(x),
                'deletable': True,
            }
                     for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'right'
                } for c in ['Price', 'Sales']
            ]

        ),
    ]


if __name__ == '__main__':
    app.run_server(port=8000, debug=True)