-- =====================================================
-- 04_reporting_views.sql
-- Project: Workforce Operations & Benefits Cost Intelligence Dashboard
-- Purpose: Create reporting views for Power BI and business analysis
-- =====================================================

USE DATABASE WORKFORCE_OPS_BI;
USE SCHEMA REPORTING;

-- =====================================================
-- Department-level executive scorecard
-- =====================================================
CREATE OR REPLACE VIEW VW_DEPARTMENT_SCORECARD AS
SELECT
    department_id,
    department_name,
    business_unit,
    annual_budget,
    headcount_target,
    monthly_budget,
    active_headcount,
    total_employees,
    terminated_employees,
    turnover_rate,
    total_labor_cost,
    total_overtime_cost,
    avg_monthly_labor_cost,
    total_employer_premium,
    total_employee_premium,
    avg_employer_premium,
    avg_total_benefits_cost,
    total_monthly_vendor_spend,
    total_annualized_vendor_spend,
    vendors_renewing_90_days,
    total_tickets,
    closed_tickets,
    sla_missed,
    sla_met,
    avg_resolution_days,
    sla_compliance_rate,
    labor_cost_per_active_employee,
    benefits_cost_per_active_employee,
    budget_variance,
    budget_variance_pct
FROM WORKFORCE_OPS_BI.CLEAN.DEPARTMENT_SCORECARD;

-- =====================================================
-- Workforce and payroll reporting view
-- =====================================================
CREATE OR REPLACE VIEW VW_WORKFORCE_PAYROLL AS
SELECT
    e.employee_id,
    e.department_id,
    d.department_name,
    d.business_unit,
    e.job_level,
    e.location,
    e.employment_status,
    e.salary,
    e.tenure_years,
    e.tenure_band,
    e.salary_band,
    e.terminated_flag,
    e.active_flag,
    p.payroll_id,
    p.pay_period,
    p.pay_year,
    p.pay_month,
    p.pay_month_name,
    p.pay_year_month,
    p.base_pay,
    p.overtime_pay,
    p.bonus_pay,
    p.total_compensation,
    p.overtime_flag
FROM WORKFORCE_OPS_BI.CLEAN.EMPLOYEES_CLEAN e
LEFT JOIN WORKFORCE_OPS_BI.CLEAN.DEPARTMENTS_CLEAN d
    ON e.department_id = d.department_id
LEFT JOIN WORKFORCE_OPS_BI.CLEAN.PAYROLL_CLEAN p
    ON e.employee_id = p.employee_id;

-- =====================================================
-- Benefits analysis reporting view
-- =====================================================
CREATE OR REPLACE VIEW VW_BENEFITS_ANALYSIS AS
SELECT
    e.employee_id,
    e.department_id,
    d.department_name,
    d.business_unit,
    e.job_level,
    e.location,
    e.employment_status,
    e.tenure_years,
    e.tenure_band,
    e.salary_band,
    b.medical_plan,
    b.dental_plan,
    b.vision_plan,
    b.retirement_401k,
    b.dental_flag,
    b.vision_flag,
    b.retirement_401k_flag,
    b.employee_premium,
    b.employer_premium,
    b.total_monthly_benefits_cost,
    b.benefits_participation_score,
    c.claim_id,
    c.claim_month,
    c.claim_year,
    c.claim_month_num,
    c.claim_year_month,
    c.medical_claim_cost,
    c.dental_claim_cost,
    c.vision_claim_cost,
    c.total_claim_cost,
    c.high_claim_flag
FROM WORKFORCE_OPS_BI.CLEAN.EMPLOYEES_CLEAN e
LEFT JOIN WORKFORCE_OPS_BI.CLEAN.DEPARTMENTS_CLEAN d
    ON e.department_id = d.department_id
LEFT JOIN WORKFORCE_OPS_BI.CLEAN.BENEFITS_ENROLLMENT_CLEAN b
    ON e.employee_id = b.employee_id
LEFT JOIN WORKFORCE_OPS_BI.CLEAN.BENEFITS_CLAIMS_CLEAN c
    ON e.employee_id = c.employee_id;

