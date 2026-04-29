from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from creditscore import calculate_credit_score

app = FastAPI()



# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
model = joblib.load('Loan_credit_model.pkl')

class LoanApplication(BaseModel):
    Age: int
    Monthly_Income: float
    Gold_Weight_g: float
    Gold_Purity: int
    Market_Value_INR: float
    Loan_Amount_INR: float
    Tenure_Months: int
    Past_Defaults: int
    Occupation: str

occupation_map = {
    'Professional': 0.95,
    'Salaried': 0.85,
    'Small Business': 0.70,
    'Farmer': 0.60,
    'Daily Wage': 0.40
}

def engineer_features(application: LoanApplication):
    occ_score = occupation_map.get(application.Occupation, 0.55)
    
    if application.Market_Value_INR > 0:
        ltv_ratio = (application.Loan_Amount_INR / application.Market_Value_INR) * 100
    else:
        ltv_ratio = 0
        
    if application.Monthly_Income > 0:
        debt_to_income = application.Loan_Amount_INR / (application.Monthly_Income * 12)
    else:
        debt_to_income = 0
        
    credit_score = calculate_credit_score(
        age=application.Age,
        monthly_income=application.Monthly_Income,
        gold_weight_g=application.Gold_Weight_g,
        gold_purity=application.Gold_Purity,
        market_value_inr=application.Market_Value_INR,
        ltv_ratio=ltv_ratio,
        loan_amount_inr=application.Loan_Amount_INR,
        tenure_months=application.Tenure_Months,
        past_defaults=application.Past_Defaults,
        occ_score=occ_score,
        debt_to_income=debt_to_income
    )
    
    return occ_score, ltv_ratio, debt_to_income, credit_score

@app.post("/predict")
def predict_risk(application: LoanApplication):
    occ_score, ltv_ratio, debt_to_income, credit_score = engineer_features(application)
    
    # Prepare model input
    input_data = pd.DataFrame([{
        'Age': application.Age,
        'Monthly_Income': application.Monthly_Income,
        'Gold_Weight_g': application.Gold_Weight_g,
        'Gold_Purity': application.Gold_Purity,
        'Market_Value_INR': application.Market_Value_INR,
        'LTV_Ratio': ltv_ratio,
        'Loan_Amount_INR': application.Loan_Amount_INR,
        'Tenure_Months': application.Tenure_Months,
        'Past_Defaults': application.Past_Defaults,
        'occ_score': occ_score,
        'Debt_to_Income': debt_to_income
    }])
    
    # Predict using the model
    prediction = int(model.predict(input_data)[0])
    
    # Calculate risk probability (Probability of default, i.e., class 1)
    probabilities = model.predict_proba(input_data)[0]
    if len(probabilities) > 1:
        risk_probability = float(probabilities[1]) * 100
    else:
        risk_probability = 100.0 if prediction == 1 else 0.0
        
    # Determine Risk Level and Color based on 5 levels
    if credit_score <= 20:
        risk_level = "High Risk"
        color = "Dark Red"
    elif credit_score <= 40:
        risk_level = "Medium-High Risk"
        color = "Red"
    elif credit_score <= 60:
        risk_level = "Medium Risk"
        color = "Orange"
    elif credit_score <= 80:
        risk_level = "Low-Medium Risk"
        color = "Yellow"
    else:
        risk_level = "Low Risk"
        color = "Green"
        
    # Approval logic based on user prompt: 0 -> Approve, 1 -> Reject
    status = "Approve" if prediction == 0 else "Reject"
    status_color = "Green" if prediction == 0 else "Red"
    
    return {
        "status": status,
        "status_color": status_color,
        "credit_score": credit_score,
        "risk_probability": round(risk_probability, 1),
        "risk_level": risk_level,
        "color": color,
        "ltv_ratio": round(ltv_ratio, 1),
        "debt_to_income": round(debt_to_income * 100, 1) # return as percentage
    }

@app.post("/calculate_live")
def calculate_live(application: LoanApplication):
    _, ltv_ratio, debt_to_income, credit_score = engineer_features(application)
    
    return {
        "ltv_ratio": round(ltv_ratio, 1),
        "debt_to_income": round(debt_to_income * 100, 1),
        "credit_score": credit_score
    }
