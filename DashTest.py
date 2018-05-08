# dash test

#import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import numpy as np

app=dash.Dash()

os.chdir('D:\\MathRegentsDataFiles')
geo=pd.read_csv('PreppedGeoQuestionBreakdown.csv',encoding='latin1')
geo['freq']=geo.groupby('Cluster')['Cluster'].transform('count')
geo=geo.sort_values(by=['Cluster'])
app.layout=html.Div(children=[
                html.H1('First Dash App'),
                html.Div('First Test Chart of Cluster Analysis'),
                dcc.Graph(id='example',
                          figure={'data':[
                                  {'x': geo['Cluster'],
                                    'y':geo['freq'],
                                    'type':'bar'}],
                                  'layout':{
                                     'title':'Cluster Bar Chart',
                                     'xaxis':{'title': 'Cluster Codes'},
                                     'yaxis':{'title': 'Total Number of Questions'}}
                                      })])

if __name__=='__main__':
    app.run_server()