# Credit Risk Score Calculation (Rule-Based Method)

def calculate_credit_score(age, monthly_income, gold_weight_g, gold_purity, 
                          market_value_inr, ltv_ratio, loan_amount_inr, 
                          tenure_months, past_defaults, occ_score, debt_to_income):
    """
    Calculate credit risk score (1-100) using rule-based formula.
    Higher score = Lower risk
    """
    # Normalize inputs
    D = min(past_defaults / 5, 1)
    DTI = min(debt_to_income / 2, 1)
    LTV = ltv_ratio / 100
    INC = min(monthly_income / 100000, 1)
    OCC = occ_score
    
    # Calculate risk factor
    risk_factor = 0.30 * D + 0.25 * DTI + 0.20 * LTV - 0.15 * INC - 0.10 * OCC
    
    # Convert to 1-100 score
    score = round(100 * (1 - risk_factor))
    
    # Clamp to [1, 100]
    score = max(1, min(100, score))
    
    return score
    
   # occ_score [Professional: 0.95,Salaried: 0.85,Small Business: 0.70,Farmer: 0.60,Daily Wage: 0.40]