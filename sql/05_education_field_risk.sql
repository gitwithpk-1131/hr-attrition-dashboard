-- Education fields with the highest attrition (groups of at least 20 people only,
-- so tiny groups do not distort the ranking).
SELECT
    EducationField                                     AS education_field,
    COUNT(*)                                           AS headcount,
    SUM(attrition_flag)                                AS leavers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 1)   AS attrition_rate_pct
FROM v_employees
GROUP BY EducationField
HAVING COUNT(*) >= 20
ORDER BY attrition_rate_pct DESC;