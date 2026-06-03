-- ────────────────────────────────────────────────────
-- HR Analytics — Attrition Analysis SQL Queries
-- Author: Madhuri Sandhi
-- ────────────────────────────────────────────────────


-- 1. Overall attrition rate
SELECT
    COUNT(*)                                              AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)   AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2
    )                                                     AS attrition_rate_pct
FROM hr_employees;


-- 2. Attrition by department
SELECT
    department,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)   AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2
    )                                                     AS attrition_rate_pct
FROM hr_employees
GROUP BY department
ORDER BY attrition_rate_pct DESC;


-- 3. Attrition by job role
SELECT
    job_role,
    department,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)   AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2
    )                                                     AS attrition_rate_pct,
    ROUND(AVG(monthly_income), 0)                         AS avg_monthly_income,
    ROUND(AVG(job_satisfaction), 2)                       AS avg_job_satisfaction
FROM hr_employees
GROUP BY job_role, department
ORDER BY attrition_rate_pct DESC;


-- 4. Attrition by tenure bucket (critical retention windows)
SELECT
    CASE
        WHEN years_at_company <= 1  THEN '0-1 Year'
        WHEN years_at_company <= 3  THEN '2-3 Years'
        WHEN years_at_company <= 7  THEN '4-7 Years'
        WHEN years_at_company <= 15 THEN '8-15 Years'
        ELSE '15+ Years'
    END                                                   AS tenure_bucket,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)   AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2
    )                                                     AS attrition_rate_pct
FROM hr_employees
GROUP BY
    CASE
        WHEN years_at_company <= 1  THEN '0-1 Year'
        WHEN years_at_company <= 3  THEN '2-3 Years'
        WHEN years_at_company <= 7  THEN '4-7 Years'
        WHEN years_at_company <= 15 THEN '8-15 Years'
        ELSE '15+ Years'
    END
ORDER BY MIN(years_at_company);


-- 5. Impact of overtime on attrition
SELECT
    overtime,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)   AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2
    )                                                     AS attrition_rate_pct,
    ROUND(AVG(monthly_income), 0)                         AS avg_income,
    ROUND(AVG(work_life_balance), 2)                      AS avg_work_life_balance
FROM hr_employees
GROUP BY overtime
ORDER BY attrition_rate_pct DESC;


-- 6. Job satisfaction vs attrition cross-tab
SELECT
    job_satisfaction,
    COUNT(*)                                              AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)   AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2
    )                                                     AS attrition_rate_pct,
    ROUND(AVG(monthly_income), 0)                         AS avg_monthly_income
FROM hr_employees
GROUP BY job_satisfaction
ORDER BY job_satisfaction;


-- 7. High-risk employee profile — for proactive HR intervention
SELECT
    employee_id,
    department,
    job_role,
    age,
    years_at_company,
    monthly_income,
    job_satisfaction,
    work_life_balance,
    overtime,
    distance_from_home,
    -- Risk score (higher = more at risk)
    (
        CASE WHEN overtime = 'Yes'           THEN 2 ELSE 0 END
      + CASE WHEN job_satisfaction <= 2      THEN 2 ELSE 0 END
      + CASE WHEN work_life_balance <= 2     THEN 2 ELSE 0 END
      + CASE WHEN years_at_company <= 2      THEN 1 ELSE 0 END
      + CASE WHEN distance_from_home > 20    THEN 1 ELSE 0 END
      + CASE WHEN monthly_income < 3000      THEN 1 ELSE 0 END
    )                                                     AS risk_score
FROM hr_employees
WHERE attrition = 'No'
ORDER BY risk_score DESC;
