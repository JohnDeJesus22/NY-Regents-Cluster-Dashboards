# dash test

#import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth
from plotly.graph_objs import *
import os
import pandas as pd
from RegentsAppMarkdown import *
import json
#import base64 #for future pics of questions

#login info
USERNAME_PASSWORD_PAIR=[['username','secretpassword']]

#initiate app
app=dash.Dash()

#authorization
auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIR)

#change directory and get data with necessary columns
os.chdir('D:\\MathRegentsDataFiles')
geo=pd.read_csv('PreppedGeoQuestionBreakdown.csv',encoding='latin1',usecols=['ClusterTitle',
                                        'Cluster', 'DateFixed','Regents Date', 'Type'])

'''
below done for improving display of dropdown options for bar charts
geo['Regents Date']=pd.to_datetime(geo['Regents Date'])#,format='%m/%d/%Y')

def month_year(date):
    month=date.strftime("%b")
    year=date.year
    return str(month)+' '+str(year) 

geo['DateFixed']=geo['Regents Date'].apply(month_year)


geo.to_csv('PreppedGeoQuestionBreakdown.csv',index=False)
'''

#exam options for first bar chart
exam_options=[{'label':'All Exams','value':'All Exams'}]
for exam in sorted(geo['DateFixed'].unique()):
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
                html.H1(children='Geometry Regents Cluster Analysis Dashboard',
                        style={'textAlign':'center','font-style':'sans-serif'}),
                      
                #subtitle description
                html.H3(children=dcc.Markdown(gen_description),
                style={'textAlign':'center','font-style':'sans-serif'}),
                        
                #divider
                html.Div(id='border_one',style={'border':'2px blue solid'}),
                         
                #instructions for nested bar chart        
                html.Div(children=dcc.Markdown(nested_description),
                         style={'font-style':'sans-serif',
                         'width':'50%','display':'table-cell'}),
    
                #dropdown for double bar chart
                html.Div(children=[dcc.Dropdown(id='exam_selector',
                        options=exam_options,
                        value='All Exams',
                        clearable=False)],
                    style={'width':'40%','display':'table-cell'}),
                
                #Double Bar of question types
                html.Div(dcc.Graph(id='double bar')),
                
                #reveal skipped clusters
                html.Div(id='excluded-double',
                         style={'font-style':'sans-serif',
                         'width':'40%','display':'inline-block',
                         'color':'blue','border': '5px solid red',
                         'font-size':'110%','textAlign':'center'}),
                
                #divider
                html.Div(id='border_one',style={'border':'2px red solid'}),
                
                #instructions for percentage bar chart
                html.Div(dcc.Markdown(percentage_description),
                         style={'font-style':'sans-serif',
                         'width':'50%','display':'table-cell'}),
    
                #dropdown for percentage bar
                html.Div(children=[dcc.Dropdown(id='exam_selector_two',
                        options=exam_options,
                        value='All Exams',
                        clearable=False)],
                    style={'width':'40%','display':'table-cell'}),
                             
                #Percentage Bar Chart
                html.Div(dcc.Graph(id='overall')),
                
                html.Div(id='excluded-percent',
                         style={'font-style':'sans-serif',
                         'width':'40%','display':'inline-block',
                         'color':'blue','border': '5px solid red',
                         'font-size':'110%','textAlign':'center'}),
                
                
                #divider
                html.Div(id='border_one',style={'border':'2px red solid'}),
                
                #line chart dropdown
                html.Div(children=[dcc.Markdown(time_series_description),
                        dcc.Dropdown(id='cluster_selector',
                             options=clusters,
                             value=['G-CO.C'],
                             multi=True,
                             placeholder='Select Cluster(s)')]),
                             
                #line chart 
                html.Div(children=[dcc.Graph(id='line chart')],
                                   style={'width':'60%','display':'table-cell'}),
                
                #for cluster bar chart correlated with time series     
                html.Div(children=[dcc.Graph(id='bar_type_for_time_series')],
                                   style={'width':'30%','display':'table-cell'}),
                
                #divider
                html.Div(id='border_one',style={'border':'2px red solid'}),

                #info for links
                html.Div(dcc.Markdown(additional_info))
                
                ],                        
style={'backgroundColor':'#EAEAD2'}
)

#filter for nested bar chart
@app.callback(Output('double bar','figure'),
              [Input('exam_selector','value')])
