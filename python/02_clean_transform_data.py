import pandas as pd
import numpy as np
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "clean"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load raw CSV files
# -----------------------------
employees = pd.read_csv(RAW_DIR / "employees.csv")
departments = pd.read_csv(RAW_DIR / "departments.csv")
payroll = pd.read_csv(RAW_DIR / "payroll.csv")
benefits_enrollment = pd.read_csv(RAW_DIR / "benefits_enrollment.csv")
benefits_claims = pd.read_csv(RAW_DIR / "benefits_claims.csv")
vendors = pd.read_csv(RAW_DIR / "vendors.csv")
operations_tickets = pd.read_csv(RAW_DIR / "operations_tickets.csv")

# -----------------------------
# Clean Employees
# -----------------------------
employees["hire_date"] = pd.to_datetime(employees["hire_date"])
employees["termination_date"] = pd.to_datetime(employees["termination_date"], errors="coerce")

# Use a fixed analysis date so results stay stable in the portfolio project
analysis_date = pd.Timestamp("2026-06-01")

employees["tenure_years"] = np.where(
    employees["termination_date"].notna(),
    (employees["termination_date"] - employees["hire_date"]).dt.days / 365.25,
    (analysis_date - employees["hire_date"]).dt.days / 365.25
)

employees["tenure_years"] = employees["tenure_years"].round(2)

employees["tenure_band"] = pd.cut(
    employees["tenure_years"],
    bins=[-0.01, 1, 3, 5, 10],
    labels=["<1 Year", "1-3 Years", "3-5 Years", "5+ Years"]
)

employees["salary_band"] = pd.cut(
    employees["salary"],
    bins=[0, 60000, 85000, 115000, 150000, 250000],
    labels=["<$60K", "$60K-$85K", "$85K-$115K", "$115K-$150K", "$150K+"]
)

employees["terminated_flag"] = np.where(employees["employment_status"] == "Terminated", 1, 0)
employees["active_flag"] = np.where(employees["employment_status"] == "Active", 1, 0)

# -----------------------------
# Clean Departments
# -----------------------------
departments["annual_budget"] = departments["annual_budget"].astype(float)
departments["monthly_budget"] = departments["annual_budget"] / 12

# -----------------------------
# Clean Payroll
# -----------------------------
payroll["pay_period"] = pd.to_datetime(payroll["pay_period"])

payroll["pay_year"] = payroll["pay_period"].dt.year
payroll["pay_month"] = payroll["pay_period"].dt.month
payroll["pay_month_name"] = payroll["pay_period"].dt.strftime("%b")
payroll["pay_year_month"] = payroll["pay_period"].dt.strftime("%Y-%m")

payroll["overtime_flag"] = np.where(payroll["overtime_pay"] > 0, 1, 0)

# -----------------------------
# Clean Benefits Enrollment
# -----------------------------
benefits_enrollment["dental_flag"] = np.where(benefits_enrollment["dental_plan"] == "Yes", 1, 0)
benefits_enrollment["vision_flag"] = np.where(benefits_enrollment["vision_plan"] == "Yes", 1, 0)
benefits_enrollment["retirement_401k_flag"] = np.where(benefits_enrollment["retirement_401k"] == "Yes", 1, 0)

benefits_enrollment["total_monthly_benefits_cost"] = (
    benefits_enrollment["employee_premium"] + benefits_enrollment["employer_premium"]
)

benefits_enrollment["benefits_participation_score"] = (
    1
    + benefits_enrollment["dental_flag"]
    + benefits_enrollment["vision_flag"]
    + benefits_enrollment["retirement_401k_flag"]
)

# -----------------------------
# Clean Benefits Claims
# -----------------------------
benefits_claims["claim_month"] = pd.to_datetime(benefits_claims["claim_month"])
benefits_claims["claim_year"] = benefits_claims["claim_month"].dt.year
benefits_claims["claim_month_num"] = benefits_claims["claim_month"].dt.month
benefits_claims["claim_year_month"] = benefits_claims["claim_month"].dt.strftime("%Y-%m")

benefits_claims["high_claim_flag"] = np.where(
    benefits_claims["total_claim_cost"] >= benefits_claims["total_claim_cost"].quantile(0.90),
    1,
    0
)

