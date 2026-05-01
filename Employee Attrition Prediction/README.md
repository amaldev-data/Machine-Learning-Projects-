#  HR Attrition Prediction Pipeline

##  Project Overview
Employee turnover is expensive. This project applies high-level Data Science techniques to `HRDataset.csv` to predict employee attrition (Churn/Termination) before it happens. 

Instead of just predicting *who* will leave, this project focuses on **Explainable AI**, identifying the *mathematical drivers* (Feature Importance) behind why employees quit, allowing HR to make data-driven retention strategies.

##  Business Objective
*   **Target Variable:** `Termd` (1 = Terminated, 0 = Active)
*   **Primary Metric:** **Recall (Class 1)**. In HR analytics, it is better to falsely flag an employee as a flight risk (False Positive) than to completely miss an employee who is about to quit (False Negative).

##  Data Engineering & Preprocessing
To ensure the model learns from behavior rather than "cheating," rigorous data preparation was applied:

### 1. Feature Engineering
*   **Tenure:** Calculated as days between Hire Date and the Snapshot Date (or Termination Date).
*   **Age_At_Review:** Calculated to understand the lifecycle stage of the employee during their last performance cycle.
  
### 2. Data Leakage Prevention (Pruning)
The following features were strictly dropped before training to prevent Data Leakage (where the model knows the future):
*    `DateofTermination`
*    `EmploymentStatus`
*    `DateofHire`
*    `ManagerName` (Used `ManagerID` instead)

### 3. The Final Feature Set
*   **Numerical:** `Salary`, `EngagementSurvey`, `EmpSatisfaction`, `SpecialProjectsCount`, `DaysLateLast30`, `Absences`, `Age_At_Review`, `Tenure`.
*   **Nominal:** `Position`, `Sex`, `MaritalDesc`, `Department`, `ManagerID`.
*   **Ordinal:** `PerformanceScore` (Mapped: PIP < Needs Improvement < Fully Meets < Exceeds).

##  Exploratory Data Analysis (EDA)
A hypothesis-driven EDA was conducted focusing on the target variable. Visualizations include:
*   **Target-Focused Correlation Heatmap:** Isolated to see which features directly correlate with attrition.
*   **Lifecycle Analysis:** KDE plots tracking Attrition spikes against `Tenure`.
*   **Managerial Impact:** Churn-rate analysis grouped by Top 10 Managers.
*   **Behavioral Red Flags:** Scatter plots tracking `Absences` vs `DaysLateLast30`.

##  Machine Learning Pipeline (The "Bake-Off")
Built a robust `scikit-learn` Pipeline using `ColumnTransformer` (StandardScaler, OneHotEncoder, OrdinalEncoder) to handle preprocessing dynamically. Addressed class imbalance (~33% attrition) using `class_weight='balanced'`.

Two models were tested head-to-head:
1.  **Logistic Regression (Baseline):** Used for its high explainability and linear coefficient transparency.
2.  **Random Forest Classifier (Champion):** Built with 100 decision trees (`n_estimators=100`). Selected as the final model due to its ability to capture non-linear behavioral patterns and output clear **Feature Importances**.

