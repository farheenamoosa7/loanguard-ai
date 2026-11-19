import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LoanGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# -----------------------------
# CONSOLIDATED READABILITY STYLES
# -----------------------------
st.markdown("""
<style>
/* Main application background and text */
.stApp {
    background-color: #0B1120;
    color: #E5EAF4;
}
.stMarkdown, .stText, p, li {
    color: #E2E8F0;
}
h1, h2, h3 {
    color: #F8FAFC !important;
}
label {
    color: #E2E8F0 !important;
}

/* Sidebar contrast: dark background with bright readable text */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
[data-testid="stSidebar"] * {
    color: #E5EAF4 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] label {
    color: #D1D5DB !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #151F33 !important;
    border: 1px solid #26354E !important;
    padding: 16px !important;
    border-radius: 12px !important;
}
[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
}
[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-weight: 700 !important;
}

/* Buttons */
div[data-testid="stButton"] button {
    background-color: #4779F5 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
    height: 3em !important;
    font-weight: bold !important;
}

/* Cards and spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.audit-card {
    background-color: #151F33;
    border: 1px solid #26354E;
    border-radius: 12px;
    padding: 20px;
}
.small-muted {
    color: #98A8C3 !important;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SIMULATED LOAN CASES
# -----------------------------
loan_cases = [
    {
        "case_id": "LG-001",
        "annual_income": 600000,
        "monthly_debt": 5000,
        "loan_amount": 200000,
        "ai_decision": "Approved",
