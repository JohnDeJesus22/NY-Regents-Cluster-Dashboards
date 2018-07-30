# Understanding the Math Regents to Find Time for Real Learning in the School Year
The math regents exams assess a variety of topics per subject. Due to time constraints, student performance, teacher level, and class time lost due to unexpected events teachers can not cover all the material for students to obtain mastery of each topic. More importantly, the internal need to cover these topics often leads to the sacrifice of teaching topics in a project or real-life based manner. To provide this opportunity to teachers, I have collected the question data publicly provided on each regents exam and uploaded it to Postgresql. 
<br/>

Currently I am performing EDA on the Geometry Regents to obtain answers to the following questions:
* Is the frequency of each cluster of questions consistent through exam?
* Does the frequency of each cluster hold true with the engageny guidelines?
* Are there clusters being skipped? If so why and is there consistence with those omissions?
* Which clusters in a domain are more widely assessed?
<br/>
The answers to these questions will provide guidelines to the true amount of time that a teacher can delegate to a range of topics. Ideally the topics that are most focused on is where teachers can conduct their project/real-life based lessons.

## NY-Regents-Cluster-Dashboards
Dashboards of Math Regents Questions by Cluster to get visual insights. 

The original versions of the dashboards were made with Tableau. The data was prepped with Pandas.
The plan here will be to create this dashboards as a web app created with the Python library Dash.

## Tableau Dashboards
[Algebra 1 Common Core](https://public.tableau.com/profile/johndejesus#!/vizhome/Algebra1CCExamBreakdown/ClusterOccurrenceDashboard)
Updated with Jan 2018 Regents

[Geometry Common Core](https://public.tableau.com/profile/johndejesus#!/vizhome/GeometryCCRegentsBreakdown/ClusterOccurrence)
Updated with Jan 2018 Regents

[Algebra 2 Common Core](https://public.tableau.com/profile/johndejesus#!/vizhome/Algebra2CCBreakdown/ClusterOccurrence)
Updated with August 2017 Regents
