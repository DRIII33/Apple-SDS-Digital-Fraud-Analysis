# Apple-SDS-Digital-Fraud-Analysis

**Author:** Daniel Rodriguez III - Technical Fraud Analyst

**Description:** End-to-end operational fraud detection and decisioning framework targeting Account Takeover (ATO) in digital goods, optimizing the precision-recall tradeoff to minimize customer friction.

---

## Project Overview

This repository presents a comprehensive, end-to-end Portfolio Project framework specifically designed for the Digital Goods Technical Fraud Analyst role at Apple's Strategic Data Solutions (SDS) team. It directly aligns with the provided job description and industry best practices, focusing on the critical issue of Account Takeover (ATO) fraud within digital goods transactions. The core objective is to maintain a "friction-right" balance, ensuring high-precision fraud detection while minimizing false positives that could disrupt the legitimate customer experience.

---

## Strategic Context & Job Description Mapping

### The Business Problem:
Apple’s Services segment (e.g., App Store, Apple Music) requires robust, real-time fraud decisioning. Fraudsters are increasingly using automated credential stuffing to execute Account Takeovers (ATO). The challenge is to detect anomalous transaction velocity and device inconsistencies without creating "false declines" that disrupt the seamless experience for legitimate customers.

### How This Project Maps to the Apple SDS Job Description:
This project comprehensively addresses the requirements of the Apple SDS Digital Goods Technical Fraud Analyst role:

*   **"Track operational and business metrics"**
    *   **Solution:** Implemented via the SQL Monitoring layer (`02_fraud_kpi_monitoring.sql`, `fraud_kpis_precalculated_view.sql`, `fraud_kpi_summary_view.sql`) which tracks Daily Fraud Rates, System Block/Review Rates, False Positive Rates, and Revenue Protected.

*   **"Perform analyses to identify fraud patterns"**
    *   **Solution:** Addressed through Python-based Exploratory Data Analysis (EDA), advanced feature engineering in `05_fraud_detection_classifier.py`, and specialized SQL queries (`03_fraud_geo_hotspots.sql`, `04_fraud_cross_country_transactions.sql`) targeting device sharing, high-risk user velocity, and geographical anomalies.

*   **"Decision orders in mass or individually"**
    *   **Solution:** Achieved through the Python Decisioning Engine in `05_fraud_detection_classifier.py`, which translates machine learning probabilities into actionable operational decisions: 'Approve', 'Review', or 'Block'. This is further summarized in Looker Studio KPIs.

*   **"Willingness to learn big data systems and programming languages such as SQL or Python"**
    *   **Demonstrated:** The entire project showcases an end-to-end workflow utilizing Google Colab, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, and GCP BigQuery (including `pandas-gbq` and BigQuery SQL), highlighting proficiency across these essential tools and languages.

---

## Repository Structure & Content

The repository is structured to reflect a logical project flow, from data generation and ingestion to monitoring, machine learning, and documentation.

```
Apple-SDS-Digital-Fraud-Analysis/
├── data_generation/
│   └── 01_synthetic_data_pipeline.py
├── sql_monitoring/
│   ├── 02_fraud_kpi_monitoring.sql
│   ├── 03_fraud_geo_hotspots.sql
│   └── 04_fraud_cross_country_transactions.sql
├── sql_views/
│   ├── fraud_kpis_precalculated_view.sql
│   ├── fraud_kpi_summary_view.sql
│   └── transactions_dashboard_view.sql
├── ml_decisioning/
│   └── 05_fraud_detection_classifier.py
├── notebooks/
│   └── Apple-SDS-Digital-Fraud-Analysis.ipynb
├── docs/
│   ├── Data_Dictionary.md
│   ├── EDA_Summary.md
│   ├── Executive_Summary.md
│   └── Looker_Studio_Dashboard_Guide.md
└── README.md
```

*(Further details on each file, including full code, are provided in subsequent sections.)*

---
