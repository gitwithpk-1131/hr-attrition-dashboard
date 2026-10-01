# HR Attrition & Workforce Analytics Dashboard

An analytics project that uses SQL to find out who leaves a company, when, and what they have in
common. The results are shown in an interactive Streamlit dashboard, and every chart has a
"View the SQL behind this" box so the queries are easy to review.

## What it answers
- Which departments and education fields lose the most people?
- Which tenure bands (new joiners vs long-serving staff) have the highest attrition?
- Do work-life balance, income and job satisfaction relate to people leaving?
- Which department and tenure combinations are the riskiest?
- How do leavers differ from stayers?

## KPIs built
| KPI | Definition |
|---|---|
| Headcount | Number of employee records |
| Leavers | Employees with Attrition = Yes |
| Attrition rate | Leavers / headcount x 100 |
| Attrition rate by department, education field, tenure band, income quartile, work-life balance, satisfaction score | Same rate, per group |
| Low work-life balance share | Employees scoring 1-2 / headcount x 100 |
| Average tenure, average monthly income, average job satisfaction | Context numbers |
| Times company average | A segment's attrition rate divided by the company rate |

## SQL used
All queries are in `sql/`. They use `CASE` and the `NTILE` window function to build bands, `GROUP BY` and `HAVING` for segments,
a `RANK()` window function, a CTE with a `CROSS JOIN` to compare segments with the company
average, and a view (`v_employees`) that adds the helper columns.

| File | Purpose |
|---|---|
| 00_schema.sql | View with attrition flag, tenure and age bands, income quartiles (NTILE) |
| 01_headline_kpis.sql | Headline KPIs |
| 02_attrition_by_department.sql | Department attrition with a risk rank |
| 03_attrition_by_tenure_band.sql | Attrition by tenure |
| 04_work_life_balance.sql | Attrition by work-life balance score |
| 05_education_field_risk.sql | Education fields with 20+ people |
| 06_income_band.sql | Attrition by income quartile |
| 07_job_satisfaction.sql | Attrition by satisfaction score |
| 08_high_risk_segments.sql | Department x tenure hot spots vs company average |
| 09_leaver_vs_stayer_profile.sql | Average profile of leavers vs stayers |

## Project structure
```
hr-attrition-dashboard/
├── app.py                  # Streamlit dashboard
├── sql/                    # all SQL queries
├── src/
│   ├── db.py               # loads data into SQLite, runs the .sql files
│   ├── insights.py         # turns query results into written findings
│   └── sample_data.py      # synthetic fallback data
├── data/raw/               # put hr_attrition.csv here
├── requirements.txt
└── README.md
```

## Data
Download an IBM-style HR attrition dataset from Kaggle (unzip it) and save it as
`data/raw/hr_attrition.csv`. It needs these columns: Age, Attrition, Department, EducationField,
MonthlyIncome, WorkLifeBalance, YearsAtCompany, NumCompaniesWorked, DistanceFromHome, JobSatisfaction. If the file is missing, a synthetic sample is used and the
dashboard shows a warning banner.

## Run it on your computer
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Other useful commands:
```
python -m src.insights    # writes INSIGHTS.md with the written findings
python -m src.db          # writes data/hr.db to open in DB Browser for SQLite
```

## Put it online (free)
1. Push this folder to a GitHub repo.
2. Go to share.streamlit.io, sign in with GitHub, click New app.
3. Pick the repo, branch `main`, main file `app.py`, then Deploy.

## Key insights
Run `python -m src.insights` on the real dataset and paste the findings here, for example the
department with the highest attrition, the riskiest tenure band, and the work-life balance gap.

## Using Power BI or Tableau
The same CSV (or `data/hr.db`) can be connected to Power BI or Tableau, and the queries in `sql/`
can be reused as custom queries.
