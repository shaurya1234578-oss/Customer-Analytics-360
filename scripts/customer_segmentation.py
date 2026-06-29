"""RFM customer segmentation with KMeans clustering and churn probability scoring."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample_customers.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "customer_segments_output.csv"
RANDOM_STATE = 42
CLUSTER_COUNT = 4
REFERENCE_DATE = pd.Timestamp("2026-06-29")
SEGMENT_LABELS: Dict[int, str] = {0: "Champions", 1: "Loyal", 2: "At Risk", 3: "Lost"}


def load_customers(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load customer records and validate required fields."""
    try:
        customers = pd.read_csv(path, parse_dates=["first_purchase_date", "last_purchase_date"])
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Customer file not found: {path}") from exc
    required = {"customer_id", "first_purchase_date", "last_purchase_date", "total_orders", "total_revenue", "avg_order_value", "days_since_last_order", "region", "category_preference"}
    missing = required.difference(customers.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return customers


def compute_rfm(customers: pd.DataFrame) -> pd.DataFrame:
    """Compute RFM scores where higher values indicate stronger customer quality."""
    scored = customers.copy()
    scored["recency"] = scored["days_since_last_order"]
    scored["frequency"] = scored["total_orders"]
    scored["monetary"] = scored["total_revenue"]
    # Recency is reversed because fewer days since last order is better.
    scored["r_score"] = pd.qcut(scored["recency"].rank(method="first"), 4, labels=[4, 3, 2, 1]).astype(int)
    scored["f_score"] = pd.qcut(scored["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    scored["m_score"] = pd.qcut(scored["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    scored["rfm_score"] = scored[["r_score", "f_score", "m_score"]].sum(axis=1)
    return scored


def cluster_customers(scored: pd.DataFrame) -> pd.DataFrame:
    """Apply KMeans clustering and map clusters to business-friendly labels."""
    features = scored[["recency", "frequency", "monetary", "avg_order_value"]]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    model = KMeans(n_clusters=CLUSTER_COUNT, random_state=RANDOM_STATE, n_init=10)
    clustered = scored.copy()
    clustered["cluster"] = model.fit_predict(scaled_features)
    cluster_order = clustered.groupby("cluster")["rfm_score"].mean().sort_values(ascending=False).index.tolist()
    label_map = {cluster_id: SEGMENT_LABELS[position] for position, cluster_id in enumerate(cluster_order)}
    # Labeling by average RFM score keeps the cluster names stable across reruns.
    clustered["segment"] = clustered["cluster"].map(label_map)
    return clustered


def add_churn_probability(clustered: pd.DataFrame) -> pd.DataFrame:
    """Train a simple logistic model to estimate churn probability."""
    modeled = clustered.copy()
    modeled["churn_label"] = ((modeled["days_since_last_order"] > 180) | (modeled["rfm_score"] <= 5)).astype(int)
    feature_frame = modeled[["recency", "frequency", "monetary", "avg_order_value", "rfm_score"]]
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    # The churn label is synthetic but follows a transparent business rule.
    model.fit(feature_frame, modeled["churn_label"])
    # The probability column lets BI dashboards sort customers by retention urgency.
    modeled["churn_probability"] = model.predict_proba(feature_frame)[:, 1].round(3)
    return modeled


def main() -> None:
    """Run the complete customer segmentation pipeline."""
    customers = load_customers()
    output = add_churn_probability(cluster_customers(compute_rfm(customers)))
    output.to_csv(OUTPUT_PATH, index=False)
    summary = output.groupby("segment", as_index=False).agg(count=("customer_id", "count"), avg_revenue=("total_revenue", "mean"), avg_churn=("churn_probability", "mean"))
    print("Customer segment summary")
    print(summary.to_string(index=False, formatters={"avg_revenue": "₹{:,.0f}".format, "avg_churn": "{:.2f}".format}))
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
