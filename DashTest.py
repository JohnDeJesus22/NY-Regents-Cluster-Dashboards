# dash test

#import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *
import os
import pandas as pd
import numpy as np

#initiate app
app=dash.Dash()

#change directory and get data
os.chdir('D:\\MathRegentsDataFiles')
geo=pd.read_csv('PreppedGeoQuestionBreakdown.csv',encoding='latin1')

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

markdown_text='''
                Hey there everyone. I am testing out some `markdown`. Check out more of what
                I do at my [blog](http://www.jddata22.com/).
                             '''
#create app
app.layout=html.Div(children=[
                #main title
                html.H1(children='First Dash App',style={'textAlign':'center'}),
                #subtitle
                html.Div(children='First Test Chart of Cluster Analysis',
                style={'textAlign':'center'}),
                #Bar Chart
                dcc.Graph(id='example',
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
                #markdown test
                dcc.Markdown(children=markdown_text),
                #drop down test. value=default value displayed
                dcc.Dropdown(
    options=[
        {'label': 'Geometry Basics', 'value': 'G-CO.C'},
        {'label': 'Basic Trigonometry', 'value': 'SRT-C'},
        {'label': 'Modeling with Geometry', 'value': 'G-gMD.B'}
    ],value='Geometry Basics'),
                #line chart 
                dcc.Graph(id='line chart',
                          figure={'data':[
                                  {'x':gcoc['Regents Date'],
                                   'y':gcoc['freq'],
                                   'type':'scatter',
                                   'mode':'lines'}],
                                  'layout':{'title':'<b>G-CO.C Line chart</b>',
                                            'hovermode':'closest',
                                           'xaxis':{'title': '<b>Regents Exam Date</b>'},
                                     'yaxis':{'title': '<b>Number of Questions</b>'}
                                     }})],
style={'backgroundColor':'#EAEAD2'}
)

#run when called in terminal
if __name__=='__main__':
    app.run_server()