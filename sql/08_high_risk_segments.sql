-- Department x tenure-band combinations, compared with the company average.
-- Uses a CTE and a CROSS JOIN. Segments under 15 people are ignored.
WITH company AS (
    SELECT 1.0 * SUM(attrition_flag) / COUNT(*) AS rate
    FROM v_employees
),
segments AS (
    SELECT
        Department                                AS department,
        tenure_band,
        COUNT(*)                                  AS headcount,
        SUM(attrition_flag)                       AS leavers,
        1.0 * SUM(attrition_flag) / COUNT(*)      AS rate
    FROM v_employees
    GROUP BY Department, tenure_band
    HAVING COUNT(*) >= 15
)
SELECT
    s.department,
    s.tenure_band,
    s.headcount,
    s.leavers,
    ROUND(100 * s.rate, 1)                        AS attrition_rate_pct,
    ROUND(s.rate / NULLIF(c.rate, 0), 2)          AS times_company_avg
FROM segments s
CROSS JOIN company c
ORDER BY s.rate DESC
LIMIT 10;
