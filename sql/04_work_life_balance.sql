-- Attrition by work-life balance score (1 = poor, 4 = best).
SELECT
    WorkLifeBalance                                    AS work_life_balance,
    COUNT(*)                                           AS headcount,
    SUM(attrition_flag)                                AS leavers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 1)   AS attrition_rate_pct
FROM v_employees
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance;