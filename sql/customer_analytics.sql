/*
Project: Customer Analytics 360
Author: Shaurya Rajput
Date: 2026-06-29
Description: SQL queries for RFM scoring, segment contribution, churn risk, retention, CLV, and VIP outreach.
*/

-- Query 1: Calculate RFM metrics for every customer.
WITH rfm_base AS (
    SELECT customer_id, days_since_last_order AS recency, total_orders AS frequency, total_revenue AS monetary
    FROM customers
)
SELECT customer_id, recency, frequency, monetary, RANK() OVER (ORDER BY monetary DESC) AS monetary_rank
FROM rfm_base;

-- Query 2: Measure segment revenue contribution for growth planning.
WITH segment_revenue AS (
    SELECT segment, COUNT(*) AS customers, SUM(total_revenue) AS revenue
    FROM customer_segments
    GROUP BY segment
)
SELECT segment, customers, revenue, revenue / SUM(revenue) OVER () AS revenue_share
FROM segment_revenue;

-- Query 3: Build a churn risk view for retention campaigns.
WITH churn_risk AS (
    SELECT customer_id, segment, churn_probability, total_revenue
    FROM customer_segments
    WHERE churn_probability >= 0.60
)
SELECT *, ROW_NUMBER() OVER (ORDER BY churn_probability DESC, total_revenue DESC) AS outreach_rank
FROM churn_risk;

-- Query 4: Estimate cohort retention by first purchase month.
WITH cohorts AS (
    SELECT DATE_TRUNC('month', first_purchase_date) AS cohort_month, customer_id, days_since_last_order
    FROM customers
)
SELECT cohort_month, COUNT(*) AS customers, AVG(CASE WHEN days_since_last_order <= 90 THEN 1 ELSE 0 END) AS retained_rate
FROM cohorts
GROUP BY cohort_month;

-- Query 5: Estimate customer lifetime value from order frequency and average order value.
WITH clv AS (
    SELECT customer_id, total_orders * avg_order_value * 1.20 AS estimated_clv
    FROM customers
)
SELECT customer_id, estimated_clv, RANK() OVER (ORDER BY estimated_clv DESC) AS clv_rank
FROM clv;

-- Query 6: Select top customers for VIP outreach.
WITH vip_candidates AS (
    SELECT customer_id, segment, total_revenue, churn_probability
    FROM customer_segments
    WHERE segment IN ('Champions', 'Loyal')
)
SELECT *, ROW_NUMBER() OVER (ORDER BY total_revenue DESC, churn_probability ASC) AS vip_rank
FROM vip_candidates;
