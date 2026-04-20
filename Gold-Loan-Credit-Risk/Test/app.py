import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Aurum Gold Loans | Credit Risk",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# THEME & GLOBAL CSS
# ──────────────────────────────────────────────
CREAM       = "#F5EFE6"
CHARCOAL    = "#1A2238"
GOLD        = "#C5A059"
GOLD_LIGHT  = "#D4B878"
WHITE       = "#FFFFFF"
CARD_BG     = "#FDFAF5"
BORDER      = "#E8DCC8"
GREEN       = "#2ECC71"
AMBER       = "#F39C12"
RED         = "#E74C3C"

st.markdown(f"""
<style>
  /* ── IMPORT FONT ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  /* ── ROOT ── */
  html, body, [class*="css"] {{
      font-family: 'Inter', sans-serif;
  }}
  .stApp {{
      background-color: {CREAM};
  }}

  /* ── SIDEBAR ── */
  [data-testid="stSidebar"] {{
      background-color: {CHARCOAL} !important;
      border-right: none;
  }}
  [data-testid="stSidebar"] * {{
      color: #E8DCC8 !important;
  }}
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stNumberInput label,
  [data-testid="stSidebar"] .stSlider label {{
      color: #C5A059 !important;
      font-weight: 600;
      font-size: 0.78rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
  }}
  [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {{
      padding-top: 4px;
  }}
  [data-testid="stSidebar"] .stButton > button {{
      background: linear-gradient(135deg, {GOLD} 0%, {GOLD_LIGHT} 100%) !important;
      color: {CHARCOAL} !important;
      font-weight: 700 !important;
      border: none !important;
      border-radius: 10px !important;
      width: 100% !important;
      padding: 14px !important;
      font-size: 1rem !important;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      box-shadow: 0 4px 20px rgba(197,160,89,0.4);
      transition: all 0.2s ease;
  }}
  [data-testid="stSidebar"] .stButton > button:hover {{
      transform: translateY(-1px);
      box-shadow: 0 6px 24px rgba(197,160,89,0.55);
  }}

  /* ── HIDE STREAMLIT CHROME ── */
  #MainMenu, footer, header {{visibility: hidden;}}
  .block-container {{padding-top: 1.5rem; padding-bottom: 2rem;}}

  /* ── CARDS ── */
  .aurum-card {{
      background: {WHITE};
      border-radius: 16px;
      padding: 24px 28px;
      box-shadow: 0 2px 16px rgba(26,34,56,0.07);
      border: 1px solid {BORDER};
      margin-bottom: 20px;
  }}
  .aurum-card-cream {{
      background: {CARD_BG};
      border-radius: 16px;
      padding: 24px 28px;
      box-shadow: 0 2px 12px rgba(26,34,56,0.05);
      border: 1px solid {BORDER};
      margin-bottom: 20px;
  }}

  /* ── STAT TILES ── */
  .stat-tile {{
      background: {WHITE};
      border-radius: 12px;
      padding: 18px 20px;
      border: 1px solid {BORDER};
      box-shadow: 0 1px 8px rgba(26,34,56,0.05);
  }}
  .stat-tile .label {{
      color: #888;
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 6px;
  }}
  .stat-tile .value {{
      color: {CHARCOAL};
      font-size: 1.55rem;
      font-weight: 700;
      line-height: 1.1;
  }}
  .stat-tile .sub {{
      color: {GOLD};
      font-size: 0.78rem;
      font-weight: 500;
      margin-top: 4px;
  }}

  /* ── SECTION HEADERS ── */
  .section-title {{
      color: {CHARCOAL};
      font-size: 1.1rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      margin-bottom: 4px;
  }}
  .section-sub {{
      color: #9A8F82;
      font-size: 0.8rem;
      margin-bottom: 20px;
  }}

  /* ── LOGO HEADER ── */
  .logo-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 8px 0 24px 0;
      border-bottom: 1px solid rgba(197,160,89,0.25);
      margin-bottom: 24px;
  }}
  .logo-icon {{
      font-size: 1.8rem;
  }}
  .logo-name {{
      font-size: 1.15rem;
      font-weight: 800;
      color: {GOLD} !important;
      letter-spacing: 0.08em;
  }}
  .logo-tagline {{
      font-size: 0.65rem;
      color: #8A9BB5 !important;
      letter-spacing: 0.12em;
      text-transform: uppercase;
  }}

  /* ── STATUS BADGES ── */
  .badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 22px;
      border-radius: 50px;
      font-weight: 700;
      font-size: 0.88rem;
      letter-spacing: 0.04em;
  }}
  .badge-approved {{
      background: rgba(46,204,113,0.12);
      color: #27AE60;
      border: 1.5px solid rgba(46,204,113,0.35);
      box-shadow: 0 0 18px rgba(46,204,113,0.2);
  }}
  .badge-review {{
      background: rgba(243,156,18,0.12);
      color: #D68910;
      border: 1.5px solid rgba(243,156,18,0.35);
      box-shadow: 0 0 18px rgba(243,156,18,0.2);
  }}
  .badge-rejected {{
      background: rgba(231,76,60,0.1);
      color: #C0392B;
      border: 1.5px solid rgba(231,76,60,0.3);
      box-shadow: 0 0 18px rgba(231,76,60,0.2);
  }}

  /* ── DIVIDER ── */
  .gold-divider {{
      height: 2px;
      background: linear-gradient(90deg, {GOLD} 0%, transparent 100%);
      border: none;
      border-radius: 2px;
      margin: 6px 0 18px 0;
  }}

  /* ── INPUT TWEAKS ── */
  [data-testid="stSidebar"] [data-baseweb="input"] {{
      background-color: rgba(255,255,255,0.06) !important;
      border-color: rgba(197,160,89,0.3) !important;
      border-radius: 8px !important;
      color: white !important;
  }}
  [data-testid="stSidebar"] [data-baseweb="select"] > div {{
      background-color: rgba(255,255,255,0.06) !important;
      border-color: rgba(197,160,89,0.3) !important;
      border-radius: 8px !important;
  }}
  [data-testid="stSidebar"] input {{
      color: white !important;
  }}

  /* ── METRIC OVERRIDE ── */
  [data-testid="metric-container"] {{
      background: {WHITE};
      border: 1px solid {BORDER};
      border-radius: 12px;
      padding: 14px 18px;
  }}
  [data-testid="metric-container"] label {{
      color: #888 !important;
      font-size: 0.7rem !important;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-weight: 600;
  }}
  [data-testid="metric-container"] [data-testid="stMetricValue"] {{
      color: {CHARCOAL} !important;
      font-weight: 700 !important;
  }}

  /* ── SIDEBAR SECTION LABEL ── */
  .sidebar-section {{
      color: {GOLD} !important;
      font-size: 0.65rem !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.14em !important;
      padding: 14px 0 6px 0;
      border-top: 1px solid rgba(197,160,89,0.2);
      margin-top: 4px;
  }}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CONSTANTS & MAPPINGS
# ──────────────────────────────────────────────
OCCUPATION_MAP = {
    "Government Employee":       1.00,
    "Salaried (Private Sector)": 0.90,
    "Business Owner":            0.75,
    "Self-Employed Professional":0.68,
    "Farmer / Agriculture":      0.58,
    "Retired":                   0.52,
    "Daily Wage Worker":         0.40,
    "Unemployed":                0.25,
}

PURITY_MAP = {
    "24K — 99.9% Pure":  24,
    "22K — 91.6% Pure":  22,
    "20K — 83.3% Pure":  20,
    "18K — 75.0% Pure":  18,
}

FEATURES = [
    "Age", "Monthly_Income", "Gold_Weight_g", "Gold_Purity",
    "Market_Value_INR", "LTV_Ratio", "Loan_Amount_INR",
    "Tenure_Months", "Past_Defaults", "occ_score"
]

# ──────────────────────────────────────────────
# LOAD MODELS (CACHED)
# ──────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_assets():
    base = os.path.dirname(__file__)
    model  = joblib.load(os.path.join(base, "model.joblib"))
    scaler = joblib.load(os.path.join(base, "scaler.joblib"))
    return model, scaler

model, scaler = load_assets()

# ──────────────────────────────────────────────
# HELPER: PREDICT
# ──────────────────────────────────────────────
def predict(inputs: dict) -> tuple[float, float]:
    """Returns (risk_proba, credit_score)."""
    df = pd.DataFrame([inputs], columns=FEATURES)
    scaled = scaler.transform(df)
    risk_p = float(model.predict_proba(scaled)[0][1])
    score  = 900 - (risk_p * 600)
    return risk_p, round(score, 1)

# ──────────────────────────────────────────────
# HELPER: GAUGE FIGURE
# ──────────────────────────────────────────────
def make_gauge(score: float) -> go.Figure:
    if score >= 750:
        bar_color = "#2ECC71"
    elif score >= 600:
        bar_color = "#F39C12"
    else:
        bar_color = "#E74C3C"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "font": {"size": 42, "color": CHARCOAL, "family": "Inter"},
            "suffix": "",
        },
        gauge={
            "axis": {
                "range": [300, 900],
                "tickwidth": 1,
                "tickcolor": "#CCC",
                "tickvals": [300, 450, 600, 750, 900],
                "ticktext": ["300", "450", "600", "750", "900"],
                "tickfont": {"size": 11, "color": "#888"},
            },
            "bar": {"color": bar_color, "thickness": 0.28},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [300, 500], "color": "rgba(231,76,60,0.12)"},
                {"range": [500, 650], "color": "rgba(243,156,18,0.10)"},
                {"range": [650, 750], "color": "rgba(241,196,15,0.10)"},
                {"range": [750, 900], "color": "rgba(46,204,113,0.12)"},
            ],
            "threshold": {
                "line": {"color": bar_color, "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": "CREDIT SCORE",
            "font": {"size": 11, "color": "#9A8F82", "family": "Inter"},
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(t=30, b=0, l=30, r=30),
        font={"family": "Inter"},
    )
    return fig

# ──────────────────────────────────────────────
# HELPER: LTV BAR FIGURE
# ──────────────────────────────────────────────
def make_ltv_bar(loan_amt: float, total_gold_val: float, ltv: float) -> go.Figure:
    equity = max(total_gold_val - loan_amt, 0)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[loan_amt],
        y=["Collateral"],
        orientation="h",
        name="Loan Amount",
        marker_color=GOLD,
        text=[f"₹{loan_amt:,.0f}<br>({ltv:.1f}% LTV)"],
        textposition="inside",
        textfont=dict(color="white", size=11, family="Inter"),
        hovertemplate="Loan Amount: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=[equity],
        y=["Collateral"],
        orientation="h",
        name="Excess Equity",
        marker_color=CHARCOAL,
        text=[f"₹{equity:,.0f}<br>Equity"],
        textposition="inside",
        textfont=dict(color="#C5A059", size=11, family="Inter"),
        hovertemplate="Excess Equity: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=110,
        margin=dict(t=10, b=10, l=0, r=0),
        showlegend=True,
        legend=dict(
            orientation="h", x=0, y=-0.6,
            font=dict(size=11, color="#666", family="Inter"),
        ),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False),
        font={"family": "Inter"},
    )
    return fig

# ──────────────────────────────────────────────
# HELPER: RISK BREAKDOWN BAR
# ──────────────────────────────────────────────
def make_risk_bar(risk_p: float) -> go.Figure:
    safe_p = 1 - risk_p
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[safe_p * 100], y=["Risk Profile"],
        orientation="h", name="Low Risk",
        marker_color="#2ECC71",
        text=[f"{safe_p*100:.1f}%"], textposition="inside",
        textfont=dict(color="white", size=12, family="Inter"),
    ))
    fig.add_trace(go.Bar(
        x=[risk_p * 100], y=["Risk Profile"],
        orientation="h", name="High Risk",
        marker_color="#E74C3C",
        text=[f"{risk_p*100:.1f}%"], textposition="inside",
        textfont=dict(color="white", size=12, family="Inter"),
    ))
    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=90,
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=True,
        legend=dict(
            orientation="h", x=0, y=-1.0,
            font=dict(size=11, color="#666", family="Inter"),
        ),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 100]),
        yaxis=dict(showticklabels=False),
        font={"family": "Inter"},
    )
    return fig

# ──────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="logo-header">
        <span class="logo-icon">⚖️</span>
        <div>
            <div class="logo-name">AURUM</div>
            <div class="logo-tagline">Gold Loans</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section">📋 Applicant Profile</p>', unsafe_allow_html=True)

    age = st.number_input("Age (years)", min_value=18, max_value=85, value=35, step=1)
    income = st.number_input("Monthly Income (₹)", min_value=5000, max_value=2000000,
                              value=55000, step=1000, format="%d")
    occupation = st.selectbox("Occupation", list(OCCUPATION_MAP.keys()))
    past_defaults = st.slider("Past Defaults", min_value=0, max_value=5, value=0)

    st.markdown('<p class="sidebar-section">🥇 Gold Details</p>', unsafe_allow_html=True)

    gold_weight = st.number_input("Gold Weight (grams)", min_value=5.0, max_value=500.0,
                                   value=50.0, step=0.5)
    purity_label = st.selectbox("Gold Purity", list(PURITY_MAP.keys()))
    market_price = st.number_input("Market Rate per gram (₹)", min_value=4000, max_value=20000,
                                    value=7800, step=50, format="%d",
                                    help="Today's 24K gold rate per gram")

    st.markdown('<p class="sidebar-section">💳 Loan Parameters</p>', unsafe_allow_html=True)

    loan_amount = st.number_input("Loan Amount Requested (₹)", min_value=10000, max_value=5000000,
                                   value=250000, step=5000, format="%d")
    tenure = st.number_input("Tenure (months)", min_value=1, max_value=36, value=12, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    assess_btn = st.button("⚡  Assess Credit Risk", use_container_width=True)

# ──────────────────────────────────────────────
# DERIVED CALCULATIONS
# ──────────────────────────────────────────────
purity_val   = PURITY_MAP[purity_label]
occ_score    = OCCUPATION_MAP[occupation]
total_gold   = gold_weight * market_price * (purity_val / 24)
ltv_ratio    = (loan_amount / total_gold * 100) if total_gold > 0 else 0.0

inputs = {
    "Age":              age,
    "Monthly_Income":   income,
    "Gold_Weight_g":    gold_weight,
    "Gold_Purity":      float(purity_val),
    "Market_Value_INR": total_gold,
    "LTV_Ratio":        ltv_ratio,
    "Loan_Amount_INR":  float(loan_amount),
    "Tenure_Months":    float(tenure),
    "Past_Defaults":    float(past_defaults),
    "occ_score":        occ_score,
}

if assess_btn:
    with st.spinner("Analysing credit profile…"):
        risk_p, score = predict(inputs)
    st.session_state.result = {
        "risk_p": risk_p, "score": score,
        "total_gold": total_gold, "ltv": ltv_ratio,
        "loan_amount": loan_amount,
    }

# ──────────────────────────────────────────────
# MAIN LAYOUT — HEADER
# ──────────────────────────────────────────────
col_hd1, col_hd2 = st.columns([3, 1])
with col_hd1:
    st.markdown(f"""
    <div>
        <h1 style="color:{CHARCOAL};font-size:1.9rem;font-weight:800;
                   margin:0;letter-spacing:-0.02em;">
            Gold Loan Credit Assessment
        </h1>
        <p style="color:#9A8F82;font-size:0.88rem;margin-top:4px;">
            AI-powered risk intelligence for gold-backed lending decisions
        </p>
    </div>
    """, unsafe_allow_html=True)
with col_hd2:
    st.markdown(f"""
    <div style="text-align:right;padding-top:6px;">
        <span style="background:{GOLD};color:white;padding:5px 14px;
              border-radius:20px;font-size:0.72rem;font-weight:700;
              letter-spacing:0.06em;">LIVE MODEL</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LIVE STATS TILES (top row — always visible)
# ──────────────────────────────────────────────
t1, t2, t3, t4 = st.columns(4)

with t1:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="label">Total Gold Value</div>
        <div class="value">₹{total_gold:,.0f}</div>
        <div class="sub">{gold_weight}g @ ₹{market_price}/g • {purity_label[:3]}</div>
    </div>
    """, unsafe_allow_html=True)

with t2:
    ltv_color = GREEN if ltv_ratio < 70 else (AMBER if ltv_ratio < 85 else RED)
    st.markdown(f"""
    <div class="stat-tile">
        <div class="label">LTV Ratio</div>
        <div class="value" style="color:{ltv_color};">{ltv_ratio:.1f}%</div>
        <div class="sub">Loan-to-Value • {"✅ Safe" if ltv_ratio < 70 else ("⚠️ Moderate" if ltv_ratio < 85 else "🔴 High")}</div>
    </div>
    """, unsafe_allow_html=True)

with t3:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="label">Loan Amount</div>
        <div class="value">₹{loan_amount:,.0f}</div>
        <div class="sub">Tenure: {tenure} months</div>
    </div>
    """, unsafe_allow_html=True)

