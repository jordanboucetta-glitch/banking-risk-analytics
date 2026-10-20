"""Illustrative corporate lending case. EUR millions unless stated."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOAN = 5.0
ANNUAL_RATE = 0.05  # assumed, not a market quote
TENOR = 7
BASE_REVENUE = 25.0
BASE_EBITDA = 4.9
SCENARIOS = {
    "base": {"revenue_growth": 0.04, "ebitda_margin": 0.196},
    "downside": {"revenue_growth": -0.02, "ebitda_margin": 0.15},
    "severe": {"revenue_growth": -0.08, "ebitda_margin": 0.11},
}

def annuity(principal=LOAN, rate=ANNUAL_RATE, years=TENOR):
    if years <= 0 or principal < 0 or rate < 0:
        raise ValueError("Invalid loan inputs")
    return principal / years if rate == 0 else principal * rate / (1 - (1 + rate) ** (-years))

def debt_schedule():
    payment = annuity()
    balance = LOAN
    rows = []
    for year in range(2026, 2026 + TENOR):
        interest = balance * ANNUAL_RATE
        principal = min(balance, payment - interest)
        closing = max(0.0, balance - principal)
        rows.append({"year": year, "opening_debt": balance, "interest": interest,
                     "principal": principal, "debt_service": principal + interest,
                     "closing_debt": closing})
        balance = closing
    return rows

def historical():
    with (ROOT / "data" / "historical_income_statement.csv").open(newline="") as f:
        raw = {row["metric"]: row for row in csv.DictReader(f)}
    results = []
    for year in ("2023", "2024", "2025"):
        revenue = float(raw["revenue"][year])
        ebitda = float(raw["ebitda"][year])
        ebit = float(raw["ebit"][year])
        net = float(raw["net_income"][year])
        results.append({"year": int(year), "revenue": revenue, "ebitda": ebitda,
                        "ebit": ebit, "net_income": net,
                        "ebitda_margin": ebitda / revenue,
                        "net_margin": net / revenue})
    return results

def forecast():
    debt = debt_schedule()
    rows = []
    for name, assumptions in SCENARIOS.items():
        revenue = BASE_REVENUE
        for item in debt:
            revenue *= 1 + assumptions["revenue_growth"]
            ebitda = revenue * assumptions["ebitda_margin"]
            # EBITDA/debt service is a screening proxy only: it ignores cash taxes,
            # working capital, maintenance capex and all existing debt service.
            proxy = ebitda / item["debt_service"]
            rows.append({"scenario": name, "year": item["year"], "revenue": revenue,
                         "ebitda": ebitda, "new_loan_debt_service": item["debt_service"],
                         "ebitda_to_new_debt_service_proxy": proxy})
    return rows

def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    hist = historical()
    growth = hist[-1]["revenue"] / hist[-2]["revenue"] - 1
    print(f"FY2025 revenue growth: {growth:.2%}")
    print(f"FY2025 EBITDA margin: {hist[-1]['ebitda_margin']:.2%}")
    print(f"FY2025 net margin: {hist[-1]['net_margin']:.2%}")
    print(f"Annual loan payment (EUR m): {annuity():.4f}")
    write_csv(ROOT / "outputs" / "debt_schedule.csv", debt_schedule())
    write_csv(ROOT / "outputs" / "credit_analysis.csv", forecast())
    print("Outputs generated.")

if __name__ == "__main__":
    main()
