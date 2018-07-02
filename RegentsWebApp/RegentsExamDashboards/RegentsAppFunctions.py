# Regents Dashboard Functions

# import libraries
import pandas as pd
import os
from sqlalchemy import create_engine, MetaData, Table, select

pd.options.mode.chained_assignment = None
def load_postgres(table_name):
    # create engine
    engine = create_engine('postgresql+psycopg2://postgres:password@localhost:####/Regents Exams DataBase')

    # connection
    conn = engine.connect()

    metadata = MetaData()
    sql_table = Table(table_name, metadata, autoload=True, autoload_with=engine)

    # assign query to a variable with python sqlalchemy select
    results = conn.execute(select([sql_table])).fetchall()

    df = pd.DataFrame(results, columns=sql_table.columns.keys())
    return df


def load_data(pathname,file):
    os.chdir(pathname)
    df = pd.read_csv(file, encoding='latin1', usecols=['ClusterTitle',
                                                       'Cluster', 'DateFixed', 'Regents Date', 'Type'])
    
    return df


# MC/CR Nested Bar Function
def nested_bar(df, selected_exam):
    # create df grouped by question type,cluster, and exam
    type_group = df.groupby(['Type', 'Cluster', 'DateFixed','ClusterTitle']).size().reset_index(name='counts')
    
    # sort clusters alphabetically
    type_group=type_group.sort_values(by=['Cluster'])
    
    if selected_exam == 'All Exams':

        # get overall totals of clusters in each type
        type_group['QTypeTotals'] = type_group.groupby(['Type',
                    'Cluster'])['counts'].transform('sum')

        type_group['hovertext'] = type_group.apply(
            lambda x: '<b>{}</b> - {}<br>{} questions'.format(x['Cluster'], x['ClusterTitle'],
                                                              x['QTypeTotals']), axis=1)
        # create trace
        stack_trace=[
                {'x':type_group['Cluster'][type_group.Type == 'MC'],
                 'y':type_group['QTypeTotals'][type_group.Type == 'MC'],
                 'type':'bar',
                 'name':'MC',
                 'text': type_group['hovertext'][type_group.Type == 'MC'],
                 'hoverinfo': 'text+name'},
                {'x': type_group['Cluster'][type_group.Type == 'CR'],
                 'y': type_group['QTypeTotals'][type_group.Type == 'CR'],
                 'text':type_group['hovertext'][type_group.Type == 'CR'],
                 'type':'bar',
                 'name':'CR',
                  'hoverinfo':'text+name'}
                 ]
        
        return {'data': stack_trace,
                'layout': {'plot_bgcolor': '#EAEAD2',
                           'paper_bgcolor': '#EAEAD2',
                           'hovermode': 'closest',
                           'title': '<b>Clusters By Question Type</b>',
                           'xaxis': {'title': '<b>Cluster Codes</b>'},
                           'yaxis': {'title': '<b>Total Number of Questions</b>'}}}

    else:
        type_group = type_group[type_group['DateFixed'] == selected_exam]

        type_group['hovertext'] = type_group.apply(
            lambda x: '<b>{}</b> - {}<br>{} questions'.format(x['Cluster'], x['ClusterTitle'],
                                                              x['counts']), axis=1)

        filtered_stack_trace = [
                {'x': type_group['Cluster'][type_group.Type == 'MC'],
                 'y': type_group['counts'][type_group.Type == 'MC'],
                 'type':'bar',
                 'name':'MC',
                 'text': type_group['hovertext'][type_group.Type == 'MC'],
                 'hoverinfo':'text+name'},
                {'x': type_group['Cluster'][type_group.Type == 'CR'],
                 'y': type_group['counts'][type_group.Type == 'CR'],
                 'type':'bar',
                 'text': type_group['hovertext'][type_group.Type == 'CR'],
                 'name':'CR',
                 'hoverinfo':'text+name'}
                 ]
        return {'data': filtered_stack_trace,
                'layout': {'plot_bgcolor': '#EAEAD2',
                           'paper_bgcolor': '#EAEAD2',
                           'hovermode': 'closest',
                           'title': '<b>Clusters by Question Type for </b>'+ selected_exam,
                           'xaxis': {'title': '<b>Cluster Codes</b>'},
                           'yaxis': {'title': '<b>Total Number of Questions</b>'}}}
        

# Missing Clusters Reveal
def reveal_missing_clusters(df, exam_date):
    if exam_date != 'All Exams':
        filtered_by_date = df[df.DateFixed == exam_date]
        
        if len(df.Cluster.unique()) == len(filtered_by_date.Cluster.unique()):
            return 'All clusters assessed in {}.'.format(exam_date)
        
        else:
            missing_clusters = []
            for i in df.Cluster.unique().tolist():
                if i not in filtered_by_date.Cluster.unique().tolist():
                    missing_clusters.append(i)
                    return 'The following clusters were not assessed in {}: {}'.format(exam_date,
                                                                        tuple(missing_clusters))


