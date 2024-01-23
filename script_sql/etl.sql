
INSERT INTO salary_per_hour (year, month, branch_id, salary_per_hour)
WITH summary AS (
    SELECT 
        strftime('%Y', t.date) AS year,
        strftime('%m', t.date) AS month,
        e.branch_id,
        t.employee_id,
        SUM(e.salary) AS salary_total,
        SUM(
            COALESCE(
                (strftime('%s', t.checkout) - strftime('%s', t.checkin)) / 3600,
                8
            )
        ) AS working_hours_total
    FROM
        timesheets t
    LEFT JOIN
        employees e ON t.employee_id = e.employee_id
    WHERE
        t.date IS NOT NULL
    GROUP BY
        year,
        month,
        branch_id
)

SELECT
    year,
    month,
    branch_id,
    ROUND(salary_total / working_hours_total, 2) AS salary_per_hour
FROM
    summary;
