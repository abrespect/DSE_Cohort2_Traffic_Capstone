Introduction
====
Introduction | [Data](documents/report/Data.md) | [Exploratory Analysis](exploration/) | [Interactive Visualizations](documents/report/Visualizations.md)

## Abstract

This project concerns the analysis of data collected by CalTrans (http://pems.dot.ca.gov/). The data is collected from wire loops embedded in the asphalt of the California highways. It provides detailed information about the number of cars, their speed and their size.

Through extensive exploratory analysis, the Cohort 2 team pursued a myriad of different approaches and models.  However, the most robust and promising was an analysis of thirty minute oscillations that appear in the traffic flow data (number of vehicles per five minutes).  The team coined these oscillations as “the wiggles”.  In general, the phenomenon shows that the wiggles have local minima on the hour and half hour and have local maxima between 10 and 20 minutes past the hour and half hour.  Using a wavelet transform, the team was able to demonstrate that the wiggle phenomenon is real and that it oscillates along a freeway.

## Advisors

#### Professor Yoav Freund, PhD
- Faculty Director, UC San Diego Master of Advanced Study Program in Data Science and Engineering

#### Dr. Ilkay Altintas, PhD
- Chief Data Science Officer, San Diego Supercomputer Center (SDSC)
- Faculty Co-Director, UC San Diego Master of Advanced Study Program in Data Science and Engineering

## Team

Each team member contributed to the analysis, code development, and documentation of the project.  Additionally, team members were assigned to perform the duties of specific roles, as described below.

#### Miki Hardisty - Project Manager/ScrumMaster
* Team representative to advisors  
* Act as scrummaster for agile sprints including responsibilities to create a weekly project update for Ilkay based on Kanban deliverables, schedule meetings with Advisors and study group, and schedule collaboration sessions.
* Collect questions from team and revert to advisory resources; follow up for answers.
* Acts as the facilitator for an agile development team.
* Responsible for helping the team to reach consensus for what can be achieved during a specific period of time. Helps the team to reach consensus during the daily scrum, staying focused and follow the agreed-upon rules for daily scrums, removing obstacles that are impeding the team's progress and protecting the team from outside distractions.

#### Josh Duclos - Architect
* Responsible for technical design decisions (which libraries, tools, frameworks, etc we use as a team).  
* Ensure that we perform code reviews (or at least code walk-throughs) so everyone is working towards the same technical goals.

#### CJ Stevens - Product Owner
* Responsible for grooming the backlog and determining the sprint goal every two weeks.
* Walks the team through the user stories that are captured in the kanban tool.
* Based on team capacity, the product owner shall facilitate how many stories the team will commit to for the sprint.

#### Chris Sanders - Treasurer and Collaboration Tool Administrator
* Monitor spending on cloud instances.
* Setup, organize and maintain the GIT repository, kanbanflow and the various other tools needed within the team's ecosystem.

#### Abe Hart - Infrastructure Architect
* Ensure that virtual and cloud servers are setup and maintained for the team to utilize (ie spark setup, AWS setup, db setup, etc).

## Tools

| Languages | Repositories & Collaboration | Cloud |
| --------- | ---------------------------- | ----- |
| Python <br/>Javascript<br/>HTML<br/>CSS<br/>Spark | GitHub<br/>&nbsp;&nbsp;&nbsp;- [Cohort 1](https://github.com/conwaywong/dse_capstone)<br/>&nbsp;&nbsp;&nbsp;- [Cohort 2](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone)<br/>[KanbanFlow](https://kanbanflow.com/board/39b5b82d84b139d7bef8e203f9b72794)<br/>Google Docs| Amazon S3<br/>&nbsp;&nbsp;&nbsp;- [Cohort 1](https://console.aws.amazon.com/s3/home?region=us-west-2#&bucket=dse-team2-2014&prefix=)<br/>&nbsp;&nbsp;&nbsp;- [Cohort 2](https://console.aws.amazon.com/s3/home?region=us-west-2#&bucket=dse-team1-2015&prefix=)<br/>[Amazon Web Services](https://console.aws.amazon.com/s3/home?region=us-west-2#&bucket=dse-team1-2015&prefix=)<br/>[Databricks](http://tinyurl.com/dsedb)<br/>[Cyberduck](https://cyberduck.io/?l=en) |

## Resources

### Reports

| Location      | Description   |
| ------------- | -------------  |
| cohort2/documents/final_report.pdf | Final Report |
| cohort2/documents/final_report.? | Final Presentation |

### Buckets

| Location      | Description   |
| ------------- | -------------  |
| s3://dse-team2-2014/dse_traffic | Directory containing original downloaded traffic files for 2008 to 2015 |
| s3://dse-team2-2014/pivot_output_#{year} | Directory containing Pivot Output Files from parsing downloaded traffic files |
| s3://dse-team2-2014/regression | Directory containing files used for Elastic Net Regression |
| s3://dse-team1-2015/dse_traffic | Directory containing original downloaded traffic files for 2016 |

### Directory Structure
See Wiki for more information

| Path   | Description  |
|--------|-------------- |
| cohort1/ | Cohort 1's Efforts |
| cohort2/exploration/ | collection of exploratory notebooks, visualizations, etc. first word_ in name signifies effort area |
| cohort2/data/ | directory to hold smaller datasets |
| cohort2/documents/ | directory to hold documents |
| cohort2/trafficpassion/ | directory for python code related to final presentations, papers, and other files not related to exploration. |
| cohort2/config | directory for virtualenv configurations, anaconda environments, etc |
| cohort2/images | directory for related imagery |
| cohort2/vis | directory hosting the primary visualization for the project [WiggleVis](https://mas-dse-c6sander.github.io/DSE_Cohort2_Traffic_Capstone/cohort2/vis/WiggleVis/index.html#map_settings) and [SegmentVis](https://mas-dse-c6sander.github.io/DSE_Cohort2_Traffic_Capstone/cohort2/vis/WiggleVis/segmentVis.html)|
