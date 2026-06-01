-- =====================================================
-- 02_create_clean_tables.sql
-- Project: Workforce Operations & Benefits Cost Intelligence Dashboard
-- Purpose: Create clean schema tables for transformed CSV files
-- =====================================================

USE DATABASE WORKFORCE_OPS_BI;
USE SCHEMA CLEAN;

CREATE OR REPLACE TABLE EMPLOYEES_CLEAN (
    employee_id STRING,
    first_name STRING,
    last_name STRING,
    department_id STRING,
    job_level STRING,
    location STRING,
    hire_date DATE,
    termination_date DATE,
    employment_status STRING,
    salary NUMBER(12,2),
    manager_id STRING,
    tenure_years NUMBER(10,2),
    tenure_band STRING,
    salary_band STRING,
    terminated_flag NUMBER,
    active_flag NUMBER
);

CREATE OR REPLACE TABLE DEPARTMENTS_CLEAN (
    department_id STRING,
    department_name STRING,
    business_unit STRING,
    annual_budget NUMBER(14,2),
    headcount_target NUMBER,
    monthly_budget NUMBER(14,2)
);

CREATE OR REPLACE TABLE PAYROLL_CLEAN (
    payroll_id STRING,
    employee_id STRING,
    pay_period DATE,
    base_pay NUMBER(12,2),
    overtime_pay NUMBER(12,2),
    bonus_pay NUMBER(12,2),
    total_compensation NUMBER(12,2),
    pay_year NUMBER,
    pay_month NUMBER,
    pay_month_name STRING,
    pay_year_month STRING,
    overtime_flag NUMBER
);

CREATE OR REPLACE TABLE BENEFITS_ENROLLMENT_CLEAN (
    employee_id STRING,
    medical_plan STRING,
    dental_plan STRING,
    vision_plan STRING,
    retirement_401k STRING,
    employee_premium NUMBER(12,2),
    employer_premium NUMBER(12,2),
    dental_flag NUMBER,
    vision_flag NUMBER,
    retirement_401k_flag NUMBER,
    total_monthly_benefits_cost NUMBER(12,2),
    benefits_participation_score NUMBER
);

CREATE OR REPLACE TABLE BENEFITS_CLAIMS_CLEAN (
    claim_id STRING,
    employee_id STRING,
    claim_month DATE,
    medical_claim_cost NUMBER(12,2),
    dental_claim_cost NUMBER(12,2),
    vision_claim_cost NUMBER(12,2),
    total_claim_cost NUMBER(12,2),
    claim_year NUMBER,
    claim_month_num NUMBER,
    claim_year_month STRING,
    high_claim_flag NUMBER
);

CREATE OR REPLACE TABLE VENDORS_CLEAN (
    vendor_id STRING,
    vendor_name STRING,
    department_id STRING,
    vendor_category STRING,
    contract_amount NUMBER(14,2),
    monthly_spend NUMBER(14,2),
    renewal_date DATE,
    days_until_renewal NUMBER,
    renewal_90_day_flag NUMBER,
    annualized_spend NUMBER(14,2),
    contract_variance NUMBER(14,2),
    contract_variance_pct NUMBER(10,4)
);

CREATE OR REPLACE TABLE OPERATIONS_TICKETS_CLEAN (
    ticket_id STRING,
    department_id STRING,
    request_type STRING,
    priority STRING,
    opened_date DATE,
    closed_date DATE,
    sla_target_days NUMBER,
    status STRING,
    closed_flag NUMBER,
    resolution_days NUMBER,
    sla_missed_flag NUMBER,
    sla_met_flag NUMBER,
    opened_year NUMBER,
    opened_month NUMBER,
    opened_year_month STRING
);

CREATE OR REPLACE TABLE EMPLOYEE_PAYROLL_SUMMARY (
    employee_id STRING,
    total_compensation NUMBER(14,2),
    total_base_pay NUMBER(14,2),
    total_overtime_pay NUMBER(14,2),
    total_bonus_pay NUMBER(14,2),
    avg_monthly_compensation NUMBER(14,2),
    avg_monthly_overtime NUMBER(14,2),
    high_overtime_flag NUMBER
);

CREATE OR REPLACE TABLE EMPLOYEE_MODELING (
    employee_id STRING,
    first_name STRING,
    last_name STRING,
    department_id STRING,
    job_level STRING,
    location STRING,
    hire_date DATE,
    termination_date DATE,
    employment_status STRING,
    salary NUMBER(12,2),
    manager_id STRING,
    tenure_years NUMBER(10,2),
    tenure_band STRING,
    salary_band STRING,
    terminated_flag NUMBER,
    active_flag NUMBER,
    department_name STRING,
    business_unit STRING,
    total_compensation NUMBER(14,2),
    total_base_pay NUMBER(14,2),
    total_overtime_pay NUMBER(14,2),
    total_bonus_pay NUMBER(14,2),
    avg_monthly_compensation NUMBER(14,2),
    avg_monthly_overtime NUMBER(14,2),
    high_overtime_flag NUMBER,
    medical_plan STRING,
    dental_flag NUMBER,
    vision_flag NUMBER,
    retirement_401k_flag NUMBER,
    employee_premium NUMBER(12,2),
    employer_premium NUMBER(12,2),
    total_monthly_benefits_cost NUMBER(12,2),
    benefits_participation_score NUMBER
);

CREATE OR REPLACE TABLE DEPARTMENT_SCORECARD (
    department_id STRING,
    department_name STRING,
    business_unit STRING,
    annual_budget NUMBER(14,2),
    headcount_target NUMBER,
    monthly_budget NUMBER(14,2),
    active_headcount NUMBER,
    total_employees NUMBER,
    terminated_employees NUMBER,
    turnover_rate NUMBER(10,4),
    total_labor_cost NUMBER(14,2),
    total_overtime_cost NUMBER(14,2),
    avg_monthly_labor_cost NUMBER(14,2),
    total_employer_premium NUMBER(14,2),
    total_employee_premium NUMBER(14,2),
    avg_employer_premium NUMBER(14,2),
    avg_total_benefits_cost NUMBER(14,2),
    total_monthly_vendor_spend NUMBER(14,2),
    total_annualized_vendor_spend NUMBER(14,2),
    vendors_renewing_90_days NUMBER,
    total_tickets NUMBER,
    closed_tickets NUMBER,
    sla_missed NUMBER,
    sla_met NUMBER,
    avg_resolution_days NUMBER(10,2),
    sla_compliance_rate NUMBER(10,4),
    labor_cost_per_active_employee NUMBER(14,2),
    benefits_cost_per_active_employee NUMBER(14,2),
    budget_variance NUMBER(14,2),
    budget_variance_pct NUMBER(10,4)
);