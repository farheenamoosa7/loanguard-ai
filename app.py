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
