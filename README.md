# Workforce Operations & Benefits Cost Intelligence Dashboard

## Project Status
This project is currently in development.

## Project Overview
This project is an end-to-end business intelligence case study analyzing workforce costs, employee benefits, vendor spend, SLA performance, budget variance, and turnover risk for a synthetic mid-sized company.

The goal is to simulate how an Operations Analyst, Business Intelligence Analyst, Business Operations Analyst, Financial Benefits Analyst, or Data Analyst could help leadership identify cost drivers, operational inefficiencies, and workforce risk areas.

## Tools Used
- SQL
- Python
- R
- Snowflake
- Power BI
- GitHub

## Business Problem
BrightPath Services Group is experiencing rising operating costs across payroll, employee benefits, vendor spend, and internal operations. Leadership currently reviews these areas through disconnected spreadsheets and department-level reports, making it difficult to identify cost drivers, process inefficiencies, and workforce risks.

## Project Goals
- Analyze workforce and payroll cost trends
- Evaluate employee benefits costs and utilization
- Identify vendor spend concentration and renewal risks
- Measure SLA performance and operational bottlenecks
- Assess potential employee turnover risk indicators
- Build a Power BI executive dashboard for decision-making

## Planned Dashboard Pages
1. Executive Summary
2. Workforce & Payroll Analysis
3. Benefits Cost Analysis
4. Vendor Spend & Budget Control
5. Operations SLA Performance
6. Turnover Risk Insights

## Repository Structure
```text
workforce-ops-benefits-bi-project/
│
├── data/
│   ├── raw/
│   ├── clean/
│
├── python/
│   ├── 01_generate_synthetic_data.py
│   ├── 02_clean_transform_data.py
│
├── sql/
│   ├── 01_create_database_schema.sql
│   ├── 02_create_tables.sql
│   ├── 03_load_data.sql
│   ├── 04_cleaning_views.sql
│   ├── 05_reporting_views.sql
│
├── r/
│   ├── turnover_risk_model.R
│
├── powerbi/
│   ├── workforce_ops_dashboard.pbix
│
├── visuals/
│   ├── dashboard_screenshot_1.png
│   ├── dashboard_screenshot_2.png
│   ├── dashboard_screenshot_3.png
│
├── README.md
└── project_summary.md
