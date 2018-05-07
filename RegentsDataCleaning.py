#Regents Data Cleaning

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#geo regents as of Aug 2017
geo=pd.read_excel('GeoQuestionBreakdown.xlsx')
geo['Type']=geo['Type'].map({'Multiple':'MC', 'Constructed': 'CR'})

geo.to_excel('PreppedGeoQuestionBreakdown.xlsx', index=False)

#############################################################################################
#Alg 1 regents as of Aug 2017
alg=pd.read_excel('Alg1QuestionBreakdownxl.xlsx')
alg['Type']=alg['Type'].map({'Multiple':'MC', 'Constructed': 'CR'})

alg.to_excel('PreppedAlg1QuestionBreakdown.xlsx', index=False)

#############################################################################################
#Alg 2 regents as of Aug 2017
alg=pd.read_excel('Alg2QuestionBreakdownxl.xlsx')
alg['Type']=alg['Type'].map({'Multiple':'MC', 'Constructed': 'CR'})

alg.to_excel('PreppedAlg2QuestionBreakdown.xlsx', index=False)

###########################################################################################
#mapping meanings to cluster codes for geometry
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

#create dictionary and map to new cluster title column
clusterDict=dict(zip(clusters,clusterMeanings))
geo['ClusterTitle']=geo['Cluster'].map(clusterDict)

#update excel file
geo.to_excel('PreppedGeoQuestionBreakdown.xlsx', index=False)
                 

                 