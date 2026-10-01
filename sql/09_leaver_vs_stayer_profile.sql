-- Average profile of people who left versus people who stayed.
SELECT
    CASE WHEN Attrition = 'Yes' THEN 'Left' ELSE 'Stayed' END AS status,
    COUNT(*)                                       AS employees,
    ROUND(AVG(Age), 1)                             AS avg_age,
    ROUND(AVG(MonthlyIncome), 0)                   AS avg_monthly_income,
    ROUND(AVG(YearsAtCompany), 1)                  AS avg_tenure_yrs,
    ROUND(AVG(NumCompaniesWorked), 1)              AS avg_companies_worked,
    ROUND(AVG(DistanceFromHome), 1)                AS avg_distance_from_home
FROM v_employees
GROUP BY Attrition
ORDER BY status DESC;