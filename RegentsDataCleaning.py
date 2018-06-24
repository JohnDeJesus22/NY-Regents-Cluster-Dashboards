# Regents Data Cleaning
import pandas as pd
import os

# geo regents as of Aug 2017
geo=pd.read_excel('GeoQuestionBreakdown.xlsx')
geo['Type'] = geo['Type'].map({'Multiple': 'MC', 'Constructed': 'CR'})

geo.to_excel('PreppedGeoQuestionBreakdown.xlsx', index=False)

#############################################################################################
# Alg 1 regents as of Aug 2017
alg = pd.read_excel('Alg1QuestionBreakdownxl.xlsx')
alg['Type']=alg['Type'].map({'Multiple':'MC', 'Constructed': 'CR'})

alg.to_excel('PreppedAlg1QuestionBreakdown.xlsx', index=False)

os.chdir('D:\\MathRegentsDataFiles')
alg = pd.read_csv('PreppedAlg1QuestionBreakdown.csv', encoding='latin1')
alg_clusters = sorted(alg.Cluster.unique().tolist())
alg_clustermeanings = ['Perform arithmetic operations on polynomials.',
                       'Understand the relationship between zeros and factors of polynomials.',
                       'Create equations that describe numbers or relationships.',
                       'Understand solving equations as a process of reasoning and explain the reasoning.',
                       'Solve equations and inequalities in one variable.',
                       'Solve systems of equations.',
                       'Represent and solve equations and inequalities graphically.',
                       'Interpret the structure of expressions.',
                       'Write expressions in equivalent forms to solve problems.',
                       'Build a function that models a relationship between two quantities.',
                       'Build new functions from existing functions.',
                       'Understand the concept of a function and use function notation.',
                       'Interpret functions that arise in applications in terms of the context.',
                       'Analyze functions using different representations.',
                       'Construct and compare linear, quadratic, and exponential models and solve problems.',
                       'Interpret expressions for functions in terms of the situation they model.',
                       'Reason quantitatively and use units to solve problems.',
                       'Use properties of rational and irrational numbers.',
                       'Summarize, represent, and interpret data on a single count or measurement variable',
                       'Summarize, represent, and interpret data on two categorical and quantitative variables',
                       'Interpret linear models']

# create dictionary and map to new cluster title column
alg_clusterDict = dict(zip(alg_clusters, alg_clustermeanings))
alg['ClusterTitle'] = alg['Cluster'].map(alg_clusterDict)
alg.to_csv('PreppedAlg1QuestionBreakdown.csv', index=False)
#############################################################################################
# Alg 2 regents as of Aug 2017
alg = pd.read_excel('Alg2QuestionBreakdownxl.xlsx')
alg['Type']=alg['Type'].map({'Multiple':'MC', 'Constructed': 'CR'})

alg.to_excel('PreppedAlg2QuestionBreakdown.xlsx', index=False)

###########################################################################################
# mapping meanings to cluster codes for geometry
geo=pd.read_excel('PreppedGeoQuestionBreakdown.xlsx')

clusters=sorted(geo['Cluster'].unique().tolist())
clusterMeanings=['Understand and apply theorems about circles',
                 'Find arc lengths and areas of sectors of circles',
                 'Experiment with transformations in the plane',
                 'Understand congruence in terms of rigid motions',
                 'Prove geometric theorems',
                 'Make geometric constructions',
                 'Explain volume formulas and use them to solve problems',
                 'Visualize relationships between two-dimensional and three-dimensional objects',
                 'Translate between the geometric description and the equation for a conic section',
                 'Use coordinates to prove simple geometric theorems algebraically',
                 'Apply geometric concepts in modeling situations',
                 'Understand similarity in terms of similarity transformations',
                 'Prove theorems involving similarity',
                 'Define trigonometric ratios and solve problems involving right triangles']

# create dictionary and map to new cluster title column
clusterDict=dict(zip(clusters,clusterMeanings))
geo['ClusterTitle']=geo['Cluster'].map(clusterDict)

# update excel file
geo.to_excel('PreppedGeoQuestionBreakdown.xlsx', index=False)
                 

                 