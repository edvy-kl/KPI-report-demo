# KPI Report Demo - Service Desk Data Analysis Project
![dashboard.gif](docs/dashboard.gif)
## Project Overview
**Professional Showcase**: A comprehensive data analysis project demonstrating skills in:
- Business case development
- Key Performance Indicator (KPI) design
- Data modeling and database schema design
- Synthetic data generation
- Data analysis using SQL
- Business intelligence visualization with Grafana

### Motivation
Using open source tools for data analysis and KPI monitoring.

### Project Scope
This project was a end-to-end exercise in transforming raw service desk data into actionable business insights. My primary responsibilities included:
- Defining the business case and strategic objectives
- Identifying and designing meaningful KPIs
- Setting up infrastructure using [DashForgeLab](https://github.com/neuragicus/DashForgeLab)
- Designing and creating Ticket data model
- Generating a realistic dataset using complex logic
- Developing SQL queries for data analysis
- Creating a Grafana dashboard for visual reporting

## Business Goal

**Objective**: Systematically identify and address service desk performance gaps to continuously improve IT support quality and customer satisfaction.

### Business Problem

**User Story**: As an IT Support team leader, I want to monitor the quality of the service my team provides, enabling data-driven improvements in support operations.

## Technical Stack

- **Database**: PostgreSQL
- **Data Analysis**: SQL
- **Visualization**: Grafana

## Key Performance Indicators (KPIs)

| KPI | Business Rationale | Measurement | Improvement Target                                                                 |
|-----|-------------------|-------------|------------------------------------------------------------------------------------|
| Total Monthly Tickets | Understand support team workload | Number of tickets processed per month | Normalize ticket volume, identify peak periods                                     |
| Ticket Status Analysis | Optimize workflow effectiveness | Number of tickets per closure status | Minimize unnecessary ticket submissions and Reduce need for technical escalation |
| First Response Time | Improve initial support responsiveness | Average time between ticket creation and agent assignment | Reduce to <2 hours                                                                 |
| Time to Resolution | Reduce operational inefficiencies | Monthly average time from ticket creation to closure | Decrease average resolution time by 15% quarterly                                  |
| Ticket Closure Rate | Ensure timely problem solving | Percentage of tickets closed within 48 hours | Increase to >85% of tickets resolved within SLA                                    |
| Callback Incidents | Identify complex issue patterns | Number of tickets requiring customer callback | Decrease callback rate by 20%                                                      |
| Customer Satisfaction | Measure service quality perception | Average customer rating per month | Maintain rating above 4                                                            |


### KPI Metrics Explanation
**Time to Resolution and Closure Rate**: These metrics are used together to provide a comprehensive view of service desk performance. While the average resolution time might show a low number (e.g., below 2 days), the closure rate reveals the percentage of tickets actually resolved within the desired timeframe. For example, an average of 1.8 days might mask that 40% of tickets take over 48 hours to close, highlighting the importance of using both metrics for a nuanced understanding of performance.

## Repository Contents

- SQL analysis scripts
- Grafana dashboard configuration JSON file
- Sample screenshots of the report
- Postgres and Grafana setup using [DashForgeLab](https://github.com/neuragicus/DashForgeLab)
- Scripts for Ticket data model and database population

## How to reproduce the project
- Install the requirements:
```pip install -r requirements.txt```
- Add a `.env` file containing your database credentials, refer to  [DashForgeLab](https://github.com/neuragicus/DashForgeLab) documentation for extensive setup documentation. 
- Start the postgres database:
```./database/start-postgres-db.sh```
- Insert tickets dummy data:
```python insert_dummy_data.py```
- Start grafana: 
```./grafana/start-grafana.sh```
- Go to `localhost:3000` to access grafanaUI and login with your selected credentials (you should have them in your `.env` )
- Add a postgres datasource via the grafana UI:
```
Navigate to Datasource and search for postgres. 
Enter the details according to your setup:
HostURL: postgres-dashforge:5432
Database name: service_desk
...
your RO credentials from .env
...
```
- Navigate to add dashboard and import the json [service_desk_dashboard.json](grafana/service_desk_dashboard.json),
By default, the json contains a unique ID for the datasource. If the panels don't automatically update the 
data source, update it in each dashboard panel. This might happen due to limitation of exporting 
dashboard using its json. 

  
## A snapshot of the project's result
Below screenshots give you an overview of the dashboard created as a result of this project.

![ticket count.png](docs/ticket%20count.png)
![resp and res kpi.png](docs/resp%20and%20res%20kpi.png)
![callback inc.png](docs/callback%20inc.png)
![customer rating.png](docs/customer%20rating.png)