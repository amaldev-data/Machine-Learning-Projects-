# ⚖️ Aurum Gold Loans — AI Credit Risk Assessment

> A high-fidelity FinTech web app that uses a trained **XGBoost classifier** to assess gold loan credit risk in real time. Built with **Streamlit** and styled to match the Aurum Gold Loans design system.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Features

- **AI Risk Verdict** — Platinum Tier Approved / Manual Review / High Risk Rejected
- **Credit Score Gauge** — Animated 300–900 score derived from XGBoost probability
- **Collateral Bar Chart** — LTV visualisation (Loan Amount vs Excess Gold Equity)
- **Risk Probability Chart** — Model confidence breakdown
- **Live Calculations** — LTV Ratio, Total Gold Value, Coverage Ratio update in real time

---

## 📁 Repository Structure

```
aurum-gold-loans/
│
├── app.py                  # Main Streamlit application
├── model.joblib            # Pre-trained XGBoost classifier  ← you must add this
├── scaler.joblib           # Fitted StandardScaler           ← you must add this
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🚀 Deploy on Streamlit Cloud (GitHub → Cloud)

### Step 1 — Prepare your GitHub Repository

1. Create a new **public** repository on [github.com](https://github.com).
2. Clone it locally:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

### Step 2 — Add the Project Files

Copy all four files into the cloned folder:

```
app.py
requirements.txt
model.joblib
scaler.joblib
README.md
```

> ⚠️ **Important:** Both `.joblib` files **must** be in the root of the repository alongside `app.py`. The app uses `os.path.dirname(__file__)` to locate them automatically.

### Step 3 — Push to GitHub

```bash
git add .
git commit -m "Initial commit — Aurum Gold Loans Credit Risk App"
git push origin main
```

### Step 4 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **"New app"**.
3. Fill in:
   - **Repository:** `<your-username>/<your-repo-name>`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"** — Streamlit will install dependencies and launch your app.
5. Your app will be live at:
   ```
   https://<your-app-name>.streamlit.app
   ```

---

## 💻 Run Locally

### Prerequisites

- Python **3.10 or higher**
- pip

### Step 1 — Clone the Repo

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### Step 2 — Create a Virtual Environment (recommended)

```bash
# Create
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Place Model Files

Ensure `model.joblib` and `scaler.joblib` are in the **same directory** as `app.py`.

```
your-project/
├── app.py
├── model.joblib      ✅
├── scaler.joblib     ✅
└── requirements.txt
```

### Step 5 — Launch the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🧠 Model Details

| Feature | Description |
|---|---|
| `Age` | Applicant age in years |
| `Monthly_Income` | Monthly income in INR |
| `Gold_Weight_g` | Weight of pledged gold in grams |
| `Gold_Purity` | Karat value (18, 20, 22, 24) |
| `Market_Value_INR` | Computed: Weight × Rate × (Purity/24) |
| `LTV_Ratio` | Loan-to-Value %: (Loan / Gold Value) × 100 |
| `Loan_Amount_INR` | Requested loan amount in INR |
| `Tenure_Months` | Loan tenure in months |
| `Past_Defaults` | Number of historical defaults |
| `occ_score` | Occupation risk score (0.25–1.00) |

### Occupation Score Mapping

| Occupation | Score |
|---|---|
| Government Employee | 1.00 |
| Salaried (Private Sector) | 0.90 |
| Business Owner | 0.75 |
| Self-Employed Professional | 0.68 |
| Farmer / Agriculture | 0.58 |
| Retired | 0.52 |
| Daily Wage Worker | 0.40 |
| Unemployed | 0.25 |

### Scoring Formula

```
Score = 900 − (P_default × 600)
```

Where `P_default` is the XGBoost probability of class `1` (high risk).

### Verdict Thresholds

| Verdict | Score | LTV |
|---|---|---|
| 🟢 APPROVED — PLATINUM TIER | ≥ 750 | < 80% |
| 🟡 MANUAL REVIEW REQUIRED | ≥ 600 | < 90% |
| 🔴 HIGH RISK — REJECTED | < 600 | any |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: xgboost` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: model.joblib` | Ensure both `.joblib` files are in the same directory as `app.py` |
| Version mismatch on `joblib` pickle | Retrain/re-export the model using the exact versions in `requirements.txt` |
| Streamlit Cloud deploy fails | Check that your repo is **public** and `requirements.txt` lists all dependencies |
| App loads but prediction errors | Check that your `model.joblib` was trained with the 10 features listed above in exact order |

---

## 📄 License

MIT — free to use, modify, and distribute.

---

*Built with ❤️ using Streamlit + XGBoost • Aurum Gold Loans © 2025*