# -----------------------------
# Clean Vendors
# -----------------------------
vendors["renewal_date"] = pd.to_datetime(vendors["renewal_date"])

vendors["days_until_renewal"] = (vendors["renewal_date"] - analysis_date).dt.days

vendors["renewal_90_day_flag"] = np.where(
    (vendors["days_until_renewal"] >= 0) & (vendors["days_until_renewal"] <= 90),
    1,
    0
)

vendors["annualized_spend"] = vendors["monthly_spend"] * 12

vendors["contract_variance"] = vendors["annualized_spend"] - vendors["contract_amount"]

vendors["contract_variance_pct"] = np.where(
    vendors["contract_amount"] != 0,
    vendors["contract_variance"] / vendors["contract_amount"],
    0
)

# -----------------------------
# Clean Operations Tickets
# -----------------------------
operations_tickets["opened_date"] = pd.to_datetime(operations_tickets["opened_date"])
operations_tickets["closed_date"] = pd.to_datetime(operations_tickets["closed_date"], errors="coerce")

operations_tickets["closed_flag"] = np.where(operations_tickets["status"] == "Closed", 1, 0)

operations_tickets["resolution_days"] = (
    operations_tickets["closed_date"] - operations_tickets["opened_date"]
).dt.days

operations_tickets["resolution_days"] = operations_tickets["resolution_days"].fillna(0)

operations_tickets["sla_missed_flag"] = np.where(
    (operations_tickets["closed_flag"] == 1)
    & (operations_tickets["resolution_days"] > operations_tickets["sla_target_days"]),
    1,
    0
)

operations_tickets["sla_met_flag"] = np.where(
    (operations_tickets["closed_flag"] == 1)
    & (operations_tickets["resolution_days"] <= operations_tickets["sla_target_days"]),
    1,
    0
)

operations_tickets["opened_year"] = operations_tickets["opened_date"].dt.year
operations_tickets["opened_month"] = operations_tickets["opened_date"].dt.month
operations_tickets["opened_year_month"] = operations_tickets["opened_date"].dt.strftime("%Y-%m")

# -----------------------------
# Create analytical summary tables
# -----------------------------

# Payroll summary by employee
employee_payroll_summary = payroll.groupby("employee_id", as_index=False).agg(
    total_compensation=("total_compensation", "sum"),
    total_base_pay=("base_pay", "sum"),
    total_overtime_pay=("overtime_pay", "sum"),
    total_bonus_pay=("bonus_pay", "sum"),
    avg_monthly_compensation=("total_compensation", "mean"),
    avg_monthly_overtime=("overtime_pay", "mean")
)

employee_payroll_summary["high_overtime_flag"] = np.where(
    employee_payroll_summary["avg_monthly_overtime"]
    >= employee_payroll_summary["avg_monthly_overtime"].quantile(0.75),
    1,
    0
)

# Employee analytical file for R modeling
employee_modeling = (
    employees
    .merge(departments[["department_id", "department_name", "business_unit"]], on="department_id", how="left")
    .merge(employee_payroll_summary, on="employee_id", how="left")
    .merge(
        benefits_enrollment[
            [
                "employee_id",
                "medical_plan",
                "dental_flag",
                "vision_flag",
                "retirement_401k_flag",
                "employee_premium",
                "employer_premium",
                "total_monthly_benefits_cost",
                "benefits_participation_score"
            ]
        ],
        on="employee_id",
        how="left"
    )
)

# Department scorecard base file
payroll_with_dept = payroll.merge(
    employees[["employee_id", "department_id"]],
    on="employee_id",
    how="left"
)

department_payroll_summary = payroll_with_dept.groupby("department_id", as_index=False).agg(
    total_labor_cost=("total_compensation", "sum"),
    total_overtime_cost=("overtime_pay", "sum"),
    avg_monthly_labor_cost=("total_compensation", "mean")
)

department_headcount_summary = employees.groupby("department_id", as_index=False).agg(
    active_headcount=("active_flag", "sum"),
    total_employees=("employee_id", "count"),
    terminated_employees=("terminated_flag", "sum")
)

department_headcount_summary["turnover_rate"] = np.where(
    department_headcount_summary["total_employees"] != 0,
    department_headcount_summary["terminated_employees"] / department_headcount_summary["total_employees"],
    0
)

