import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LoanGuard AI",
    page_icon="🛡️",
    layout="wide"
)

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
        "decision_reason": "Stable income and manageable existing debt",
        "data_complete": True
    },
    {
        "case_id": "LG-002",
        "annual_income": 240000,
        "monthly_debt": 12000,
        "loan_amount": 400000,
        "ai_decision": "Rejected",
        "decision_reason": "",
        "data_complete": True
    },
    {
        "case_id": "LG-003",
        "annual_income": 480000,
        "monthly_debt": 8000,
        "loan_amount": 250000,
        "ai_decision": "Approved",
        "decision_reason": "Income meets requirements",
        "data_complete": False
    },
    {
        "case_id": "LG-004",
        "annual_income": 360000,
        "monthly_debt": 12000,
        "loan_amount": 500000,
        "ai_decision": "Rejected",
        "decision_reason": "High debt burden",
        "data_complete": True
    },
    {
        "case_id": "LG-005",
        "annual_income": 300000,
        "monthly_debt": 2000,
        "loan_amount": 150000,
        "ai_decision": "Rejected",
        "decision_reason": "Insufficient information",
        "data_complete": True
    },
    {
        "case_id": "LG-006",
        "annual_income": 0,
        "monthly_debt": 0,
        "loan_amount": 100000,
        "ai_decision": "Approved",
        "decision_reason": "Stable income",
        "data_complete": True
    },
    {
        "case_id": "LG-007",
        "annual_income": 300000,
        "monthly_debt": -2000,
        "loan_amount": 150000,
        "ai_decision": "Rejected",
        "decision_reason": "High debt burden",
        "data_complete": True
    },
    {
        "case_id": "LG-008",
        "annual_income": 300000,
        "monthly_debt": 5000,
        "loan_amount": 100000,
        "ai_decision": "Pending",
        "decision_reason": "Manual review pending",
        "data_complete": True
    }
]

# -----------------------------
# GOVERNANCE TOOLS
# -----------------------------
def check_data_quality(case):
    issues = []

    if not case["decision_reason"].strip():
        issues.append("Missing AI decision explanation")
    if case["annual_income"] <= 0:
        issues.append("Invalid annual income")
    if case["monthly_debt"] < 0:
        issues.append("Invalid monthly debt")
    if case["loan_amount"] <= 0:
        issues.append("Invalid loan amount")
    if not case["data_complete"]:
        issues.append("Case data marked incomplete")

    return {
        "case_id": case["case_id"],
        "status": "PASS" if not issues else "FLAGGED",
        "issues": issues
    }

def financial_check(case):
    monthly_income = case["annual_income"] / 12

    dti = case["monthly_debt"] / monthly_income if monthly_income > 0 else None

    loan_to_income = (
        case["loan_amount"] / case["annual_income"]
        if case["annual_income"] > 0 else None
    )

    flags = []

    if dti is not None and dti > 0.40:
        flags.append(
            "Debt-to-income ratio exceeds illustrative 40% alert threshold"
        )

    if loan_to_income is not None and loan_to_income > 1.50:
        flags.append(
            "Loan amount exceeds 1.5 times annual income alert threshold"
        )

    return {
        "case_id": case["case_id"],
        "monthly_income": round(monthly_income, 2),
        "debt_to_income_ratio": round(dti, 3) if dti is not None else None,
        "loan_to_annual_income_ratio": (
            round(loan_to_income, 3) if loan_to_income is not None else None
        ),
        "flags": flags
    }

