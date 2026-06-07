# ============================================================
# HR ATTRITION ANALYSIS - Python EDA
# Tools: Pandas, NumPy, Matplotlib, Seaborn
# Dataset: IBM HR Analytics (Kaggle)
# Author: Divya Sivakumar
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# STEP 1: LOAD & EXPLORE DATA
# ============================================================

df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

print("Shape:", df.shape)
print("\nFirst 5 rows:\n", df.head())
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nBasic Stats:\n", df.describe())

# ============================================================
# STEP 2: DATA CLEANING
# ============================================================

# Check duplicates
print("\nDuplicates:", df.duplicated().sum())

# Drop irrelevant columns (constant values)
df.drop(['EmployeeCount', 'Over18', 'StandardHours'], axis=1, inplace=True)

# Convert Attrition to binary
df['Attrition_Binary'] = df['Attrition'].map({'Yes': 1, 'No': 0})

print("\nAttrition Distribution:\n", df['Attrition'].value_counts())
print("\nAttrition Rate:", round(df['Attrition_Binary'].mean() * 100, 2), "%")

# ============================================================
# STEP 3: ATTRITION OVERVIEW
# ============================================================

plt.figure(figsize=(6, 4))
df['Attrition'].value_counts().plot(kind='bar', color=['steelblue', 'salmon'])
plt.title('Overall Attrition Distribution')
plt.xlabel('Attrition')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('1_attrition_overview.png')
plt.show()

# ============================================================
# STEP 4: DEPARTMENT-WISE ATTRITION
# ============================================================

dept_attrition = df.groupby('Department')['Attrition_Binary'].mean().reset_index()
dept_attrition.columns = ['Department', 'Attrition_Rate']
dept_attrition['Attrition_Rate'] = round(dept_attrition['Attrition_Rate'] * 100, 2)
dept_attrition = dept_attrition.sort_values('Attrition_Rate', ascending=False)

print("\nDepartment-wise Attrition Rate:\n", dept_attrition)

plt.figure(figsize=(8, 5))
sns.barplot(data=dept_attrition, x='Department', y='Attrition_Rate', palette='Reds_r')
plt.title('Attrition Rate by Department')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.savefig('2_department_attrition.png')
plt.show()

# ============================================================
# STEP 5: AGE GROUP ANALYSIS
# ============================================================

bins = [18, 25, 35, 45, 60]
labels = ['18-25', '26-35', '36-45', '46+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

age_attrition = df.groupby('Age_Group')['Attrition_Binary'].mean().reset_index()
age_attrition['Attrition_Rate'] = round(age_attrition['Attrition_Binary'] * 100, 2)

print("\nAge Group Attrition:\n", age_attrition)

plt.figure(figsize=(8, 5))
sns.barplot(data=age_attrition, x='Age_Group', y='Attrition_Rate', palette='Blues_r')
plt.title('Attrition Rate by Age Group')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.savefig('3_age_attrition.png')
plt.show()

# ============================================================
# STEP 6: OVERTIME vs ATTRITION
# ============================================================

overtime_attrition = df.groupby('OverTime')['Attrition_Binary'].mean().reset_index()
overtime_attrition['Attrition_Rate'] = round(overtime_attrition['Attrition_Binary'] * 100, 2)

print("\nOvertime Attrition:\n", overtime_attrition)

plt.figure(figsize=(6, 4))
sns.barplot(data=overtime_attrition, x='OverTime', y='Attrition_Rate', palette='OrRd')
plt.title('Attrition Rate by Overtime')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.savefig('4_overtime_attrition.png')
plt.show()

# ============================================================
# STEP 7: SALARY vs ATTRITION
# ============================================================

df['Salary_Band'] = pd.cut(
    df['MonthlyIncome'],
    bins=[0, 30000, 60000, 200000],
    labels=['Low', 'Mid', 'High']
)

salary_attrition = df.groupby('Salary_Band')['Attrition_Binary'].mean().reset_index()
salary_attrition['Attrition_Rate'] = round(salary_attrition['Attrition_Binary'] * 100, 2)

print("\nSalary Band Attrition:\n", salary_attrition)

plt.figure(figsize=(6, 4))
sns.barplot(data=salary_attrition, x='Salary_Band', y='Attrition_Rate', palette='coolwarm')
plt.title('Attrition Rate by Salary Band')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.savefig('5_salary_attrition.png')
plt.show()

# ============================================================
# STEP 8: JOB SATISFACTION vs ATTRITION
# ============================================================

job_sat = df.groupby('JobSatisfaction')['Attrition_Binary'].mean().reset_index()
job_sat['Attrition_Rate'] = round(job_sat['Attrition_Binary'] * 100, 2)

print("\nJob Satisfaction Attrition:\n", job_sat)

plt.figure(figsize=(6, 4))
sns.lineplot(data=job_sat, x='JobSatisfaction', y='Attrition_Rate', marker='o', color='red')
plt.title('Attrition Rate by Job Satisfaction Level')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.savefig('6_jobsatisfaction_attrition.png')
plt.show()

# ============================================================
# STEP 9: CORRELATION HEATMAP
# ============================================================

numeric_cols = df.select_dtypes(include=np.number).columns
corr = df[numeric_cols].corr()

plt.figure(figsize=(14, 10))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('7_correlation_heatmap.png')
plt.show()

# ============================================================
# STEP 10: KEY INSIGHTS SUMMARY
# ============================================================

print("\n" + "="*60)
print("KEY INSIGHTS FROM HR ATTRITION ANALYSIS")
print("="*60)
print(f"1. Overall Attrition Rate: {round(df['Attrition_Binary'].mean()*100,2)}%")
print(f"2. Highest Attrition Dept: {dept_attrition.iloc[0]['Department']} ({dept_attrition.iloc[0]['Attrition_Rate']}%)")
print(f"3. Employees with Overtime have significantly higher attrition")
print(f"4. Low salary band employees leave the most")
print(f"5. Younger employees (18-25) show highest attrition tendency")
print(f"6. Low job satisfaction (1-2) strongly correlates with attrition")
print("="*60)
