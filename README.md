# 👥 HR Analytics — Employee Attrition Analysis

**Tools:** Python · Pandas · SQL · Power BI · Matplotlib · Seaborn  
**Domain:** Human Resources · People Analytics · Business Intelligence  
**Status:** Completed

---

## 📌 Project Overview

Analyzed **1,400+ employee records** to identify attrition patterns across departments, age groups, job roles, and satisfaction levels. Combined SQL for data aggregation, Python for statistical analysis, and Power BI for executive-ready dashboards — delivering actionable retention recommendations to HR leadership.

---

## 🎯 Objectives

- Quantify attrition rates by department, role, age, and tenure
- Identify the top factors driving employee attrition
- Validate findings using statistical hypothesis testing
- Deliver a Power BI dashboard for HR leadership to monitor attrition trends

---

## 📊 Key Findings

| Finding | Detail |
|---|---|
| Overall attrition rate | ~16% of 1,470 employees |
| Highest attrition dept | Sales (21%) |
| Most at-risk role | Sales Representative (40%+) |
| Tenure risk window | First 2 years — highest attrition |
| Key drivers | Low job satisfaction, overtime, monthly income, work-life balance |
| Distance effect | Employees living far from office 2× more likely to leave |

---

## 🗂️ Project Structure

```
hr-attrition-analysis/
│
├── data/
│   └── hr_attrition_sample.csv     # IBM HR Analytics-style sample dataset
│
├── notebooks/
│   ├── 01_data_exploration.py
│   ├── 02_attrition_analysis.py
│   └── 03_statistical_testing.py
│
├── sql/
│   └── hr_attrition_queries.sql
│
├── outputs/
│   └── figures/
│
├── requirements.txt
└── README.md
```

---

## 🔍 Approach

### 1. Data Exploration & Cleaning
- Integrated CSV exports with SQL-aggregated summaries into a unified Python dataframe
- Handled categorical encoding and missing value imputation
- Profiled 35 employee attributes including satisfaction scores, performance ratings, and compensation data

### 2. Attrition Analysis
- Computed attrition rates across departments, job levels, age groups, and tenure buckets
- Identified the "first 2 years" as the critical retention window across all departments
- Visualized key breakdowns using Seaborn bar charts, heatmaps, and box plots

### 3. Statistical Validation
- Applied **chi-squared tests** to confirm associations between categorical variables and attrition
- Used **Mann-Whitney U tests** to compare continuous variable distributions (income, age) between attrited and retained employees
- Validated all insights at p < 0.05 significance level

### 4. Power BI Dashboard
- Built a multi-page HR dashboard with attrition KPIs, department drill-downs, and satisfaction score breakdowns
- Added dynamic slicers for department, gender, job level, and age group
- Enabled HR leadership to monitor real-time headcount and attrition trends

### 5. Recommendations
- Targeted retention programs for Sales team (highest risk)
- Structured 6-month and 12-month check-ins for new hires
- Overtime policy review — strong correlation between overtime and attrition

---

## ⚙️ How to Run

```bash
git clone https://github.com/madhuri-sandhi/hr-attrition-analysis.git
cd hr-attrition-analysis
pip install -r requirements.txt
python notebooks/01_data_exploration.py
python notebooks/02_attrition_analysis.py
python notebooks/03_statistical_testing.py
```

---

## 📦 Requirements

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.9.0
jupyter>=1.0.0
```

---

## 💡 Key Learnings

- Attrition is rarely caused by a single factor — it's almost always a combination of satisfaction, compensation, and workload
- Statistical testing separates real patterns from noise — visual analysis alone can be misleading
- Dashboards for HR leadership need to prioritize **actionable** metrics over comprehensive ones — less is more
