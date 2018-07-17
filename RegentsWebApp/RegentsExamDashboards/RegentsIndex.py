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

index_page = html.Div([
    dcc.Link('Algebra 1 CC Page', href='/Alg1CC'),
    html.Br(),
    dcc.Link('Geometry CC Page', href='/GeometryCC'),
    html.Br(),
    dcc.Link('Algebra 2 CC Page', href='/Alg2CC'),
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
        return index_page

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server()

