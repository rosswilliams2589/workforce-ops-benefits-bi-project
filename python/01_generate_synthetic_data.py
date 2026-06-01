import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path
from datetime import timedelta
import random

fake = Faker()
np.random.seed(42)
random.seed(42)

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Project settings
NUM_EMPLOYEES = 1000
NUM_VENDORS = 50
NUM_TICKETS = 5000

departments = [
    ("D001", "Operations", "Operations"),
    ("D002", "Customer Support", "Operations"),
    ("D003", "Finance", "Corporate"),
    ("D004", "Human Resources", "Corporate"),
    ("D005", "Information Technology", "Technology"),
    ("D006", "Sales", "Revenue"),
    ("D007", "Marketing", "Revenue"),
    ("D008", "Legal", "Corporate"),
    ("D009", "Analytics", "Technology"),
    ("D010", "Product", "Technology"),
    ("D011", "Compliance", "Corporate"),
    ("D012", "Administration", "Corporate"),
]

locations = ["Florida", "Texas", "Oklahoma", "New York", "California", "Remote"]
job_levels = ["Associate", "Analyst", "Senior Analyst", "Manager", "Director"]
medical_plans = ["Basic PPO", "Standard PPO", "Premium PPO", "HDHP"]
vendor_categories = ["Software", "Benefits", "Consulting", "Facilities", "Recruiting", "IT Services"]
request_types = ["IT Access", "Payroll Issue", "Benefits Question", "Vendor Request", "Onboarding", "System Support"]
priorities = ["Low", "Medium", "High", "Critical"]

# -----------------------------
# Departments
# -----------------------------
department_rows = []

for dept_id, dept_name, business_unit in departments:
    annual_budget = random.randint(1_500_000, 8_000_000)
    headcount_target = random.randint(40, 150)

    department_rows.append({
        "department_id": dept_id,
        "department_name": dept_name,
        "business_unit": business_unit,
        "annual_budget": annual_budget,
        "headcount_target": headcount_target
    })

departments_df = pd.DataFrame(department_rows)

# -----------------------------
# Employees
# -----------------------------
employee_rows = []

for i in range(1, NUM_EMPLOYEES + 1):
    employee_id = f"E{i:04d}"
    dept_id, dept_name, business_unit = random.choice(departments)

    job_level = np.random.choice(
        job_levels,
        p=[0.35, 0.30, 0.20, 0.10, 0.05]
    )

    salary_ranges = {
        "Associate": (42000, 60000),
        "Analyst": (55000, 80000),
        "Senior Analyst": (75000, 105000),
        "Manager": (95000, 135000),
        "Director": (130000, 180000)
    }

    salary = random.randint(*salary_ranges[job_level])
    hire_date = fake.date_between(start_date="-8y", end_date="-30d")

    # Create a slightly higher turnover pattern in Operations and Customer Support
    termination_probability = 0.12
    if dept_name in ["Customer Support", "Operations"]:
        termination_probability += 0.05

    terminated = np.random.random() < termination_probability

    if terminated:
        termination_date = fake.date_between(start_date=hire_date, end_date="today")
        employment_status = "Terminated"
    else:
        termination_date = None
        employment_status = "Active"

    manager_id = f"E{random.randint(1, NUM_EMPLOYEES):04d}"

    employee_rows.append({
        "employee_id": employee_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "department_id": dept_id,
        "job_level": job_level,
        "location": random.choice(locations),
        "hire_date": hire_date,
        "termination_date": termination_date,
        "employment_status": employment_status,
        "salary": salary,
        "manager_id": manager_id
    })

employees_df = pd.DataFrame(employee_rows)

# -----------------------------
# Payroll
# -----------------------------
payroll_rows = []
pay_periods = pd.date_range(start="2024-01-01", periods=24, freq="MS")

for _, emp in employees_df.iterrows():
    monthly_base_pay = emp["salary"] / 12

    dept_name = departments_df.loc[
        departments_df["department_id"] == emp["department_id"],
        "department_name"
    ].iloc[0]

    for pay_period in pay_periods:
        overtime_multiplier = 1.0

        # Simulated business pattern:
        # Operations and Customer Support have more overtime pressure.
        if dept_name in ["Customer Support", "Operations"]:
            overtime_multiplier = 2.0

        overtime_pay = np.random.gamma(shape=2, scale=120) * overtime_multiplier
        bonus_pay = np.random.choice([0, 250, 500, 1000], p=[0.80, 0.10, 0.07, 0.03])
        total_compensation = monthly_base_pay + overtime_pay + bonus_pay

        payroll_rows.append({
            "payroll_id": f"P{len(payroll_rows) + 1:06d}",
            "employee_id": emp["employee_id"],
            "pay_period": pay_period.date(),
            "base_pay": round(monthly_base_pay, 2),
            "overtime_pay": round(overtime_pay, 2),
            "bonus_pay": round(bonus_pay, 2),
            "total_compensation": round(total_compensation, 2)
        })

payroll_df = pd.DataFrame(payroll_rows)

# -----------------------------
# Benefits Enrollment
# -----------------------------
benefits_rows = []

