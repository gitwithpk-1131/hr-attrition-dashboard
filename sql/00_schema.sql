-- View that adds the helper columns every other query uses.
-- Income bands are quartiles (NTILE), so they work whatever the income scale is.
DROP VIEW IF EXISTS v_employees;

CREATE VIEW v_employees AS
SELECT
    e.*,
    CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END AS attrition_flag,
    CASE
        WHEN YearsAtCompany < 2  THEN '0-1 yrs'
        WHEN YearsAtCompany < 5  THEN '2-4 yrs'
        WHEN YearsAtCompany < 10 THEN '5-9 yrs'
        ELSE '10+ yrs'
    END AS tenure_band,
    CASE
        WHEN Age < 30 THEN 'Under 30'
        WHEN Age < 40 THEN '30-39'
        WHEN Age < 50 THEN '40-49'
        ELSE '50+'
    END AS age_band,
    CASE NTILE(4) OVER (ORDER BY MonthlyIncome)
        WHEN 1 THEN 'Q1 (lowest 25%)'
        WHEN 2 THEN 'Q2'
        WHEN 3 THEN 'Q3'
        ELSE 'Q4 (highest 25%)'
    END AS income_band
FROM employees e;