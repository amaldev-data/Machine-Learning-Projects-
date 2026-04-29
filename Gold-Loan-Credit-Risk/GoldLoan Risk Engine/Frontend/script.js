const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById('loanForm');
const inputs = form.querySelectorAll('input, select');
const needle = document.getElementById('gauge-needle');

const probValue = document.getElementById('prob-value');
const probStatus = document.getElementById('prob-status');
const ltvValue = document.getElementById('ltv-value');
const ltvStatus = document.getElementById('ltv-status');
const dtiValue = document.getElementById('dti-value');
const dtiStatus = document.getElementById('dti-status');

const recCard = document.getElementById('recommendation-card');
const recStatus = document.getElementById('rec-status');

const analysisId = document.getElementById('analysis-id');
const timestamp = document.getElementById('timestamp');

// Helper to gather form data
function getFormData() {
    return {
        Age: parseInt(document.getElementById('age').value) || 0,
        Monthly_Income: parseFloat(document.getElementById('monthly_income').value) || 0,
        Gold_Weight_g: parseFloat(document.getElementById('gold_weight_g').value) || 0,
        Gold_Purity: parseInt(document.getElementById('gold_purity').value) || 22,
        Market_Value_INR: parseFloat(document.getElementById('market_value_inr').value) || 0,
        Loan_Amount_INR: parseFloat(document.getElementById('loan_amount_inr').value) || 0,
        Tenure_Months: parseInt(document.getElementById('tenure_months').value) || 18,
        Past_Defaults: parseInt(document.querySelector('input[name="past_defaults"]:checked').value),
        Occupation: document.getElementById('occupation').value
    };
}

// Format numbers
function formatPercent(val) {
    return val.toFixed(1);
}

function updateColorClass(element, riskLevel) {
    element.className = 'metric-status'; // Reset
    if (riskLevel.includes('Low')) {
        element.classList.add('status-green');
    } else if (riskLevel.includes('High') && !riskLevel.includes('Medium')) {
        element.classList.add('status-red');
    } else if (riskLevel.includes('Medium') && riskLevel.includes('High')) {
        element.classList.add('status-orange');
    } else {
        element.classList.add('status-yellow');
    }
}

// Live Update
let debounceTimer;
inputs.forEach(input => {
    input.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(async () => {
            try {
                const data = getFormData();
                const response = await fetch(`${API_URL}/calculate_live`, { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    
                    // Update live values (but not score/risk to full predict logic unless wanted)
                    ltvValue.textContent = formatPercent(result.ltv_ratio);
                    dtiValue.textContent = formatPercent(result.debt_to_income);
                    
                    if (result.ltv_ratio <= 75) {
                        ltvStatus.textContent = 'Healthy LTV';
                        ltvStatus.className = 'metric-status status-green';
                    } else {
                        ltvStatus.textContent = 'High LTV';
                        ltvStatus.className = 'metric-status status-red';
                    }

                    if (result.debt_to_income <= 40) {
                        dtiStatus.textContent = 'Good DTI';
                        dtiStatus.className = 'metric-status status-green';
                    } else {
                        dtiStatus.textContent = 'High DTI';
                        dtiStatus.className = 'metric-status status-red';
                    }
                }
            } catch (error) {
                console.error("Live calculation failed", error);
            }
        }, 500); // 500ms debounce
    });
});

// Form Submission (Predict)
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Generate a mock ID and timestamp
    const randomId = Math.floor(Math.random() * 900000) + 100000;
    analysisId.textContent = `Analysis ID: GLR-${randomId}`;
    
    const now = new Date();
    timestamp.textContent = `Timestamp: ${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
    
    const submitBtn = form.querySelector('.submit-btn');
    submitBtn.textContent = 'ANALYZING...';
    submitBtn.disabled = true;

    try {
        const data = getFormData();
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Update Needle Rotation (-90 to 90 degrees)
            const score = Math.max(0, Math.min(100, result.credit_score));
            const rotation = ((50 - score) / 50) * 90;
            needle.style.transform = `rotate(${rotation}deg)`;
            
            // Update Metrics
            probValue.textContent = formatPercent(result.risk_probability);
            probStatus.textContent = result.risk_level;
            updateColorClass(probStatus, result.risk_level);
            
            ltvValue.textContent = formatPercent(result.ltv_ratio);
            if (result.ltv_ratio <= 75) {
                ltvStatus.textContent = 'Healthy LTV';
                ltvStatus.className = 'metric-status status-green';
            } else {
                ltvStatus.textContent = 'High LTV';
                ltvStatus.className = 'metric-status status-red';
            }

            dtiValue.textContent = formatPercent(result.debt_to_income);
            if (result.debt_to_income <= 40) {
                dtiStatus.textContent = 'Good DTI';
                dtiStatus.className = 'metric-status status-green';
            } else {
                dtiStatus.textContent = 'High DTI';
                dtiStatus.className = 'metric-status status-red';
            }

            // Update Recommendation Card
            recCard.className = 'recommendation-card'; // Reset
            if (result.status === 'Approve') {
                recCard.classList.add('approve');
                recStatus.textContent = 'Approve (Not Default)';
                recStatus.style.color = '#2e7d32';
            } else {
                recCard.classList.add('reject');
                recStatus.textContent = 'Reject (Default Risk)';
                recStatus.style.color = '#c62828';
            }
        } else {
            alert('Error from server during prediction');
        }
    } catch (error) {
        console.error("Prediction failed", error);
        alert('Could not connect to the server. Is it running?');
    } finally {
        submitBtn.textContent = 'ANALYZE CREDIT RISK';
        submitBtn.disabled = false;
    }
});

// Trigger initial live calculation removed to keep metrics vacant by default