benefits_with_dept = benefits_enrollment.merge(
    employees[["employee_id", "department_id"]],
    on="employee_id",
    how="left"
)

department_benefits_summary = benefits_with_dept.groupby("department_id", as_index=False).agg(
    total_employer_premium=("employer_premium", "sum"),
    total_employee_premium=("employee_premium", "sum"),
    avg_employer_premium=("employer_premium", "mean"),
    avg_total_benefits_cost=("total_monthly_benefits_cost", "mean")
)

department_vendor_summary = vendors.groupby("department_id", as_index=False).agg(
    total_monthly_vendor_spend=("monthly_spend", "sum"),
    total_annualized_vendor_spend=("annualized_spend", "sum"),
    vendors_renewing_90_days=("renewal_90_day_flag", "sum")
)

department_ticket_summary = operations_tickets.groupby("department_id", as_index=False).agg(
    total_tickets=("ticket_id", "count"),
    closed_tickets=("closed_flag", "sum"),
    sla_missed=("sla_missed_flag", "sum"),
    sla_met=("sla_met_flag", "sum"),
    avg_resolution_days=("resolution_days", "mean")
)

department_ticket_summary["sla_compliance_rate"] = np.where(
    department_ticket_summary["closed_tickets"] != 0,
    department_ticket_summary["sla_met"] / department_ticket_summary["closed_tickets"],
    0
)

department_scorecard = (
    departments
    .merge(department_headcount_summary, on="department_id", how="left")
    .merge(department_payroll_summary, on="department_id", how="left")
    .merge(department_benefits_summary, on="department_id", how="left")
    .merge(department_vendor_summary, on="department_id", how="left")
    .merge(department_ticket_summary, on="department_id", how="left")
)

department_scorecard["labor_cost_per_active_employee"] = np.where(
    department_scorecard["active_headcount"] != 0,
    department_scorecard["total_labor_cost"] / department_scorecard["active_headcount"],
    0
)

department_scorecard["benefits_cost_per_active_employee"] = np.where(
    department_scorecard["active_headcount"] != 0,
    department_scorecard["total_employer_premium"] / department_scorecard["active_headcount"],
    0
)

department_scorecard["budget_variance"] = (
    department_scorecard["total_labor_cost"]
    + department_scorecard["total_annualized_vendor_spend"].fillna(0)
    - department_scorecard["annual_budget"]
)

department_scorecard["budget_variance_pct"] = np.where(
    department_scorecard["annual_budget"] != 0,
    department_scorecard["budget_variance"] / department_scorecard["annual_budget"],
    0
)

# -----------------------------
# Export clean CSV files
# -----------------------------
employees.to_csv(CLEAN_DIR / "employees_clean.csv", index=False)
departments.to_csv(CLEAN_DIR / "departments_clean.csv", index=False)
payroll.to_csv(CLEAN_DIR / "payroll_clean.csv", index=False)
benefits_enrollment.to_csv(CLEAN_DIR / "benefits_enrollment_clean.csv", index=False)
benefits_claims.to_csv(CLEAN_DIR / "benefits_claims_clean.csv", index=False)
vendors.to_csv(CLEAN_DIR / "vendors_clean.csv", index=False)
operations_tickets.to_csv(CLEAN_DIR / "operations_tickets_clean.csv", index=False)

employee_payroll_summary.to_csv(CLEAN_DIR / "employee_payroll_summary.csv", index=False)
employee_modeling.to_csv(CLEAN_DIR / "employee_modeling.csv", index=False)
department_scorecard.to_csv(CLEAN_DIR / "department_scorecard.csv", index=False)

print("Clean data transformation completed successfully.")
print(f"Clean files saved to: {CLEAN_DIR}")
print("Generated clean files:")
print("- employees_clean.csv")
print("- departments_clean.csv")
print("- payroll_clean.csv")
print("- benefits_enrollment_clean.csv")
print("- benefits_claims_clean.csv")
print("- vendors_clean.csv")
print("- operations_tickets_clean.csv")
print("- employee_payroll_summary.csv")
print("- employee_modeling.csv")
print("- department_scorecard.csv")