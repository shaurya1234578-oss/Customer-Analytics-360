# Customer Analytics 360

RFM segmentation and churn probability pipeline using KMeans clustering, logistic regression, SQL, and BI-ready customer outputs.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)

## Executive Summary

This project analyzes 250 synthetic India-context customer records to identify high-value customers, retention risks, and segment-level revenue opportunities. It is differentiated from the other repositories by focusing on customer lifecycle analytics, RFM scoring, clustering, and churn probability.

## Segment Results

| Segment    | Count | Avg Revenue | Churn Risk |
|------------|-------|-------------|------------|
| Champions  | 63    | ₹130,136    | Low        |
| Loyal      | 107   | ₹48,761     | Low-Med    |
| At Risk    | 58    | ₹12,420     | High       |
| Lost       | 22    | ₹17,850     | Critical   |

## How To Run

```bash
pip install -r requirements.txt
python scripts/customer_segmentation.py
```

## Architecture Pipeline

```text
Synthetic customer data
    -> RFM score calculation
    -> KMeans segmentation
    -> Logistic regression churn probability
    -> Segment summary table
    -> SQL customer analytics views
```
