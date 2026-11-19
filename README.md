# LoanGuard AI — Lending Governance Audit Prototype

**LoanGuard AI** is a beginner-built, rule-based prototype exploring how governance checks can help identify potential issues in AI-assisted lending workflows.

Rather than making lending decisions, it examines simulated cases and surfaces potential concerns for human review.

🔗 **Live Demo:** https://loanguard-lending-audit.streamlit.app/  
💻 **Source Code:** https://github.com/farheenamoosa7/loanguard-ai

## Why I built this

AI governance principles such as transparency, accountability, data quality, and human oversight need to translate into practical processes.

I wanted to explore what this could look like operationally in a lending context: what happens when information is missing, financial inputs are invalid, a decision explanation is inconsistent, or a system produces an unexpected decision value?

## What the prototype checks

| Component | Purpose |
|---|---|
| Data Quality Checker | Flags incomplete, missing, or invalid data |
| Financial Indicator Checker | Calculates illustrative financial indicators and flags threshold concerns |
| Policy Consistency Checker | Identifies inconsistencies between case data, decisions, and explanations |
| Human Review | Surfaces flagged cases requiring further investigation |

## Demonstration scenarios

The prototype includes eight simulated cases covering:

- Baseline case
- Multiple risk indicators
- Incomplete information
- Decision rationale inconsistency
- Contradictory case information
- Zero-income edge case
- Negative financial input
- Unrecognized decision value

## Testing

I manually tested eight simulated scenarios and recorded the governance findings produced by the prototype.

Testing focused on whether designed data-quality issues, financial indicators, inconsistencies, and unexpected values were surfaced as intended.

This was exploratory testing—not a formal independent validation.

## Design approach

- Rule-based checks rather than a trained machine-learning model
- Transparent, predefined conditions
- Simulated data rather than real borrower records
- Governance findings rather than automated decisions
- Human review rather than autonomous action

## Limitations

This is an educational prototype.

- It does not make loan approval or rejection decisions.
- All cases are simulated.
- Thresholds are illustrative and not based on a real lending institution's policy.
- A flagged condition is not proof of unfairness or regulatory non-compliance.
- The prototype does not measure real-world model accuracy or fairness.
- Absence of a flag does not mean a case is fair, safe, or compliant.

## What I learned

Building this prototype helped me understand the gap between high-level AI governance principles and their practical implementation. It made me think about how monitoring, validation, escalation, documentation, and human oversight can be incorporated into operational workflows.

My interest is in AI governance operations: making oversight processes practical, structured, and accountable.

## Future work

- Expand testing scenarios
- Improve testing documentation and traceability
- Explore fairness-related checks using synthetic data
- Investigate escalation and accountability workflows
- Explore how governance monitoring can be incorporated into AI-assisted decision systems

---

*Built as an independent learning and exploratory AI governance project.*
