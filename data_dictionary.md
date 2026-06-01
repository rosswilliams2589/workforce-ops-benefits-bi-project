# Data Dictionary

This file defines the synthetic datasets used in the Workforce Operations & Benefits Cost Intelligence Dashboard.

## 1. employees.csv

| Column | Description |
|---|---|
| employee_id | Unique employee identifier |
| first_name | Synthetic employee first name |
| last_name | Synthetic employee last name |
| department_id | Department identifier |
| job_level | Employee level such as Associate, Analyst, Senior Analyst, Manager, or Director |
| location | Employee work location |
| hire_date | Employee hire date |
| termination_date | Employee termination date, if applicable |
| employment_status | Active or Terminated |
| salary | Annual salary |
| manager_id | Employee manager identifier |

## 2. departments.csv

| Column | Description |
|---|---|
| department_id | Unique department identifier |
| department_name | Department name |
| business_unit | Larger business unit |
| annual_budget | Annual department budget |
| headcount_target | Planned department headcount |

## 3. payroll.csv

| Column | Description |
|---|---|
| payroll_id | Unique payroll record identifier |
| employee_id | Employee identifier |
| pay_period | Payroll period date |
| base_pay | Base payroll amount |
| overtime_pay | Overtime payroll amount |
| bonus_pay | Bonus payroll amount |
| total_compensation | Total payroll compensation for the period |

## 4. benefits_enrollment.csv

| Column | Description |
|---|---|
| employee_id | Employee identifier |
| medical_plan | Medical plan selected |
| dental_plan | Dental plan selected |
| vision_plan | Vision plan selected |
| retirement_401k | 401k participation flag |
| employee_premium | Employee monthly premium contribution |
| employer_premium | Employer monthly premium contribution |

## 5. benefits_claims.csv

| Column | Description |
|---|---|
| claim_id | Unique claim identifier |
| employee_id | Employee identifier |
| claim_month | Month of claim activity |
| medical_claim_cost | Medical claims cost |
| dental_claim_cost | Dental claims cost |
| vision_claim_cost | Vision claims cost |
| total_claim_cost | Total claims cost |

## 6. vendors.csv

| Column | Description |
|---|---|
| vendor_id | Unique vendor identifier |
| vendor_name | Synthetic vendor name |
| department_id | Department using the vendor |
| vendor_category | Vendor category |
| contract_amount | Total annual contract amount |
| monthly_spend | Monthly vendor spend |
| renewal_date | Contract renewal date |

## 7. operations_tickets.csv

| Column | Description |
|---|---|
| ticket_id | Unique ticket identifier |
| department_id | Department submitting or owning the ticket |
| request_type | Type of operational request |
| priority | Ticket priority |
| opened_date | Date ticket was opened |
| closed_date | Date ticket was closed |
| sla_target_days | Target resolution time in days |
| status | Open, Closed, or In Progress |
