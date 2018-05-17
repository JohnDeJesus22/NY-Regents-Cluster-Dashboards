# dash test

#import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.graph_objs import *
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

#initiate app
app=dash.Dash()

#change directory and get data
os.chdir('D:\\MathRegentsDataFiles')
geo=pd.read_csv('PreppedGeoQuestionBreakdown.csv',encoding='latin1')

#exam options for first bar chart
#geo['Regents Date']=pd.to_datetime(geo['Regents Date'],format='%m/%d/%Y')
exam_options=[{'label':'All Exams','value':'All Exams'}]
for exam in sorted(geo['Regents Date'].unique()):
    exam_options.append({'label':exam,'value':exam})

#options for cluster dropdown
clusters=[]
geo=geo.sort_values(by=['Cluster'])
cluster_dict=dict(zip(geo['Cluster'].unique(),geo['ClusterTitle'].unique()))
for cluster in cluster_dict:
    clusters.append({'label':cluster+'-'+ cluster_dict.get(cluster),'value':cluster})

#create app
app.layout=html.Div(children=[
                #main title
                html.H1(children='Geometry Regents Cluster Dashboard',
                        style={'textAlign':'center'}),
                      
                #subtitle
                html.Div(children='First Test Dashboard of Geometry Regents Cluster Analysis',
                style={'textAlign':'center'}),
                         
                #dropdown for simple bar chart
                dcc.Dropdown(id='exam_selector',
                        options=exam_options,
                        value='All Exams'),
                
                #DoubleBar of question types
                dcc.Graph(id='double bar'),
                             
                #Bar Chart
                dcc.Graph(id='overall'),
                
                #line chart dropdown
                dcc.Dropdown(id='cluster_selector',
                             options=clusters,
                             value='G-CO.C'),
                             
                #line chart 
                dcc.Graph(id='line chart'),
                
                ],
style={'backgroundColor':'#EAEAD2'}
)
 
#only seems to work if date format is unchanged. not sure why it isn't being picked up
#here. Supposedly the label selected in drop down is inputted into the function below.
@app.callback(Output('overall','figure'),
              [Input('exam_selector','value')])
def update_simple_bar(selected_exam):

    if selected_exam != 'All Exams':
        #data only for selected exam
        filtered_exam=geo[geo['Regents Date']==selected_exam]
        
        #question total
        filtered_exam['freq']=filtered_exam.groupby('Cluster')['Cluster'].transform('count')
        
        #sort clusters alphabetically
        filtered_exam=filtered_exam.sort_values(by=['Cluster'])
        
        #create trace
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
    else:
        #get question totals
        geo['freq']=geo.groupby('Cluster')['Cluster'].transform('count')

        #sort data by cluster alphabetically
        clusters_sorted=geo.sort_values(by=['Cluster'])
        
        #get overall trace
        all_exams_trace=[{'x': clusters_sorted['Cluster'],
                    'y':clusters_sorted['freq'],
                    'type':'bar'}]
            
        return {'data': all_exams_trace,
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
    
    #data only for selected cluster and get freq by exam date
    sel_cluster=geo[geo['Cluster']==cluster]
    sel_cluster['freq']=sel_cluster.groupby('Regents Date')['Regents Date'].transform('count')

    #convert Regents Date column to date time
    sel_cluster['Regents Date']=pd.to_datetime(sel_cluster['Regents Date'],format='%m/%d/%Y')
    
    #drop duplicate dates
    sel_cluster=sel_cluster.drop_duplicates(subset=['Regents Date'],keep='first')

    #sort by date
    sel_cluster=sel_cluster.sort_values(by=['Regents Date'])
    
    #create trace
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
    
@app.callback(Output('double bar','figure'),
              [Input('exam_selector','value')])
def update_double_bar(selected_exam):
    #create df grouped by question type,cluster, and exam
    type_group=geo.groupby(['Type', 'Cluster', 'Regents Date']).size().reset_index(name='counts')
    
    #sort clusters alphabetically
    type_group=type_group.sort_values(by=['Cluster'])
    
    if selected_exam =='All Exams':
        stack_trace=[
                {'x':type_group['Cluster'][type_group.Type=='MC'],
                'y':type_group['counts'][type_group.Type=='MC'],
                'type':'bar',
                'name':'MC'},
                 {'x':type_group['Cluster'][type_group.Type=='CR'],
                  'y':type_group['counts'][type_group.Type=='CR'],
                  'type':'bar',
                  'name':'CR'}
                 ]
        return {'data':stack_trace,
                'layout':{'plot_bgcolor':'#EAEAD2',
                                    'paper_bgcolor':'#EAEAD2',
                                    'hovermode':'closest',
                                     'title':'<b>Cluster Bar Chart by type</b>',
                                     'xaxis':{'title': '<b>Cluster Codes</b>'},
                                     'yaxis':{'title': '<b>Total Number of Questions</b>'}}}
    else:
        type_group=type_group[type_group['Regents Date']==selected_exam]
        
        filtered_stack_trace=[
                {'x':type_group['Cluster'][type_group.Type=='MC'],
                'y':type_group['counts'][type_group.Type=='MC'],
                'type':'bar',
                'name':'MC'},
                 {'x':type_group['Cluster'][type_group.Type=='CR'],
                  'y':type_group['counts'][type_group.Type=='CR'],
                  'type':'bar',
                  'name':'CR'}
                 ]
        return {'data':filtered_stack_trace,
                'layout':{'plot_bgcolor':'#EAEAD2',
                                    'paper_bgcolor':'#EAEAD2',
                                    'hovermode':'closest',
                                     'title':'<b>Cluster Bar Chart by type</b>',
                                     'xaxis':{'title': '<b>Cluster Codes</b>'},
                                     'yaxis':{'title': '<b>Total Number of Questions</b>'}}}
        
        
#run when called in terminal
if __name__=='__main__':
    app.run_server()
