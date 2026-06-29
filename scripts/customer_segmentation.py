"""Customer segmentation workflow for the Customer Analytics 360 project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "sample_customers.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "customer_segments_output.csv"
REFERENCE_DATE = pd.Timestamp("2026-06-29")


def load_customers(path: Path = INPUT_PATH) -> pd.DataFrame:
    """Load customer records and parse date columns."""
    customers = pd.read_csv(path, parse_dates=["signup_date", "last_purchase_date"])
    return customers


def assign_segment(row: pd.Series) -> str:
    """Assign a business-friendly customer segment."""
    if row["total_revenue"] >= 8000 and row["recency_days"] <= 90:
        return "High Value Loyal"
    if row["total_revenue"] >= 3000 and row["recency_days"] > 120:
        return "Win Back Priority"
    if row["total_orders"] <= 3:
        return "New or Low Frequency"
    return "Core Customer"


def score_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Create customer KPIs, risk scores, and recommended actions."""
    scored = customers.copy()
    scored["recency_days"] = (REFERENCE_DATE - scored["last_purchase_date"]).dt.days
    scored["customer_age_days"] = (REFERENCE_DATE - scored["signup_date"]).dt.days
    scored["orders_per_month"] = (
        scored["total_orders"] / (scored["customer_age_days"].clip(lower=30) / 30)
    ).round(2)
    scored["churn_risk_score"] = (
        (scored["recency_days"] / 180).clip(0, 1) * 0.55
        + (1 - (scored["orders_per_month"] / 2).clip(0, 1)) * 0.30
        + (scored["support_tickets"] / 5).clip(0, 1) * 0.15
    ).round(2)
    scored["segment"] = scored.apply(assign_segment, axis=1)
    scored["recommended_action"] = scored["segment"].map(
        {
            "High Value Loyal": "Offer premium loyalty benefits and cross-sell bundles.",
            "Win Back Priority": "Run personalized win-back campaign with limited-time incentive.",
            "New or Low Frequency": "Trigger onboarding journey and second-purchase offer.",
            "Core Customer": "Maintain engagement with category-based recommendations.",
        }
    )
    return scored.sort_values(["churn_risk_score", "total_revenue"], ascending=[False, False])


def main() -> None:
    """Run the complete segmentation workflow."""
    customers = load_customers()
    scored = score_customers(customers)
    scored.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved customer segment output to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
