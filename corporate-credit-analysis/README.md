# Corporate Credit Analysis — INDUSTRIA SAS

**Portfolio case study | Corporate banking | Fictional data**

Credit assessment of a hypothetical French industrial borrower with €25m FY2025 revenue requesting a **€5m, seven-year amortising term loan** to finance a production line.

## Deliverables
- Three-year historical income statement and financial ratios.
- Debt service schedule and affordability analysis.
- Forward-looking 2026–2032 operating forecasts and downside stress scenarios.
- Credit committee memo with a conditional recommendation.
- Reproducible Python model using only the standard library.

## Run
```bash
python3 corporate-credit-analysis/src/model.py
python3 corporate-credit-analysis/tests/test_model.py
```
The script writes `outputs/credit_analysis.csv` and `outputs/debt_schedule.csv` relative to this project directory.

## Case assumptions
All figures are **invented**, not drawn from LCL or any real client. Revenue and earnings for 2023–2025 are provided as a pedagogical starting point. The opening balance sheet, existing debt service, working capital, capital expenditure, tax and pricing assumptions are **not available**. Accordingly, the simplified debt service coverage proxy in this project is **not a bank-ready DSCR**. A real underwriting decision requires verified statements, existing debt schedules, cash flow bridge, security review, KYC and borrower forecasts.

## Structure
- `data/historical_income_statement.csv` — historical P&L in EUR million.
- `src/model.py` — financial ratios, debt amortisation, scenario forecasts.
- `tests/test_model.py` — arithmetic checks.
- `docs/credit_committee_memo.md` — credit decision and outstanding due diligence.
- `docs/methodology.md` — definitions, caveats and next steps.

**Author:** Jordan Boucetta — personal learning project, not professional credit advice.
