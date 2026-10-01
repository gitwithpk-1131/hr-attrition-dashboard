"""Synthetic sample data with the same columns as the trimmed IBM HR file.

Only used when data/raw/hr_attrition.csv is missing, so the project always runs.
The numbers it produces are NOT real findings.
"""
import numpy as np
import pandas as pd


def generate(n: int = 1470, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    department = rng.choice(
        ["Sales", "Research & Development", "Human Resources"], size=n, p=[0.31, 0.65, 0.04]
    )
    fields = {
        "Sales": ["Marketing", "Life Sciences", "Other"],
        "Research & Development": ["Life Sciences", "Medical", "Technical Degree", "Other"],
        "Human Resources": ["Human Resources", "Other"],
    }
    education_field = np.array([rng.choice(fields[d]) for d in department])

    age = rng.integers(18, 60, size=n)
    total_working_years = np.clip(age - 18 - rng.integers(0, 6, size=n), 0, None)
    years_at_company = np.minimum(total_working_years, rng.gamma(2.0, 3.0, size=n).astype(int))
    monthly_income = (2000 + total_working_years * 300 + rng.normal(0, 1200, size=n)).clip(1009, 19999).round(0)
    job_satisfaction = rng.integers(1, 5, size=n)
    work_life_balance = rng.integers(1, 5, size=n)
    environment_satisfaction = rng.integers(1, 5, size=n)
    distance = rng.integers(1, 30, size=n)

    logit = (
        -2.4
        + 0.9 * (work_life_balance == 1)
        + 0.9 * (years_at_company < 2)
        + 0.7 * (monthly_income < 3000)
        + 0.5 * (job_satisfaction == 1)
        + 0.3 * (department == "Sales")
        + 0.02 * (distance - 10)
    )
    prob = 1 / (1 + np.exp(-logit))
    attrition = np.where(rng.random(n) < prob, "Yes", "No")

    return pd.DataFrame(
        {
            "Age": age,
            "Attrition": attrition,
            "Department": department,
            "DistanceFromHome": distance,
            "Education": rng.integers(1, 6, size=n),
            "EducationField": education_field,
            "EnvironmentSatisfaction": environment_satisfaction,
            "JobSatisfaction": job_satisfaction,
            "MaritalStatus": rng.choice(["Single", "Married", "Divorced"], size=n),
            "MonthlyIncome": monthly_income,
            "NumCompaniesWorked": rng.integers(0, 9, size=n),
            "WorkLifeBalance": work_life_balance,
            "YearsAtCompany": years_at_company,
        }
    )
