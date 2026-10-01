-- Attrition by job satisfaction score (1 = low, 4 = high).
SELECT
    JobSatisfaction                                    AS job_satisfaction,
    COUNT(*)                                           AS headcount,
    SUM(attrition_flag)                                AS leavers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 1)   AS attrition_rate_pct
FROM v_employees
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;