# percentage bar chart
def percentage_bar(df,selected_exam):
    
    if selected_exam != 'All Exams':
        # group data by DateFixed
        date_group = df.groupby(['DateFixed','Cluster', 'ClusterTitle']).size().reset_index(name='count')
        
        # filter exam by selected date
        sel_exam = date_group[date_group['DateFixed'] == selected_exam]
        
        # create percentage column
        sel_exam['count_pct'] = sel_exam['count'].apply(lambda x: x/sum(sel_exam['count']))

        sel_exam['hovertext']=sel_exam.apply(lambda x:'<b>{}</b> - {}<br>'.format(x['Cluster'],
                                                        x['ClusterTitle']), axis=1)

        # create trace
        new_trace = [{'x': sel_exam['Cluster'],
                      'y': sel_exam['count_pct'],
                     'type': 'bar',
                      'text': sel_exam['hovertext'],
                      'hoverinfo':'text+y'}]
        
        return {'data': new_trace,
                'layout': {
                        'plot_bgcolor': '#EAEAD2',
                        'paper_bgcolor': '#EAEAD2',
                        'hovermode': 'closest',
                        'title': '<b>Cluster Percentage Bar Chart for </b>' + selected_exam,
                        'xaxis': {'title': '<b>Cluster Codes</b>'},
                        'yaxis': {'title': '<b>Percentage of Exam</b>',
                                  'tickformat': '%'}}}
    else:
        # get frequency
        df['freq'] = df.groupby('Cluster')['Cluster'].transform('count')
        
        # drop duplicates
        new_df = df.drop_duplicates(subset=['Cluster'], keep='first')
        
        # percentage of exam column
        new_df['freq_pct'] = new_df['freq'].apply(lambda x: x/sum(new_df['freq']))

        new_df['hovertext'] = new_df.apply(lambda x:'<b>{}</b> - {}<br>'.format(x['Cluster'],
                                                                                x['ClusterTitle']), axis=1)
        # create trace
        new_trace=[{'x': new_df['Cluster'],
                    'y': new_df['freq_pct'],
                    'type': 'bar',
                    'text': new_df['hovertext'],
                    'hoverinfo': 'text+y'
                    }]
        return {'data': new_trace,
                'layout': {
                        'plot_bgcolor':'#EAEAD2',
                        'paper_bgcolor':'#EAEAD2',
                        'hovermode':'closest',
                        'title':'<b>Cluster Overall Percentage Bar Chart</b>',
                        'xaxis':{'title': '<b>Cluster Codes</b>'},
                        'yaxis':{'title': '<b>Percentage of All Exams</b>',
                                 'tickformat':'%'}}}


# time series line chart
def cluster_time_series(df, cluster_list):
    traces = []
    for cluster in cluster_list:
        # data only for selected cluster and get freq by exam date
        sel_cluster = df[df['Cluster'] == cluster]
        sel_cluster['freq'] = sel_cluster.groupby('Regents Date')['Regents Date'].transform('count')
    
        # convert Regents Date column to date time to sort correctly
        sel_cluster['Regents Date'] = pd.to_datetime(sel_cluster['Regents Date'])
        
        # drop duplicate dates
        sel_cluster = sel_cluster.drop_duplicates(subset=['Regents Date','Type'],keep='first')
    
        # sort by date
        sel_cluster = sel_cluster.sort_values(by=['Regents Date'])
        
        # hovertext
        sel_cluster['hovertext'] = sel_cluster.apply(lambda x:
                    '<b>{} {}</b><br> {} questions'.format(x['Regents Date'].strftime("%b"),
                                                           x['Regents Date'].year, x['freq']), axis=1)
        
        # create traces
        traces.append({'x': sel_cluster['Regents Date'],
                       'y': sel_cluster['freq'],
                       'type': 'scatter',
                       'text': sel_cluster['hovertext'],
                       'hoverinfo': 'text+name',
                       'name': cluster,
                       'mode': 'lines+markers'})

    return {'data': traces,
            'layout': {'title': '<b>Cluster Line Chart </b>',
                       'hovermode': 'closest',
                       'xaxis': {'title': '<b>Regents Exam Date</b>'},
                       'yaxis': {'title': '<b>Number of Questions</b>',
                       'range': [0, 6.75]}
                       }}


def time_series_bar(df, clickData, cluster_list):
    if clickData is None:
        filtered = df[df.Cluster.isin(cluster_list)]
        counts = filtered.Type.value_counts()
        
        trace = [{'type': 'bar',
                  'x': counts.index.values.tolist(),
                  'y': counts.tolist(),
                  'hoverinfo':'y'}]

        return {'data': trace,
                'layout': {'title': '<b>MC/CR Breakdown of Selected<br>Clusters for All Exams</b>',
                           'xaxis': {'title': 'Question Type'},
                           'yaxis': {'title': 'Number of Questions'},
                           'hovermode': 'closest'}}
    
    else:
        
        exam_date = clickData["points"][0]["x"]
        filtered = df[(df['Regents Date'] == exam_date) & (df.Cluster.isin(cluster_list))]
        exam_date = filtered['DateFixed'].tolist()[0]

        traces = []
        for cluster in cluster_list:
            second_filter = filtered[filtered.Cluster == cluster]
            counts = second_filter.Type.value_counts()
            traces.append({'type': 'bar',
                           'x': counts.index.values.tolist(),
                           'y': counts.tolist(),
                           'hoverinfo': 'y+name',
                           'name': cluster})

        return {'data': traces,
                'layout': {'title': '<b>MC/CR Breakdown of<br>Selected Clusters<br>for </b> ' + exam_date,
                           'barmode': 'stack',
                           'xaxis': {'title': 'Question Type'},
                           'yaxis': {'title': 'Number of Questions'},
                           'hovermode': 'closest'}}
