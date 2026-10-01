-- Attrition by monthly income band.
SELECT
    income_band,
    COUNT(*)                                           AS headcount,
    SUM(attrition_flag)                                AS leavers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 1)   AS attrition_rate_pct
FROM v_employees
GROUP BY income_band
ORDER BY MIN(MonthlyIncome);
