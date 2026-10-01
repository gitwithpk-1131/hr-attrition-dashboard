-- KPI cards: headcount, leavers, attrition rate and a few context numbers.
SELECT
    COUNT(*)                                                    AS headcount,
    SUM(attrition_flag)                                         AS leavers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 1)            AS attrition_rate_pct,
    ROUND(AVG(YearsAtCompany), 1)                               AS avg_tenure_yrs,
    ROUND(AVG(MonthlyIncome), 0)                                AS avg_monthly_income,
    ROUND(100.0 * SUM(CASE WHEN WorkLifeBalance <= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS low_work_life_balance_pct,
    ROUND(AVG(JobSatisfaction), 2)                              AS avg_job_satisfaction
FROM v_employees;