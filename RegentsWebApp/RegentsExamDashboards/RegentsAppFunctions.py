# Regents Dashboard Functions

#import libraries
import pandas as pd
import os

def load_data(pathname,file):
    os.chdir(pathname)
    df=pd.read_csv(file,encoding='latin1',usecols=['ClusterTitle',
                                            'Cluster', 'DateFixed','Regents Date', 'Type'])
    
    return df

#MC/CR Nested Bar Function
def nested_bar(df,selected_exam):
    #create df grouped by question type,cluster, and exam
    type_group=df.groupby(['Type', 'Cluster', 'DateFixed']).size().reset_index(name='counts')
    
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
        

#Missing CLusters Reveal
def reveal_missing_clusters(df,exam_date):
    if exam_date !='All Exams':
        filtered_by_date=df[df.DateFixed==exam_date]
        
        if len(df.Cluster.unique())==len(filtered_by_date.Cluster.unique()):
            return 'All clusters assessed in {}.'.format(exam_date)
        
        else:
            missing_clusters=[]
            for i in df.Cluster.unique().tolist():
                if i not in filtered_by_date.Cluster.unique().tolist():
                    missing_clusters.append(i)
                    return 'The following clusters were not assessed in {}: {}'.format(exam_date,
                                                                        tuple(missing_clusters))
#percentage bar chart         
def percentage_bar(df,selected_exam):
    
    if selected_exam !='All Exams':
        #group data by DateFixed
        date_group=df.groupby(['DateFixed','Cluster']).size().reset_index(name='count')
        
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
        df['freq']=df.groupby('Cluster')['Cluster'].transform('count')
        
        #drop duplicates
        new_df=df.drop_duplicates(subset=['Cluster'],keep='first')
        
        #percentage of exam column
        new_df['freq_pct']=new_df['freq'].apply(lambda x: x/sum(new_df['freq']))
        
        #create trace
        new_trace=[{'x': new_df['Cluster'],
                    'y':new_df['freq_pct'],
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
        
def Cluster_Time_Series(df,cluster_list):
    traces=[]
    for cluster in cluster_list:
        #data only for selected cluster and get freq by exam date
        sel_cluster=df[df['Cluster']==cluster]
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
                                     
def time_Series_Bar(df,clickData,cluster_list):
    
    
    if clickData==None:
        filtered=df[df.Cluster.isin(cluster_list)]
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
        filtered=df[(df['Regents Date']==exam_date) & (df.Cluster.isin(cluster_list))]
        
        traces=[]
        for cluster in cluster_list:
            second_filter=filtered[filtered.Cluster==cluster]
            counts=second_filter.Type.value_counts()
            traces.append({'type':'bar',
                    'x': counts.index.values.tolist(),
                    'y':counts.tolist(),
                    'hoverinfo':'y+name',
                    'name':cluster})
    
    
        return {'data':traces,
            'layout':{'title':'<b>MC/CR Breakdown of<br>Selected Clusters</b>',
                      'barmode':'stack',
                    'xaxis':{'title':'Question Type'},
                      'yaxis':{'title':'Number of Questions'},
                      'hovermode':'closest'}}