for _, emp in employees_df.iterrows():
    medical_plan = np.random.choice(
        medical_plans,
        p=[0.25, 0.40, 0.25, 0.10]
    )

    plan_costs = {
        "Basic PPO": (120, 350),
        "Standard PPO": (180, 500),
        "Premium PPO": (260, 750),
        "HDHP": (90, 300)
    }

    employee_premium, employer_premium = plan_costs[medical_plan]

    benefits_rows.append({
        "employee_id": emp["employee_id"],
        "medical_plan": medical_plan,
        "dental_plan": np.random.choice(["Yes", "No"], p=[0.75, 0.25]),
        "vision_plan": np.random.choice(["Yes", "No"], p=[0.70, 0.30]),
        "retirement_401k": np.random.choice(["Yes", "No"], p=[0.68, 0.32]),
        "employee_premium": employee_premium,
        "employer_premium": employer_premium
    })

benefits_enrollment_df = pd.DataFrame(benefits_rows)

# -----------------------------
# Benefits Claims
# -----------------------------
claims_rows = []

for _, emp in employees_df.iterrows():
    medical_plan = benefits_enrollment_df.loc[
        benefits_enrollment_df["employee_id"] == emp["employee_id"],
        "medical_plan"
    ].iloc[0]

    for claim_month in pay_periods:
        base_claim = {
            "Basic PPO": 180,
            "Standard PPO": 240,
            "Premium PPO": 350,
            "HDHP": 130
        }[medical_plan]

        medical_claim_cost = max(0, np.random.normal(base_claim, 90))
        dental_claim_cost = max(0, np.random.normal(35, 20))
        vision_claim_cost = max(0, np.random.normal(20, 15))
        total_claim_cost = medical_claim_cost + dental_claim_cost + vision_claim_cost

        claims_rows.append({
            "claim_id": f"C{len(claims_rows) + 1:07d}",
            "employee_id": emp["employee_id"],
            "claim_month": claim_month.date(),
            "medical_claim_cost": round(medical_claim_cost, 2),
            "dental_claim_cost": round(dental_claim_cost, 2),
            "vision_claim_cost": round(vision_claim_cost, 2),
            "total_claim_cost": round(total_claim_cost, 2)
        })

benefits_claims_df = pd.DataFrame(claims_rows)

# -----------------------------
# Vendors
# -----------------------------
vendor_rows = []

for i in range(1, NUM_VENDORS + 1):
    dept_id, dept_name, business_unit = random.choice(departments)

    contract_amount = random.randint(25_000, 500_000)
    monthly_spend = contract_amount / 12 * np.random.uniform(0.85, 1.20)
    renewal_date = fake.date_between(start_date="today", end_date="+18M")

    vendor_rows.append({
        "vendor_id": f"V{i:03d}",
        "vendor_name": fake.company(),
        "department_id": dept_id,
        "vendor_category": random.choice(vendor_categories),
        "contract_amount": round(contract_amount, 2),
        "monthly_spend": round(monthly_spend, 2),
        "renewal_date": renewal_date
    })

vendors_df = pd.DataFrame(vendor_rows)

# -----------------------------
# Operations Tickets
# -----------------------------
ticket_rows = []

for i in range(1, NUM_TICKETS + 1):
    dept_id, dept_name, business_unit = random.choice(departments)

    opened_date = fake.date_between(start_date="-24M", end_date="today")
    request_type = random.choice(request_types)
    priority = random.choice(priorities)

    sla_target_days = {
        "Low": 7,
        "Medium": 5,
        "High": 3,
        "Critical": 1
    }[priority]

    # Simulated business pattern:
    # IT Access and Onboarding requests take longer.
    resolution_days = np.random.poisson(lam=3)
    if request_type in ["IT Access", "Onboarding"]:
        resolution_days += random.randint(1, 5)

    closed_date = opened_date + timedelta(days=int(resolution_days))
    status = np.random.choice(["Closed", "Open", "In Progress"], p=[0.82, 0.08, 0.10])

    if status != "Closed":
        closed_date = None

    ticket_rows.append({
        "ticket_id": f"T{i:06d}",
        "department_id": dept_id,
        "request_type": request_type,
        "priority": priority,
        "opened_date": opened_date,
        "closed_date": closed_date,
        "sla_target_days": sla_target_days,
        "status": status
    })

operations_tickets_df = pd.DataFrame(ticket_rows)

# -----------------------------
# Export raw CSV files
# -----------------------------
departments_df.to_csv(RAW_DIR / "departments.csv", index=False)
employees_df.to_csv(RAW_DIR / "employees.csv", index=False)
payroll_df.to_csv(RAW_DIR / "payroll.csv", index=False)
benefits_enrollment_df.to_csv(RAW_DIR / "benefits_enrollment.csv", index=False)
benefits_claims_df.to_csv(RAW_DIR / "benefits_claims.csv", index=False)
vendors_df.to_csv(RAW_DIR / "vendors.csv", index=False)
operations_tickets_df.to_csv(RAW_DIR / "operations_tickets.csv", index=False)

print("Synthetic raw data generated successfully.")
print(f"Files saved to: {RAW_DIR}")
print("Generated files:")
print("- departments.csv")
print("- employees.csv")
print("- payroll.csv")
print("- benefits_enrollment.csv")
print("- benefits_claims.csv")
print("- vendors.csv")
print("- operations_tickets.csv")