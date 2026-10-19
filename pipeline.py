"""Synthetic banking risk portfolio analytics. No real customer data."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def generate_loans(size=8000, seed=42):
    rng = np.random.default_rng(seed)
    loan_type = rng.choice(["Mortgage", "Consumer", "Auto", "SME"], size=size, p=[.35,.35,.20,.10])
    amount = np.round(rng.lognormal(9.5, 0.8, size)).astype(int)
    dti = np.clip(rng.normal(.33, .14, size), .02, .95)
    credit_score = np.clip(rng.normal(665, 85, size), 300, 850).astype(int)
    logits = -4.1 + 3.5 * (dti - .3) + .007 * (650 - credit_score) + (loan_type == "Consumer") * .4
    probability = 1 / (1 + np.exp(-logits))
    default_90d = rng.binomial(1, probability)
    return pd.DataFrame({"loan_id": [f"L{i:06d}" for i in range(1,size+1)],
                         "loan_type":loan_type, "exposure_eur":amount,
                         "dti":np.round(dti,3), "credit_score":credit_score,
                         "default_90d":default_90d})

def summary(df):
    return df.groupby("loan_type").agg(loans=("loan_id","count"),
      exposure_eur=("exposure_eur","sum"),
      default_rate_90d=("default_90d","mean")).reset_index()

def run(size=8000, seed=42):
    base = Path(__file__).resolve().parent
    for directory in ["data","reports","images"]:
        (base/directory).mkdir(exist_ok=True)
    df=generate_loans(size,seed)
    assert df.loan_id.is_unique and not df.isna().any().any()
    df.to_csv(base/"data"/"synthetic_loans.csv",index=False)
    result=summary(df)
    result.to_csv(base/"reports"/"risk_by_loan_type.csv",index=False)
    (base/"reports"/"summary.txt").write_text(
        f"SIMULATED PORTFOLIO ONLY\nLoans: {len(df)}\nExposure EUR: {df.exposure_eur.sum():,.0f}\n90-day incident rate: {df.default_90d.mean():.2%}\n",encoding="utf-8")
    fig,ax=plt.subplots(figsize=(8,4))
    ax.bar(result.loan_type,result.default_rate_90d*100)
    ax.set(ylabel="90-day simulated incident rate (%)",title="Risk by loan type — synthetic")
    fig.tight_layout()
    fig.savefig(base/"images"/"risk_by_loan_type.png",dpi=160)
    plt.close(fig)
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--size",type=int,default=8000)
    parser.add_argument("--seed",type=int,default=42)
    args=parser.parse_args()
    print(run(args.size,args.seed).to_string(index=False))
