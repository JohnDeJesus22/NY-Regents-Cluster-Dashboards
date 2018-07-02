# Algebra 1 CC Dashboard

# import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import RegentsAppFunctions as func
from RegentsAppMarkdown import *
from dash.dependencies import Input, Output
# import base64 #for future pics of questions

# initiate app
app = dash.Dash()

# load data from postgres
alg_one = func.load_postgres('Alg1CC')

# convert dates to string data type
alg_one['Regents Date'] = alg_one['Regents Date'].astype('str')

# exam options for first bar chart
exam_options = [{'label': 'All Exams', 'value': 'All Exams'}]
for exam in sorted(alg_one['DateFixed'].unique()):
    exam_options.append({'label': exam, 'value': exam})

# options for cluster dropdown
clusters = []
alg_one = alg_one.sort_values(by=['Cluster'])
cluster_dict = dict(zip(alg_one['Cluster'].unique(), alg_one['ClusterTitle'].unique()))
for cluster in cluster_dict:
    clusters.append({'label': cluster + '-' + cluster_dict.get(cluster), 'value': cluster})

# create app
app.layout=html.Div(children=[
                # main title
                html.H1(children='Algebra 1 CC Regents Cluster Analysis Dashboard',
                        style={'textAlign': 'center', 'fontFamily': 'Arial'}),
                      
                # subtitle description
                html.H3(children=dcc.Markdown(alg_gen_description),
                        style={'textAlign': 'center', 'fontFamily': 'Arial'}),
                        
                # divider
                html.Div(id='border_one', style={'border': '2px blue solid'}),
                         
                # instructions for nested bar chart
                html.Div(children=dcc.Markdown(nested_description),
                         style={'fontFamily': 'Arial',
                         'width': '50%', 'display': 'table-cell'}),
    
                # dropdown for double bar chart
                html.Div(children=[dcc.Dropdown(id='exam_selector',
                         options=exam_options,
                         value='All Exams',
                         clearable=False)],
                         style={'width': '40%', 'display': 'table-cell'}),
                
                # Double Bar of question types
                html.Div(dcc.Graph(id='double bar')),
                
                # reveal skipped clusters
                html.Div(id='excluded-double',
                         style={'fontFamily': 'Arial',
                                'width': '40%', 'display': 'inline-block',
                                'color': 'blue', 'border': '5px solid red',
                                'font-size': '110%', 'textAlign': 'center'}),
                
                # divider
                html.Div(id='border_one', style={'border': '2px red solid'}),
                
                # instructions for percentage bar chart
                html.Div(dcc.Markdown(percentage_description),
                         style={'fontFamily': 'Arial',
                         'width': '50%', 'display': 'table-cell'}),
    
                # dropdown for percentage bar
                html.Div(children=[dcc.Dropdown(id='exam_selector_two',
                         options=exam_options,
                         value='All Exams',
                         clearable=False)],
                         style={'width': '40%', 'display': 'table-cell'}),
                             
                # Percentage Bar Chart
                html.Div(dcc.Graph(id='overall')),
                
                html.Div(id='excluded-percent',
                         style={'fontFamily': 'Arial',
                                'width': '40%', 'display': 'inline-block',
                                'color': 'blue', 'border': '5px solid red',
                                'font-size': '110%', 'textAlign': 'center'}),
                
                
                # divider
                html.Div(id='border_one', style={'border': '2px red solid'}),
                
                # line chart dropdown
                html.Div(children=[dcc.Markdown(time_series_description),
                                   dcc.Dropdown(id='cluster_selector',
                                   options=clusters,
                                   value=['G-CO.C'],
                             multi=True,
                             placeholder='Select Cluster(s)')],
                         style={'fontFamily': 'Arial'}),
                             
                # line chart
                html.Div(children=[dcc.Graph(id='line chart')],
                         style={'width': '60%', 'display': 'table-cell'}),
                
                # for cluster bar chart correlated with time series
                html.Div(children=[dcc.Graph(id='bar_type_for_time_series')],
                         style={'width': '30%', 'display': 'table-cell'}),
                
                # divider
                html.Div(id='border_one',style={'border': '2px red solid'}),

                # info for links
                html.Div(dcc.Markdown(alg_additional_info), style={'fontFamily': 'Arial'})
                
                ],                        
                style={'backgroundColor': '#EAEAD2'}
)


# filter for nested bar chart
@app.callback(Output('double bar', 'figure'),
              [Input('exam_selector', 'value')])
def update_double_bar(selected_exam):
    return func.nested_bar(alg_one, selected_exam)


# function to reveal excluded clusters from selected exam date.
@app.callback(Output('excluded-double', 'children'),
              [Input('exam_selector', 'value')])
def excluded_clusters_double(exam_date):
    return func.reveal_missing_clusters(alg_one, exam_date)


# filter for simple percentage bar chart
@app.callback(Output('overall', 'figure'),
              [Input('exam_selector_two', 'value')])
def update_simple_bar(selected_exam):
    return func.percentage_bar(alg_one, selected_exam)


# function to reveal excluded clusters from selected exam date.
@app.callback(Output('excluded-percent', 'children'),
              [Input('exam_selector_two', 'value')])
def excluded_clusters_percent(exam_date):
    return func.reveal_missing_clusters(alg_one, exam_date)


# line chart filter
@app.callback(Output('line chart', 'figure'),
              [Input('cluster_selector', 'value')])
def update_cluster_timeseries(cluster_list):
    return func.cluster_time_series(alg_one, cluster_list)


# function for bar chart corresponding to line chart
@app.callback(Output('bar_type_for_time_series', 'figure'),
              [Input('line chart', 'clickData'),
              Input('cluster_selector', 'value')])
def time_series_click_bar(clickData, cluster_list):
    return func.time_series_bar(alg_one, clickData, cluster_list)


# run when called in terminal
if __name__ == '__main__':
    app.run_server()