def update_double_bar(selected_exam):
    #create df grouped by question type,cluster, and exam
    type_group=geo.groupby(['Type', 'Cluster', 'DateFixed']).size().reset_index(name='counts')
    
    #sort clusters alphabetically
    type_group=type_group.sort_values(by=['Cluster'])
    
    if selected_exam =='All Exams':
        #get overall totals of clusters in each type
        type_group['QTypeTotals']=type_group.groupby(['Type',
                  'Cluster'])['counts'].transform('sum')
        
        #create trace
        stack_trace=[
                {'x':type_group['Cluster'][type_group.Type=='MC'],
                'y':type_group['QTypeTotals'][type_group.Type=='MC'],
                'type':'bar',
                'name':'MC'},
                 {'x':type_group['Cluster'][type_group.Type=='CR'],
                  'y':type_group['QTypeTotals'][type_group.Type=='CR'],
                  'type':'bar',
                  'name':'CR'}
                 ]
        
        return {'data':stack_trace,
                'layout':{'plot_bgcolor':'#EAEAD2',
                                    'paper_bgcolor':'#EAEAD2',
                                    'hovermode':'closest',
                                     'title':'<b>Clusters By Question Type</b>',
                                     'xaxis':{'title': '<b>Cluster Codes</b>'},
                                     'yaxis':{'title': '<b>Total Number of Questions</b>'}}}
    else:
        type_group=type_group[type_group['DateFixed']==selected_exam]
        
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
                          'title':'<b>Clusters by Question Type for </b>'+ selected_exam,
                          'xaxis':{'title': '<b>Cluster Codes</b>'},
                          'yaxis':{'title': '<b>Total Number of Questions</b>'}}}

#function to reveal excluded clusters from selected exam date.
@app.callback(Output('excluded-double','children'),
              [Input('exam_selector','value')])
def excluded_clusters_double(exam_date):
    if exam_date !='All Exams':
        clusters=geo.Cluster.unique().tolist()
        filtered_by_date=geo[geo.DateFixed==exam_date]
        chosen_date_clusters=filtered_by_date.Cluster.unique().tolist()
        
        if len(clusters)==len(chosen_date_clusters):
            return 'All clusters assessed in {}.'.format(exam_date)
        
        else:
            missing_clusters=[]
            for i in clusters:
                if i not in chosen_date_clusters:
                    missing_clusters.append(i)
                    return 'The following clusters were not assessed in {}: {}'.format(exam_date,
                                                                        tuple(missing_clusters))

#filter for simple percentage bar chart
@app.callback(Output('overall','figure'),
              [Input('exam_selector_two','value')])
def update_simple_bar(selected_exam):
    
    if selected_exam !='All Exams':
        #group data by DateFixed
        date_group=geo.groupby(['DateFixed','Cluster']).size().reset_index(name='count')
        
        #filter exam by selected date
        sel_exam=date_group[date_group['DateFixed']==selected_exam]
        
        #create percentage column
        sel_exam['count_pct']=sel_exam['count'].apply(lambda x: x/sum(sel_exam['count']))
        
        #create trace
        new_trace=[{'x': sel_exam['Cluster'],
                    'y':sel_exam['count_pct'],
                    'type':'bar'}]
        
        return {'data': new_trace,
                'layout':{
                        'plot_bgcolor':'#EAEAD2',
                        'paper_bgcolor':'#EAEAD2',
                        'hovermode':'closest',
                        'title':'<b>Cluster Percentage Bar Chart for </b>'+ selected_exam,
                        'xaxis':{'title': '<b>Cluster Codes</b>'},
                        'yaxis':{'title': '<b>Percentage of Exam</b>',
                                 'tickformat':'%'}}}
    else:
        #get freqency
        geo['freq']=geo.groupby('Cluster')['Cluster'].transform('count')
        
        #drop duplicates
        new_geo=geo.drop_duplicates(subset=['Cluster'],keep='first')
        
        #percentage of exam column
        new_geo['freq_pct']=new_geo['freq'].apply(lambda x: x/sum(new_geo['freq']))
        
        #create trace
        new_trace=[{'x': new_geo['Cluster'],
                    'y':new_geo['freq_pct'],
                    'type':'bar'}]
        return {'data': new_trace,
                'layout':{
                        'plot_bgcolor':'#EAEAD2',
                        'paper_bgcolor':'#EAEAD2',
                        'hovermode':'closest',
                        'title':'<b>Cluster Overall Percentage Bar Chart</b>',
                        'xaxis':{'title': '<b>Cluster Codes</b>'},
                        'yaxis':{'title': '<b>Percentage of All Exams</b>',
                                 'tickformat':'%'}}}
    
