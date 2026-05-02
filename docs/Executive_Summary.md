### Executive Summary: Apple SDS Digital Fraud Analysis

**Author:** Daniel Rodriguez III - Technical Fraud Analyst

This project delivers a robust, end-to-end framework for detecting and decisioning Account Takeover (ATO) fraud within Apple's digital goods ecosystem. Designed for the Apple SDS Digital Goods Technical Fraud Analyst role, the solution prioritizes a "friction-right" balance, ensuring high-precision fraud detection while minimizing false positives to safeguard the legitimate customer experience.

#### 1. Business Problem & Strategic Context

Apple's Services segment faces increasing threats from ATO fraud, typically executed via automated credential stuffing. The core challenge is to identify anomalous transaction patterns and device inconsistencies without disrupting legitimate user journeys. This framework directly addresses this by building an operational fraud detection and decisioning system.

#### 2. Key Phases & Deliverables

**Phase 1: Synthetic Data Generation (`01_synthetic_data_pipeline.py`)**
*   **Objective:** Create a highly realistic, audit-safe dataset simulating digital goods transactions, user metadata, and session data, including an ATO surge.
*   **Enhancements:** Incorporated IP-to-Geolocation enrichment (`ip_country`, `ip_city`, `ip_region`, `ip_latitude`, `ip_longitude`) and a mechanism to simulate cross-country transactions to facilitate advanced geographical fraud analysis.

**Phase 2: Data Ingestion & Initial EDA (Google BigQuery & Python)**
*   **Objective:** Load generated data into Google BigQuery and perform initial exploratory data analysis.
*   **Process:**
    *   `transactions.csv` and `users.csv` were successfully loaded into Pandas DataFrames.
    *   EDA confirmed data quality (no missing values), validated feature distributions, and verified the successful enrichment of geolocation fields and the intended class imbalance for fraud (approx. 9.62% fraud rate) and compromised users (approx. 5.1%).
    *   Timestamp column was converted to `datetime` for time-series analysis.
    *   Data was successfully uploaded to `driiiportfolio.fraud_analysis_data.transactions_temp` and `users_temp` tables in BigQuery.

**Phase 3: SQL Monitoring & Fraud Pattern Identification (`sql_monitoring/*.sql`, `sql_views/*.sql`)**
*   **Objective:** Develop SQL queries for daily KPI monitoring and identify specific fraud patterns within BigQuery.
*   **Key Queries/Views:**
    *   `02_fraud_kpi_monitoring.sql`: Tracks daily fraud rate, revenue impact, high-risk user velocity, and excessive device sharing.
    *   `03_fraud_geo_hotspots.sql`: Pinpoints geographical fraud hotspots using `ip_country` and `ip_city`.
    *   `04_fraud_cross_country_transactions.sql`: Identifies transactions where the IP country differs from the user's registered country, a strong ATO indicator. This query's functionality was validated after re-generating data with intentional geo-mismatches.
    *   `transactions_dashboard_view.sql`: A consolidated BigQuery view joining enriched transactions and user data for dashboarding.
    *   `fraud_kpis_precalculated_view.sql`: Aggregates daily operational metrics to optimize dashboard performance.
    *   `fraud_kpi_summary_view.sql`: Provides overall project-level KPI metrics for scorecards.

**Phase 4: Feature Engineering, ML Classifier, and Decisioning Layer (`05_fraud_detection_classifier.py`)**
*   **Objective:** Build a predictive model to identify fraud and translate its output into actionable business decisions.
*   **Approach:**
    *   **Feature Engineering:** Incorporated comprehensive features including temporal (hour, day, month), user-level aggregations (avg/max amount, total txns, distinct devices/IPs), user account age, and crucial geolocation features (`ip_latitude`, `ip_longitude`, one-hot encoded `ip_country`/`ip_city`, and `is_cross_country_txn` flag).
    *   **Model:** Employed a `RandomForestClassifier` with `class_weight='balanced'` to handle the inherent class imbalance in fraud data.
    *   **Decisioning Engine:** Developed a logic to translate model-predicted fraud probabilities into operational decisions: 'block' (high confidence fraud), 'review' (gray area), and 'approve' (low risk).
    *   **Optimization:** Adjusted decision thresholds based on Precision-Recall curve analysis to significantly improve fraud recall, demonstrating:
        *   Recall (Blocked Fraud): ~83.05%
        *   Recall (Blocked + Reviewed Fraud): ~88.67%
        *   False Positive Rate (Friction Index - Block/Review): ~7.58%
        *   Estimated Revenue Protected: ~$98,376.73 (for the simulated dataset).

**Phase 5: Looker Studio Dashboard Integration (Conceptual & Guide)**
*   **Objective:** Design a Looker Studio dashboard for continuous monitoring and visualization of fraud KPIs and patterns.
*   **Components:** Outlined detailed KPIs (Overall Fraud Rate, System Block/Review Rate, FPR, Revenue Protected) and visualizations (time series, tables, geo charts) leveraging the BigQuery views to provide real-time, actionable insights for analysts.

#### 3. Project Impact & Job Description Alignment

This project successfully demonstrates the capabilities required for the Apple SDS role:
*   **Track operational metrics:** Through comprehensive SQL monitoring and pre-calculated KPI views.
*   **Identify fraud patterns:** Utilizing advanced feature engineering, ML models, and specialized geo-location SQL queries.
*   **Decision orders:** Implementing a data-driven ML decisioning engine.
*   **Proficiency in big data systems & programming:** Showcasing expertise in Python (Pandas, Scikit-learn), SQL, and Google Cloud Platform (BigQuery, Looker Studio integration).

By establishing a robust fraud detection and decisioning pipeline, this project safeguards revenue, minimizes customer friction, and provides critical intelligence for combating ATO fraud in digital goods.
