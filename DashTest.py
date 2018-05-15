# dash test

#import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.graph_objs import *
import os
import pandas as pd
import numpy as np
import datetime

#initiate app
app=dash.Dash()

#change directory and get data
os.chdir('D:\\MathRegentsDataFiles')
geo=pd.read_csv('PreppedGeoQuestionBreakdown.csv',encoding='latin1')

#create df grouped by question type and cluster.
type_group=geo.groupby(['Type', 'Cluster']).size().reset_index(name='counts')

#create freq column for clusters
geo['freq']=geo.groupby('Cluster')['Cluster'].transform('count')

#sort data by cluster alphabetically
geo=geo.sort_values(by=['Cluster'])

#test filter for line chart on a single cluster (need to work on this to get correct filter
#and display line chart properly 5/9/18)
gcoc=geo[geo.Cluster=='G-CO.C']
gcoc['freq']=gcoc.groupby('Regents Date')['Regents Date'].transform('count')

#convert Regents Date column to date time
gcoc['Regents Date']=pd.to_datetime(gcoc['Regents Date'],format='%m/%d/%Y')

#drop duplicate dates
gcoc=gcoc.drop_duplicates(subset=['Regents Date'],keep='first')

#sort by date
gcoc=gcoc.sort_values(by=['Regents Date'])

#exam options for first bar chart
#geo['Regents Date']=pd.to_datetime(geo['Regents Date'],format='%m/%d/%Y')
exam_options=[]
for exam in sorted(geo['Regents Date'].unique()):
    exam_options.append({'label':exam,'value':exam})

clusters=[]
for cluster in sorted(geo['Cluster'].unique()):
    clusters.append({'label':cluster,'value':cluster})

#create app
app.layout=html.Div(children=[
                #main title
                html.H1(children='First Dash App',style={'textAlign':'center'}),
                #subtitle
                html.Div(children='First Test Chart of Cluster Analysis',
                style={'textAlign':'center'}),
                #dropdown for simple bar chart
                dcc.Dropdown(id='exam_selector',
                        options=exam_options,
                        value=geo['Regents Date'].min()),
                #Bar Chart
                dcc.Graph(id='overall',
                          figure={'data':[
                                  {'x': geo['Cluster'],
                                    'y':geo['freq'],
                                    'type':'bar'}],
                                  'layout':{
                                    'plot_bgcolor':'#EAEAD2',
                                    'paper_bgcolor':'#EAEAD2',
                                    'hovermode':'closest',
                                     'title':'<b>Cluster Bar Chart</b>',
                                     'xaxis':{'title': '<b>Cluster Codes</b>'},
                                     'yaxis':{'title': '<b>Total Number of Questions</b>'}}
                                      }),
                #line chart dropdown
                dcc.Dropdown(id='cluster_selector',
                             options=clusters,
                             value='G-CO.C'),
                #line chart 
                dcc.Graph(id='line chart',
                          figure={'data':[
                                  {'x':gcoc['Regents Date'],
                                   'y':gcoc['freq'],
                                   'type':'scatter',
                                   'mode':'lines+markers'}],
                                  'layout':{'title':'<b>G-CO.C Line chart</b>',
                                            'hovermode':'closest',
                                           'xaxis':{'title': '<b>Regents Exam Date</b>'},
                                     'yaxis':{'title': '<b>Number of Questions</b>'}
                                     }}),
                dcc.Graph(id='double bar',
                          figure={'data':[
                                  {'x':type_group['Cluster'][type_group.Type=='MC'],
                                  'y':type_group['counts'][type_group.Type=='MC'],
                                  'type':'bar',
                                  'name':'MC'},
                                   {'x':type_group['Cluster'][type_group.Type=='CR'],
                                  'y':type_group['counts'][type_group.Type=='CR'],
                                  'type':'bar',
                                  'name':'CR'}
                                    ],
                                  'layout':{
                                'barmode':'stack',
                                'plot_bgcolor':'#EAEAD2',
                                    'paper_bgcolor':'#EAEAD2',
                                    'hovermode':'closest',
                                     'title':'<b>Cluster Bar Chart by type</b>',
                                     'xaxis':{'title': '<b>Cluster Codes</b>'},
                                     'yaxis':{'title': '<b>Total Number of Questions</b>'}}})],
style={'backgroundColor':'#EAEAD2'}
)
 
#only seems to work if date format is unchanged. not sure why it isn't being picked up
#here. Supposedly the label selected in drop down is inputted into the function below.

@app.callback(Output('overall','figure'),
              [Input('exam_selector','value')])
def update_simple_bar(selected_exam):

    #data only for selected exam
    filtered_exam=geo[geo['Regents Date']==selected_exam]
    
    filtered_exam['freq']=filtered_exam.groupby('Cluster')['Cluster'].transform('count')
    
    new_trace=[{'x': filtered_exam['Cluster'],
                'y':filtered_exam['freq'],
                'type':'bar'}]
    
    return {'data': new_trace,
            'layout':{
                    'plot_bgcolor':'#EAEAD2',
                    'paper_bgcolor':'#EAEAD2',
                    'hovermode':'closest',
                    'title':'<b>Cluster Bar Chart for </b>'+ selected_exam,
                    'xaxis':{'title': '<b>Cluster Codes</b>'},
                    'yaxis':{'title': '<b>Total Number of Questions</b>'}}}


#line chart filter
@app.callback(Output('line chart','figure'),
              [Input('cluster_selector','value')])
def update_cluster_timeSeries(cluster):
    
    #data only for selected cluster
    sel_cluster=geo[geo.Cluster==cluster]
    sel_cluster['freq']=sel_cluster.groupby('Regents Date')['Regents Date'].transform('count')

    #convert Regents Date column to date time
    sel_cluster['Regents Date']=pd.to_datetime(sel_cluster['Regents Date'],format='%m/%d/%Y')
    
    #drop duplicate dates
    sel_cluster=sel_cluster.drop_duplicates(subset=['Regents Date'],keep='first')

    #sort by date
    sel_cluster=sel_cluster.sort_values(by=['Regents Date'])
    
    new_trace=[{'x': sel_cluster['Regents Date'],
                'y':sel_cluster['freq'],
                'type':'scatter',
                'mode':'lines+markers'}]
    
    return {'data': new_trace,
            'layout':{'title':'<b>Line Chart of </b>'+ cluster,
                                            'hovermode':'closest',
                                           'xaxis':{'title': '<b>Regents Exam Date</b>'},
                                     'yaxis':{'title': '<b>Number of Questions</b>'}
                                     }}
    
#run when called in terminal
if __name__=='__main__':
    app.run_server()