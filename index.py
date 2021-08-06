from app import app
from app import server
from homepage import home_page_App
import dash_core_components as dcc
import dash_html_components as html
import dash
# from apps.revenue import revenue_App
# from apps.pc_rev import pcrev_App
# from apps.pl_rev import plrev_App
# from apps.biz import biz_App
from os import environ
from dotenv import load_dotenv
import callbacks

load_dotenv()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    return home_page_App()

if __name__ == '__main__':
    app.run_server(port=8000, debug=True)