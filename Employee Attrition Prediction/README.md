HR Attrition Prediction Pipeline
Overview

Employee turnover is a significant cost driver for organizations. This project applies Data Science and Machine Learning techniques to predict employee attrition using HRDataset.csv.

The focus is not only on prediction but also on Explainable AI, identifying the key factors influencing employee churn. This allows HR teams to take proactive, data-driven retention actions.

Business Objective
Target Variable: Termd
1 → Terminated
0 → Active
Primary Metric: Recall (Class 1)

Rationale: Missing an employee who is likely to leave (False Negative) is more costly than incorrectly flagging a stable employee (False Positive).

Dataset

The dataset contains employee-level HR data, including:

Demographics
Job-related attributes
Performance metrics
Behavioral indicators
Data Engineering and Preprocessing
Feature Engineering
Snapshot Date: January 1, 2024
Tenure: Days between Hire Date and Snapshot (or Termination Date)
Age_At_Review: Age at last performance review
Century Fix: Corrected two-digit year parsing issues to avoid invalid ages
Data Leakage Prevention

The following columns were removed before training to avoid leakage:

DateofTermination
EmploymentStatus
DateofHire
ManagerName

ManagerID was retained as a structured proxy for managerial influence.

Final Feature Set
Numerical Features
Salary
EngagementSurvey
EmpSatisfaction
SpecialProjectsCount
DaysLateLast30
Absences
Age_At_Review
Tenure
Categorical Features

Nominal:

Position
Sex
MaritalDesc
Department
ManagerID

Ordinal:

PerformanceScore
PIP < Needs Improvement < Fully Meets < Exceeds
Exploratory Data Analysis

EDA was conducted with a strong focus on attrition behavior:

Correlation analysis targeting the attrition variable
Tenure-based lifecycle analysis using density plots
Manager-level churn comparisons
Behavioral risk patterns (Absences vs Days Late)
Machine Learning Pipeline

A modular pipeline was built using scikit-learn:

ColumnTransformer
StandardScaler → Numerical features
OneHotEncoder → Nominal features
OrdinalEncoder → Ordinal features
Class Imbalance Handling
class_weight='balanced' (~33% attrition rate)
Models Evaluated
1. Logistic Regression (Baseline)
High interpretability
Transparent coefficients
Serves as benchmark
2. Random Forest Classifier (Final Model)
100 decision trees (n_estimators=100)
Captures non-linear relationships
Provides feature importance for explainability
Model Selection

The Random Forest Classifier was selected due to:

Better recall on attrition class
Ability to model complex behavioral patterns
Built-in feature importance for decision support
Key Insights (Example Outputs)
High absenteeism and frequent lateness are strong predictors of attrition
Low engagement and satisfaction scores increase churn risk
Certain managers show consistently higher attrition rates
Early tenure phase shows higher exit probability
Tech Stack
Python
Pandas, NumPy
Matplotlib, Seaborn
Scikit-learn