# connection for app pages

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from RegentsApp import app
import RegentsAppFunctions, RegentsAppMarkdown, Alg1CC, Alg2CC, GeometryCC


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Alg1CC':
         return Alg1CC.layout
    elif pathname == '/GeometryCC':
         return GeometryCC.layout
    elif pathname == '/Alg2CC':
         return Alg2CC.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server()