#function to reveal excluded clusters from selected exam date.
@app.callback(Output('excluded-percent','children'),
              [Input('exam_selector_two','value')])
def excluded_clusters_percent(exam_date):
    if exam_date !='All Exams':
        clusters=geo.Cluster.unique().tolist()
        filtered_by_date=geo[geo.DateFixed==exam_date]
        chosen_date_clusters=filtered_by_date.Cluster.unique().tolist()
        
        if len(clusters)==len(chosen_date_clusters):
            return 'All clusters assessed in {}.'.format(exam_date)
        
        else:
            missing_clusters=[]
            for i in clusters:
                if i not in chosen_date_clusters:
                    missing_clusters.append(i)
                    return 'The following clusters were not assessed in {}: {}'.format(exam_date,
                                                                        tuple(missing_clusters))


      
#line chart filter
@app.callback(Output('line chart','figure'),
              [Input('cluster_selector','value')])
def update_cluster_timeSeries(cluster_list):
    traces=[]
    for cluster in cluster_list:
        #data only for selected cluster and get freq by exam date
        sel_cluster=geo[geo['Cluster']==cluster]
        sel_cluster['freq']=sel_cluster.groupby('Regents Date')['Regents Date'].transform('count')
    
        #convert Regents Date column to date time
        sel_cluster['Regents Date']=pd.to_datetime(sel_cluster['Regents Date'])
        
        #drop duplicate dates
        sel_cluster=sel_cluster.drop_duplicates(subset=['Regents Date','Type'],keep='first')
    
        #sort by date
        sel_cluster=sel_cluster.sort_values(by=['Regents Date'])
        
        #hovertext
        sel_cluster['hovertext']=sel_cluster.apply(lambda x:
          '<b>{} {}</b><br> {} questions'.format(x['Regents Date'].strftime("%b"),
                   x['Regents Date'].year, x['freq']),axis=1)
        
        #create traces
        traces.append({'x': sel_cluster['Regents Date'],
                    'y':sel_cluster['freq'],
                    'type':'scatter',
                    'text':sel_cluster['hovertext'],
                    'hoverinfo':'text+name',
                    'name':cluster,
                    'mode':'lines+markers'})

    return {'data': traces,
            'layout':{'title':'<b>Cluster Line Chart </b>',
                                            'hovermode':'closest',
                                           'xaxis':{'title': '<b>Regents Exam Date</b>'},
                                     'yaxis':{'title': '<b>Number of Questions</b>',
                                              'range':[0,6.75]}
                                     }}


#function for bar chart corresponding to line chart
#6/9/18 need to fix to correctly incorporate exam date and for when exam date==None
@app.callback(Output('bar_type_for_time_series','figure'),
              [Input('line chart','clickData'),
              Input('cluster_selector','value')])
def time_series_click_bar(clickData,cluster_list):
    
    
    if clickData==None:
        filtered=geo[geo.Cluster.isin(cluster_list)]
        counts=filtered.Type.value_counts()
        
        trace=[{'type':'bar',
           'x': counts.index.values.tolist(),
            'y':counts.tolist(),
            'hoverinfo':'y'}]
    
    
        return {'data':trace,
            'layout':{'title':'<b>MC/CR Breakdown of<br>Selected Clusters</b>',
                    'xaxis':{'title':'Question Type'},
                      'yaxis':{'title':'Number of Questions'},
                      'hovermode':'closest'}}
    
    else:
        exam_date=clickData["points"][0]["x"]
        filtered=geo[(geo['Regents Date']==exam_date) & (geo.Cluster==cluster_list[0])]
        
        counts=filtered.Type.value_counts()
        trace=[{'type':'bar',
           'x': counts.index.values.tolist(),
            'y':counts.tolist(),
            'hoverinfo':'y'}]
    
    
        return {'data':trace,
            'layout':{'title':'<b>MC/CR Breakdown of<br>Selected Clusters</b>',
                    'xaxis':{'title':'Question Type'},
                      'yaxis':{'title':'Number of Questions'},
                      'hovermode':'closest'}}

#run when called in terminal
if __name__=='__main__':
    app.run_server()
