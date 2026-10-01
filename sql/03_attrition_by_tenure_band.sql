-- Attrition rate by how long people have been at the company.
SELECT
    tenure_band,
    COUNT(*)                                           AS headcount,
    SUM(attrition_flag)                                AS leavers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 1)   AS attrition_rate_pct
FROM v_employees
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany);