-- =====================================================
-- Vendor spend reporting view
-- =====================================================
CREATE OR REPLACE VIEW VW_VENDOR_SPEND AS
SELECT
    v.vendor_id,
    v.vendor_name,
    v.department_id,
    d.department_name,
    d.business_unit,
    v.vendor_category,
    v.contract_amount,
    v.monthly_spend,
    v.annualized_spend,
    v.renewal_date,
    v.days_until_renewal,
    v.renewal_90_day_flag,
    v.contract_variance,
    v.contract_variance_pct
FROM WORKFORCE_OPS_BI.CLEAN.VENDORS_CLEAN v
LEFT JOIN WORKFORCE_OPS_BI.CLEAN.DEPARTMENTS_CLEAN d
    ON v.department_id = d.department_id;

-- =====================================================
-- SLA and operations reporting view
-- =====================================================
CREATE OR REPLACE VIEW VW_SLA_PERFORMANCE AS
SELECT
    t.ticket_id,
    t.department_id,
    d.department_name,
    d.business_unit,
    t.request_type,
    t.priority,
    t.opened_date,
    t.closed_date,
    t.sla_target_days,
    t.status,
    t.closed_flag,
    t.resolution_days,
    t.sla_missed_flag,
    t.sla_met_flag,
    t.opened_year,
    t.opened_month,
    t.opened_year_month
FROM WORKFORCE_OPS_BI.CLEAN.OPERATIONS_TICKETS_CLEAN t
LEFT JOIN WORKFORCE_OPS_BI.CLEAN.DEPARTMENTS_CLEAN d
    ON t.department_id = d.department_id;

-- =====================================================
-- Employee modeling view for R / turnover analysis
-- =====================================================
CREATE OR REPLACE VIEW VW_EMPLOYEE_MODELING AS
SELECT
    employee_id,
    department_id,
    department_name,
    business_unit,
    job_level,
    location,
    employment_status,
    salary,
    tenure_years,
    tenure_band,
    salary_band,
    terminated_flag,
    active_flag,
    total_compensation,
    total_base_pay,
    total_overtime_pay,
    total_bonus_pay,
    avg_monthly_compensation,
    avg_monthly_overtime,
    high_overtime_flag,
    medical_plan,
    dental_flag,
    vision_flag,
    retirement_401k_flag,
    employee_premium,
    employer_premium,
    total_monthly_benefits_cost,
    benefits_participation_score
FROM WORKFORCE_OPS_BI.CLEAN.EMPLOYEE_MODELING;

-- =====================================================
-- Executive KPI summary view
-- =====================================================
CREATE OR REPLACE VIEW VW_EXECUTIVE_KPI_SUMMARY AS
SELECT
    COUNT(DISTINCT department_id) AS total_departments,
    SUM(active_headcount) AS total_active_headcount,
    SUM(total_employees) AS total_employees,
    SUM(terminated_employees) AS total_terminated_employees,
    ROUND(SUM(terminated_employees) / NULLIF(SUM(total_employees), 0), 4) AS overall_turnover_rate,
    SUM(total_labor_cost) AS total_labor_cost,
    SUM(total_overtime_cost) AS total_overtime_cost,
    SUM(total_employer_premium) AS total_employer_benefits_cost,
    SUM(total_monthly_vendor_spend) AS total_monthly_vendor_spend,
    SUM(total_annualized_vendor_spend) AS total_annualized_vendor_spend,
    SUM(total_tickets) AS total_operations_tickets,
    SUM(closed_tickets) AS total_closed_tickets,
    SUM(sla_missed) AS total_sla_missed,
    SUM(sla_met) AS total_sla_met,
    ROUND(SUM(sla_met) / NULLIF(SUM(closed_tickets), 0), 4) AS overall_sla_compliance_rate,
    SUM(budget_variance) AS total_budget_variance
FROM WORKFORCE_OPS_BI.CLEAN.DEPARTMENT_SCORECARD;