with t4:
    occ_pct = int(occ_score * 100)
    st.markdown(f"""
    <div class="stat-tile">
        <div class="label">Occupation Score</div>
        <div class="value">{occ_pct}/100</div>
        <div class="sub">{occupation}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# RESULTS OR PLACEHOLDER
# ──────────────────────────────────────────────
if st.session_state.result is None:
    # Placeholder state
    st.markdown(f"""
    <div class="aurum-card" style="text-align:center;padding:56px 28px;">
        <div style="font-size:3rem;margin-bottom:12px;">⚖️</div>
        <h3 style="color:{CHARCOAL};font-weight:700;margin-bottom:8px;">
            Ready to Assess
        </h3>
        <p style="color:#9A8F82;max-width:380px;margin:0 auto;font-size:0.9rem;line-height:1.6;">
            Fill in the applicant details in the sidebar and click
            <strong style="color:{GOLD};">Assess Credit Risk</strong> to generate
            an AI-powered risk report.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature guide
    st.markdown(f"""
    <div class="aurum-card-cream">
        <div class="section-title">How the Model Works</div>
        <hr class="gold-divider">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;">
            <div>
                <div style="color:{GOLD};font-size:1.4rem;margin-bottom:6px;">📊</div>
                <div style="color:{CHARCOAL};font-weight:600;font-size:0.85rem;">XGBoost Classifier</div>
                <div style="color:#888;font-size:0.78rem;margin-top:4px;line-height:1.5;">
                    Trained on 10 financial & collateral features to predict default probability.
                </div>
            </div>
            <div>
                <div style="color:{GOLD};font-size:1.4rem;margin-bottom:6px;">🎯</div>
                <div style="color:{CHARCOAL};font-weight:600;font-size:0.85rem;">Score: 300–900</div>
                <div style="color:#888;font-size:0.78rem;margin-top:4px;line-height:1.5;">
                    Converted from raw probability. Higher score = lower default risk.
                </div>
            </div>
            <div>
                <div style="color:{GOLD};font-size:1.4rem;margin-bottom:6px;">🔒</div>
                <div style="color:{CHARCOAL};font-weight:600;font-size:0.85rem;">LTV Safety Guard</div>
                <div style="color:#888;font-size:0.78rem;margin-top:4px;line-height:1.5;">
                    LTV &lt;70% is safe. &gt;85% triggers mandatory manual review.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    r = st.session_state.result
    score   = r["score"]
    risk_p  = r["risk_p"]
    ltv     = r["ltv"]
    t_gold  = r["total_gold"]
    l_amt   = r["loan_amount"]

    # ── DETERMINE VERDICT ──
    if score >= 750 and ltv < 80:
        badge_html = '<span class="badge badge-approved">🟢 APPROVED — PLATINUM TIER</span>'
        verdict_color = "#27AE60"
        verdict_note  = "Strong applicant. Recommend immediate disbursement."
    elif score >= 600 and ltv < 90:
        badge_html = '<span class="badge badge-review">🟡 MANUAL REVIEW REQUIRED</span>'
        verdict_color = "#D68910"
        verdict_note  = "Moderate risk. Recommend senior officer verification."
    else:
        badge_html = '<span class="badge badge-rejected">🔴 HIGH RISK — REJECTED</span>'
        verdict_color = RED
        verdict_note  = "High default probability. Loan application declined."

    # ── ROW 1: GAUGE + VERDICT ──
    g_col, v_col = st.columns([1.1, 1])

    with g_col:
        st.markdown(f'<div class="aurum-card" style="padding:20px 24px;">', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(score), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""
        <div style="text-align:center;margin-top:-10px;margin-bottom:8px;">
            <span style="font-size:0.75rem;color:#888;text-transform:uppercase;
                         letter-spacing:0.08em;">Score Range</span>
            <span style="color:#CCC;margin:0 8px;">|</span>
            <span style="font-size:0.75rem;color:#E74C3C;font-weight:600;">300–499 Poor</span>
            <span style="color:#CCC;margin:0 6px;">·</span>
            <span style="font-size:0.75rem;color:{AMBER};font-weight:600;">500–699 Fair</span>
            <span style="color:#CCC;margin:0 6px;">·</span>
            <span style="font-size:0.75rem;color:#27AE60;font-weight:600;">750+ Excellent</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with v_col:
        st.markdown(f"""
        <div class="aurum-card" style="height:100%;">
            <div class="section-title" style="margin-bottom:14px;">Decision Verdict</div>
            {badge_html}
            <p style="color:#666;font-size:0.83rem;margin-top:14px;line-height:1.6;">
                {verdict_note}
            </p>
            <hr style="border:none;border-top:1px solid {BORDER};margin:14px 0;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                <div>
                    <div style="color:#888;font-size:0.7rem;font-weight:600;text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:4px;">Credit Score</div>
                    <div style="color:{verdict_color};font-size:1.5rem;font-weight:800;">{score:.0f}</div>
                </div>
                <div>
                    <div style="color:#888;font-size:0.7rem;font-weight:600;text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:4px;">Default Risk</div>
                    <div style="color:{verdict_color};font-size:1.5rem;font-weight:800;">{risk_p*100:.1f}%</div>
                </div>
                <div>
                    <div style="color:#888;font-size:0.7rem;font-weight:600;text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:4px;">LTV Ratio</div>
                    <div style="color:{CHARCOAL};font-size:1.3rem;font-weight:700;">{ltv:.1f}%</div>
                </div>
                <div>
                    <div style="color:#888;font-size:0.7rem;font-weight:600;text-transform:uppercase;
                                letter-spacing:0.06em;margin-bottom:4px;">Gold Coverage</div>
                    <div style="color:{CHARCOAL};font-size:1.3rem;font-weight:700;">
                        {(t_gold/l_amt):.2f}x
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 2: COLLATERAL BAR + RISK BREAKDOWN ──
    b1, b2 = st.columns(2)

    with b1:
        st.markdown(f"""
        <div class="aurum-card">
            <div class="section-title">Collateral Coverage</div>
            <div class="section-sub">Loan vs Total Gold Value breakdown</div>
        """, unsafe_allow_html=True)
        st.plotly_chart(make_ltv_bar(l_amt, t_gold, ltv), use_container_width=True,
                        config={"displayModeBar": False})
        excess = max(t_gold - l_amt, 0)
        st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        margin-top:12px;font-size:0.8rem;color:#666;">
                <span>📌 Total Gold Value: <strong style="color:{CHARCOAL};">
                    ₹{t_gold:,.0f}</strong></span>
                <span>📌 Excess Equity: <strong style="color:{CHARCOAL};">
                    ₹{excess:,.0f}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b2:
        st.markdown(f"""
        <div class="aurum-card">
            <div class="section-title">Risk Probability Distribution</div>
            <div class="section-sub">Model confidence in low vs high risk classification</div>
        """, unsafe_allow_html=True)
        st.plotly_chart(make_risk_bar(risk_p), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown(f"""
            <div style="margin-top:14px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <div style="width:10px;height:10px;border-radius:50%;
                                background:#2ECC71;"></div>
                    <span style="font-size:0.8rem;color:#555;">
                        Low Risk: <strong>{(1-risk_p)*100:.1f}%</strong>
                        — Model confidence in approval
                    </span>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:10px;height:10px;border-radius:50%;
                                background:#E74C3C;"></div>
                    <span style="font-size:0.8rem;color:#555;">
                        High Risk: <strong>{risk_p*100:.1f}%</strong>
                        — Probability of default
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 3: APPLICANT SUMMARY TABLE ──
    st.markdown(f"""
    <div class="aurum-card">
        <div class="section-title">Applicant Summary — Input Parameters</div>
        <hr class="gold-divider">
    """, unsafe_allow_html=True)

    s1, s2, s3, s4, s5 = st.columns(5)
    params = [
        ("Age", f"{age} yrs"),
        ("Monthly Income", f"₹{income:,.0f}"),
        ("Occupation", occupation.split()[0]),
        ("Past Defaults", str(past_defaults)),
        ("Gold Weight", f"{gold_weight}g"),
        ("Purity", purity_label[:3]),
        ("Market Rate", f"₹{market_price}/g"),
        ("Loan Amount", f"₹{loan_amount:,.0f}"),
        ("Tenure", f"{tenure} months"),
        ("Occ. Score", f"{int(occ_score*100)}/100"),
    ]
    cols = st.columns(5)
    for i, (label, val) in enumerate(params):
        with cols[i % 5]:
            st.markdown(f"""
            <div style="text-align:center;padding:10px 6px;border-radius:10px;
                        background:{CREAM};margin-bottom:8px;">
                <div style="color:#888;font-size:0.65rem;font-weight:600;
                            text-transform:uppercase;letter-spacing:0.06em;">{label}</div>
                <div style="color:{CHARCOAL};font-size:0.95rem;font-weight:700;
                            margin-top:3px;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── RESET BUTTON ──
    st.markdown("<br>", unsafe_allow_html=True)
    _, rc, _ = st.columns([3, 1, 3])
    with rc:
        if st.button("🔄  New Assessment", use_container_width=True):
            st.session_state.result = None
            st.rerun()

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:28px 0 8px 0;
            border-top:1px solid {BORDER};margin-top:32px;">
    <span style="color:#C5A059;font-weight:800;letter-spacing:0.1em;
                 font-size:0.9rem;">AURUM</span>
    <span style="color:#9A8F82;font-size:0.75rem;margin-left:8px;">
        Gold Loans · AI Credit Risk Platform · © 2025
    </span>
</div>
""", unsafe_allow_html=True)