def policy_check(case, financial_result):
    findings = []
    reason = case["decision_reason"].lower().strip()
    dti = financial_result["debt_to_income_ratio"]

    if not reason:
        findings.append("Decision has no documented explanation")

    if "high debt" in reason or "debt burden" in reason:
        if dti is not None and dti <= 0.40:
            findings.append(
                "Debt-related rejection rationale requires verification: "
                "DTI does not exceed the illustrative 40% alert threshold"
            )

    if "insufficient information" in reason and case["data_complete"]:
        findings.append(
            "Potential inconsistency: decision cites insufficient information "
            "but case is marked complete"
        )

    if case["ai_decision"] == "Approved" and dti is not None and dti > 0.40:
        findings.append(
            "Approved case exceeds illustrative DTI alert threshold; "
            "review may be warranted"
        )

    if case["ai_decision"] not in ["Approved", "Rejected"]:
        findings.append("Unrecognized AI decision value")

    return {
        "case_id": case["case_id"],
        "decision": case["ai_decision"],
        "findings": findings,
        "status": "REVIEW" if findings else "NO_FLAGS"
    }

# -----------------------------
# AGENT ORCHESTRATOR
# -----------------------------
def run_governance_agent(case):
    activity_log = []
    all_findings = []

    activity_log.append(f"Agent received case {case['case_id']}")

    data_result = check_data_quality(case)
    activity_log.append("Executed Data Quality Checker")
    all_findings.extend(data_result["issues"])

    financial_result = financial_check(case)
    activity_log.append("Executed Financial Indicator Checker")
    all_findings.extend(financial_result["flags"])

    policy_result = policy_check(case, financial_result)
    activity_log.append("Executed Policy Consistency Checker")
    all_findings.extend(policy_result["findings"])

    final_status = (
        "HUMAN REVIEW REQUIRED"
        if all_findings
        else "NO FLAGS - NOT A CLEARANCE"
    )

    return {
        "case_id": case["case_id"],
        "original_decision": case["ai_decision"],
        "final_status": final_status,
        "data_quality": data_result,
        "financial_analysis": financial_result,
        "policy_analysis": policy_result,
        "all_findings": all_findings,
        "activity_log": activity_log
    }

