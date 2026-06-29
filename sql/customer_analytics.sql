-- Customer Analytics 360 reporting queries.
-- Adapt table and column names to your warehouse naming convention.

CREATE TABLE customer_metrics (
    customer_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE,
    last_purchase_date DATE,
    total_orders INTEGER,
    total_revenue NUMERIC(12, 2),
    avg_order_value NUMERIC(12, 2),
    returns_count INTEGER,
    support_tickets INTEGER,
    segment VARCHAR(40),
    churn_risk_score NUMERIC(5, 2)
);

CREATE VIEW segment_performance AS
SELECT
    segment,
    COUNT(*) AS customers,
    SUM(total_revenue) AS revenue,
    AVG(avg_order_value) AS avg_order_value,
    AVG(churn_risk_score) AS avg_churn_risk_score
FROM customer_metrics
GROUP BY segment;

SELECT
    customer_id,
    segment,
    total_revenue,
    churn_risk_score
FROM customer_metrics
WHERE churn_risk_score >= 0.60
ORDER BY churn_risk_score DESC, total_revenue DESC;
