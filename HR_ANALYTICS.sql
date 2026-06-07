CREATE TABLE hr_attrition (
    EmployeeID INT PRIMARY KEY,
    Age INT,
    Gender VARCHAR(10),
    Department VARCHAR(50),
    JobRole VARCHAR(50),
    EducationField VARCHAR(50),
    MonthlyIncome INT,
    YearsAtCompany INT,
    YearsInCurrentRole INT,
    YearsSinceLastPromotion INT,
    OverTime VARCHAR(5),
    JobSatisfaction INT,
    WorkLifeBalance INT,
    EnvironmentSatisfaction INT,
    PerformanceRating INT,
    Attrition VARCHAR(5)
);

-- ============================================================
-- STEP 2: BASIC EXPLORATION
-- ============================================================

-- Total Employees
SELECT COUNT(*) AS Total_Employees FROM hr_attrition;

-- Attrition Count & Rate
SELECT 
    Attrition,
    COUNT(*) AS Count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_attrition), 2) AS Percentage
FROM hr_attrition
GROUP BY Attrition;

-- ============================================================
-- STEP 3: DEPARTMENT-WISE ATTRITION
-- ============================================================

SELECT 
    Department,
    COUNT(*) AS Total_Employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM hr_attrition
GROUP BY Department
ORDER BY Attrition_Rate DESC;

-- ============================================================
-- STEP 4: AGE GROUP ATTRITION ANALYSIS
-- ============================================================

SELECT 
    CASE 
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 45 THEN '36-45'
        ELSE '46+' 
    END AS Age_Group,
    COUNT(*) AS Total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM hr_attrition
GROUP BY Age_Group
ORDER BY Attrition_Rate DESC;

-- ============================================================
-- STEP 5: SALARY vs ATTRITION
-- ============================================================

SELECT 
    CASE 
        WHEN MonthlyIncome < 30000 THEN 'Low (<30K)'
        WHEN MonthlyIncome BETWEEN 30000 AND 60000 THEN 'Mid (30K-60K)'
        ELSE 'High (60K+)' 
    END AS Salary_Band,
    COUNT(*) AS Total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Left_Count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM hr_attrition
GROUP BY Salary_Band
ORDER BY Attrition_Rate DESC;

-- ============================================================
-- STEP 6: OVERTIME IMPACT ON ATTRITION
-- ============================================================

SELECT 
    OverTime,
    COUNT(*) AS Total_Employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM hr_attrition
GROUP BY OverTime;

-- ============================================================
-- STEP 7: JOB SATISFACTION vs ATTRITION
-- ============================================================

SELECT 
    JobSatisfaction,
    COUNT(*) AS Total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Left,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM hr_attrition
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;

-- ============================================================
-- STEP 8: YEARS AT COMPANY vs ATTRITION (CTE)
-- ============================================================

WITH tenure_analysis AS (
    SELECT 
        CASE 
            WHEN YearsAtCompany <= 2 THEN '0-2 Years'
            WHEN YearsAtCompany BETWEEN 3 AND 5 THEN '3-5 Years'
            WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 Years'
            ELSE '10+ Years'
        END AS Tenure_Group,
        Attrition
    FROM hr_attrition
)
SELECT 
    Tenure_Group,
    COUNT(*) AS Total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM tenure_analysis
GROUP BY Tenure_Group
ORDER BY Attrition_Rate DESC;

-- ============================================================
-- STEP 9: TOP HIGH-RISK EMPLOYEES (WINDOW FUNCTION)
-- ============================================================

SELECT 
    EmployeeID,
    Department,
    JobRole,
    MonthlyIncome,
    JobSatisfaction,
    YearsSinceLastPromotion,
    OverTime,
    RANK() OVER (PARTITION BY Department ORDER BY YearsSinceLastPromotion DESC) AS Risk_Rank
FROM hr_attrition
WHERE Attrition = 'No'
  AND JobSatisfaction <= 2
  AND OverTime = 'Yes'
ORDER BY Risk_Rank;

-- ============================================================
-- STEP 10: GENDER-WISE ATTRITION
-- ============================================================

SELECT 
    Gender,
    COUNT(*) AS Total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Attrition_Count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM hr_attrition
GROUP BY Gender;