# -----------------------------
# CUSTOM UI STYLE
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #e5eaf4;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
[data-testid="stMetric"] {
    background-color: #151f33;
    border: 1px solid #26354e;
    padding: 16px;
    border-radius: 12px;
}
div[data-testid="stButton"] button {
    background-color: #4779f5;
    color: white;
    border-radius: 8px;
    border: none;
    height: 3em;
    font-weight: bold;
}
.audit-card {
    background-color: #151f33;
    border: 1px solid #26354e;
    border-radius: 12px;
    padding: 20px;
}
.small-muted {
    color: #98a8c3;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.markdown("## 🛡️ LoanGuard AI")
st.sidebar.caption("Lending Decision Governance Auditor")
st.sidebar.markdown("---")
st.sidebar.markdown("**Prototype information**")
st.sidebar.write("• Simulated cases")
st.sidebar.write("• Rule-based audit tools")
st.sidebar.write("• Illustrative thresholds")
st.sidebar.write("• Human oversight")
st.sidebar.markdown("---")
st.sidebar.caption("Independent portfolio prototype · 2026")

# -----------------------------
# MAIN HEADER
# -----------------------------
st.markdown("# 🛡️ LoanGuard AI")
st.markdown("### Lending Decision Governance Auditor")
st.markdown(
    "A prototype designed to examine AI-assisted lending decisions, "
    "identify governance concerns, and flag cases for human review."
)

st.info(
    "Demonstration only: this prototype uses simulated data and illustrative "
    "thresholds. It does not approve, reject, or determine loan eligibility."
)

# -----------------------------
# OVERVIEW METRICS
# -----------------------------
all_reports = [run_governance_agent(c) for c in loan_cases]

total_cases = len(all_reports)
review_cases = sum(
    r["final_status"] == "HUMAN REVIEW REQUIRED" for r in all_reports
)
total_findings = sum(len(r["all_findings"]) for r in all_reports)
review_rate = review_cases / total_cases * 100

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cases Analysed", total_cases)
c2.metric("Flagged for Review", review_cases)
c3.metric("Governance Findings", total_findings)
c4.metric("Review Rate", f"{review_rate:.1f}%")

st.markdown("---")

# -----------------------------
# CASE SELECTOR
# -----------------------------
st.markdown("## 🔍 Case Audit")

case_options = [c["case_id"] for c in loan_cases]

selected_case_id = st.selectbox(
    "Select a simulated loan case",
    case_options
)

selected_case = next(
    c for c in loan_cases if c["case_id"] == selected_case_id
)

left, right = st.columns(2)

with left:
    st.markdown("### Case Information")
    st.write("**Case ID:**", selected_case["case_id"])
    st.write("**Original AI Decision:**", selected_case["ai_decision"])
    st.write("**Annual Income:**", f"₹{selected_case['annual_income']:,.0f}")
    st.write("**Monthly Debt:**", f"₹{selected_case['monthly_debt']:,.0f}")
    st.write("**Loan Amount:**", f"₹{selected_case['loan_amount']:,.0f}")

with right:
    st.markdown("### Decision Evidence")
    st.write(
        selected_case["decision_reason"]
        if selected_case["decision_reason"]
        else "⚠️ No explanation provided"
    )
    st.write(
        "Data complete:",
        "Yes" if selected_case["data_complete"] else "No"
    )

run_button = st.button("🔎 Run Governance Audit", use_container_width=True)

if run_button:
    report = run_governance_agent(selected_case)

    st.markdown("---")
    st.markdown("## 📋 Audit Report")

    if report["final_status"] == "HUMAN REVIEW REQUIRED":
        st.error("⚠️ HUMAN REVIEW REQUIRED")
    else:
        st.success("No flags detected — this is NOT a clearance.")

    # Agent activity
    st.markdown("### ⚙️ Agent Activity")
    for step in report["activity_log"]:
        st.markdown(f"✓ {step}")

    # Findings
    st.markdown("### 🚩 Governance Findings")
    if report["all_findings"]:
        for finding in report["all_findings"]:
            st.warning(finding)
    else:
        st.success("No governance findings identified by current checks.")

    # Financial analysis
    st.markdown("### 📊 Financial Indicators")

    financial = report["financial_analysis"]

    f1, f2, f3 = st.columns(3)

    f1.metric(
        "Monthly Income",
        f"₹{financial['monthly_income']:,.0f}"
    )

    f2.metric(
        "Debt-to-Income Ratio",
        (
            f"{financial['debt_to_income_ratio'] * 100:.1f}%"
            if financial["debt_to_income_ratio"] is not None
            else "Unavailable"
        )
    )

    f3.metric(
        "Loan / Annual Income",
        (
            f"{financial['loan_to_annual_income_ratio']:.2f}x"
            if financial["loan_to_annual_income_ratio"] is not None
            else "Unavailable"
        )
    )

    st.markdown("### 🧾 Tool Results")

    with st.expander("Data Quality Checker"):
        st.json(report["data_quality"])

    with st.expander("Financial Indicator Checker"):
        st.json(report["financial_analysis"])

    with st.expander("Policy Consistency Checker"):
        st.json(report["policy_analysis"])

# -----------------------------
# ALL CASES TABLE
# -----------------------------
st.markdown("---")
st.markdown("## 📁 Test Case Overview")

overview = []

for case in loan_cases:
    r = run_governance_agent(case)
    overview.append({
        "Case": case["case_id"],
        "AI Decision": case["ai_decision"],
        "Audit Status": r["final_status"],
        "Findings": len(r["all_findings"])
    })

st.dataframe(
    pd.DataFrame(overview),
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# LIMITATIONS
# -----------------------------
st.markdown("---")
with st.expander("ℹ️ Limitations & Responsible Use"):
    st.markdown("""
    - All loan cases are simulated.
    - Rules and financial thresholds are illustrative, not official lending policy.
    - The system is rule-based and does not use a trained ML model or LLM.
    - It does not assess actual borrower creditworthiness.
    - It does not make lending decisions.
    - A flag indicates a potential issue requiring verification, not proof of unfairness.
    - No flags do not mean a case is safe, fair, compliant, or approved.
    - Human review is necessary before any consequential decision.
    """)

st.markdown("---")
st.caption(
    "LoanGuard AI | Independent AI Governance Prototype | "
    "Built for learning and demonstration purposes"
)
