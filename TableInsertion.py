# Insert data into each of 3 exam tables

#import libraries
import pandas as pd
import os
from sqlalchemy import create_engine, MetaData, Table, select, insert

###########################################################################################
# testing insertion with table from udemy course

# create engine
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:####/Test Database')

# connection
conn = engine.connect()

metadata = MetaData()
sql_table = Table('customers', metadata, autoload=True, autoload_with=engine)
sql_columns=sql_table.columns.keys()

results = conn.execute(select([sql_table])).fetchall()

df = pd.DataFrame(results, columns=sql_table.columns.keys())
df_columns=reversed(df.columns.tolist())
#array=list(i for i in range (6,8))
array=list(i for i in range (8,9))

# create sample rows and add them to a list for insertion
rows=[]

for i in array:
    row=['max',i,'duke']
    rows.append(dict(zip(df_columns,row)))

#insert rows into table
conn.execute(sql_table.insert(),rows)


#check results of insertion
results = conn.execute(select([sql_table])).fetchall()
df_check = pd.DataFrame(results, columns=sql_table.columns.keys())
df_check.shape # equaled 7 so checks out

###########################################################################
# now for the real thing
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

os.chdir('D:\\MathRegentsDataFiles')

alg_csv=pd.read_csv('PreppedAlg1QuestionBreakdown.csv', encoding='latin1')
alg_2018=alg_csv[alg_csv.DateFixed=='18-Jun']
alg=load_postgres('Alg1CC')

# create engine
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:####/Regents Exams DataBase')

    # connection
conn = engine.connect()

metadata = MetaData()
sql_table = Table('Alg1CC', metadata, autoload=True, autoload_with=engine)
sql_columns=sql_table.columns.keys()

rows = []
for i in range(alg.shape[0]+1,alg_csv.shape+1):
    row=alg_2018.iloc[i-alg.shape[0]+1,:].values.tolist()
    row=[str(x) for x in row]
    row.insert(0, str(i))
    rows.append(dict(zip(sql_columns,row)))

# insert data into table
conn.execute(sql_table.insert(),rows)

# check results of insertion
results = conn.execute(select([sql_table])).fetchall()
df_check = pd.DataFrame(results, columns=sql_table.columns.keys())
df_check.shape

# successful