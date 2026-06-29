# Customer Analytics 360

Customer Analytics 360 is a business intelligence and applied machine learning case study for understanding customer value, retention risk, and segment-level growth opportunities.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?style=flat-square)

## Executive Summary

Many businesses collect customer transactions but struggle to identify which customers are loyal, which are at risk, and which segments deserve targeted campaigns.

This project converts customer-level transaction data into a decision-support layer for marketing, sales, and retention teams. It includes sample data, SQL reporting logic, a Python segmentation workflow, and dashboard-ready recommendations.

## Key Features

- Customer segmentation using revenue, order frequency, recency, and retention indicators.
- Churn-risk scoring logic for prioritizing outreach.
- SQL views for executive KPIs and segment reporting.
- Python workflow for clean, repeatable customer scoring.
- Dashboard blueprint for Power BI or Tableau implementation.

## Architecture Pipeline

```text
Customer transactions
    -> Data validation and KPI calculation
    -> Customer feature table
    -> Segmentation and churn-risk scoring
    -> SQL reporting views
    -> BI dashboard and campaign recommendations
```

## Repository Structure

```text
Customer-Analytics-360/
├── data/
│   └── sample_customers.csv
├── docs/
│   ├── dashboard_blueprint.md
│   └── insights.md
├── scripts/
│   └── customer_segmentation.py
├── sql/
│   └── customer_analytics.sql
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Actionable Insights Demonstrated

- High-value loyal customers should receive premium retention and upsell offers.
- High-revenue but inactive customers should be targeted with win-back campaigns.
- Low-frequency new customers need onboarding journeys and second-purchase nudges.
- Segment-level revenue concentration helps teams avoid over-investing in low-return campaigns.

## How To Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the segmentation workflow:

```bash
python scripts/customer_segmentation.py
```

3. Review the generated output:

```text
data/customer_segments_output.csv
```

4. Use the SQL file in `sql/customer_analytics.sql` to create reporting tables or BI views.

## Dashboard Design

Recommended dashboard pages:

- Executive Overview: revenue, customers, churn risk, average order value.
- Segment Analysis: segment size, revenue contribution, retention actions.
- Customer List: ranked customers for campaign prioritization.
- Growth Opportunities: win-back, upsell, and onboarding recommendations.

## Suggested GitHub Topics

`customer-analytics`, `customer-segmentation`, `churn-analysis`, `business-intelligence`, `powerbi-dashboard`, `sql`, `python`, `pandas`, `machine-learning`, `data-analytics`, `marketing-analytics`, `portfolio-project`
