"""Run with: python3 corporate-credit-analysis/tests/test_model.py"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from model import annuity, debt_schedule, historical, forecast

def test_historical():
    h = historical()
    assert math.isclose(h[-1]["revenue"] / h[-2]["revenue"] - 1, 3 / 22)
    assert math.isclose(h[-1]["ebitda_margin"], 4.9 / 25)
    assert math.isclose(h[-1]["net_margin"], 2.2 / 25)

def test_loan():
    s = debt_schedule()
    assert len(s) == 7
    assert math.isclose(s[-1]["closing_debt"], 0, abs_tol=1e-8)
    assert math.isclose(sum(x["principal"] for x in s), 5, abs_tol=1e-8)
    assert all(math.isclose(x["debt_service"], annuity(), abs_tol=1e-8) for x in s)

def test_forecast():
    f = forecast()
    assert len(f) == 21
    assert all(x["ebitda_to_new_debt_service_proxy"] > 0 for x in f)

if __name__ == "__main__":
    test_historical()
    test_loan()
    test_forecast()
    print("All tests passed")
