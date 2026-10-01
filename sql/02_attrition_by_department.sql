-- Attrition rate per department, ranked highest first.
SELECT
    Department                                         AS department,
    COUNT(*)                                           AS headcount,
    SUM(attrition_flag)                                AS leavers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 1)   AS attrition_rate_pct,
    RANK() OVER (ORDER BY 1.0 * SUM(attrition_flag) / COUNT(*) DESC) AS risk_rank
FROM v_employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;
