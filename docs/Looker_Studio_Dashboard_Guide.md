### Looker Studio Dashboard Guide: Apple SDS Digital Fraud Analysis

**Author:** Daniel Rodriguez III - Technical Fraud Analyst

This document provides comprehensive, step-by-step instructions for building the **Apple SDS Digital Fraud Analysis dashboard** in Google Looker Studio. This dashboard leverages pre-calculated BigQuery views (`fraud_kpis_precalculated_view` and `fraud_kpi_summary_view` for aggregated metrics, and `transactions_dashboard_view` for granular data) to ensure optimal performance and accuracy. Each visual is designed to communicate critical insights, directly addressing the business problem of Account Takeover (ATO) fraud and supporting the requirements of the Digital Goods Technical Fraud Analyst role at Apple SDS.

---

### **1. Looker Studio Setup**

1.  Open Google Looker Studio and create a new report.
2.  Connect to a new data source.
    *   Select 'BigQuery' as the connector.
    *   Choose your Google Cloud Project (`driiiportfolio`).
    *   Select the `fraud_analysis_data` dataset.
    *   Connect to `transactions_dashboard_view` (for granular data and time series).
    *   Repeat the process and connect to `fraud_kpis_precalculated_view` (for daily aggregated KPIs).
    *   Repeat again and connect to `fraud_kpi_summary_view` (for overall scorecard KPIs, if using this separate view).

---

### **2. Pre-computation for KPI Scorecards (Optional but Recommended)**

To efficiently calculate the aggregated KPIs without complex Looker Studio calculations, it is highly recommended to use the `fraud_kpi_summary_view` (or ensure your `fraud_kpis_precalculated_view` contains these aggregate values as a single row). If not already created or if you want a dedicated single-row summary, execute the following SQL in BigQuery:

```sql
CREATE OR REPLACE VIEW `driiiportfolio.fraud_analysis_data.fraud_kpi_summary_view` AS
SELECT
    -- Overall Fraud Rate: Proportion of all transactions that are fraudulent
    SAFE_DIVIDE(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END), COUNT(*)) AS overall_fraud_rate,
    -- System Block Rate: Proportion of all transactions that were blocked by the system
    SAFE_DIVIDE(SUM(CASE WHEN decision = 'block' THEN 1 ELSE 0 END), COUNT(*)) AS system_block_rate,
    -- System Review Rate: Proportion of all transactions that were sent for manual review
    SAFE_DIVIDE(SUM(CASE WHEN decision = 'review' THEN 1 ELSE 0 END), COUNT(*)) AS system_review_rate,
    -- False Positive Rate: Proportion of legitimate transactions (is_fraud=0) that were incorrectly blocked by the system
    SAFE_DIVIDE(
        SUM(CASE WHEN is_fraud = 0 AND decision = 'block' THEN 1 ELSE 0 END),
        SUM(CASE WHEN is_fraud = 0 THEN 1 ELSE 0 END)
    ) AS false_positive_rate,
    -- Estimated Revenue Protected: Total amount of fraudulent transactions that were either blocked or sent for review
    SUM(CASE WHEN is_fraud = 1 AND (decision = 'block' OR decision = 'review') THEN amount ELSE 0 END) AS estimated_revenue_protected
FROM
    `driiiportfolio.fraud_analysis_data.transactions_dashboard_view`;
```
**Explanation:** This view pre-aggregates the core KPI metrics into a single row, optimizing performance for Looker Studio scorecards.

---

### **3. Dashboard Pages & Chart Configuration**

#### **PAGE 1: Overview & Key Metrics**

**Purpose:** Provides an executive-level summary of overall fraud performance and system effectiveness. This page directly addresses the JD requirement to "Track operational and business metrics."

**Data Source for Scorecards:** `driiiportfolio.fraud_analysis_data.fraud_kpi_summary_view`

*   **CHART 1: Overall Fraud Rate**
    *   **Type:** Scorecard
    *   **Metric:** `overall_fraud_rate` (Aggregation: `AVG`, Type: `Number -> Percent`)
    *   **Caption:** Displays the overall percentage of transactions identified as fraudulent. A lower rate indicates effective fraud prevention, while an increasing trend might signal new fraud patterns.

*   **CHART 2: System Block Rate**
    *   **Type:** Scorecard
    *   **Metric:** `system_block_rate` (Aggregation: `AVG`, Type: `Number -> Percent`)
    *   **Caption:** Quantifies the percentage of transactions automatically blocked. A high rate needs to be balanced against potential false positives.

*   **CHART 3: System Review Rate**
    *   **Type:** Scorecard
    *   **Metric:** `system_review_rate` (Aggregation: `AVG`, Type: `Number -> Percent`)
    *   **Caption:** Shows the percentage of transactions flagged for manual review. A manageable rate is crucial for operational efficiency.

*   **CHART 4: False Positive Rate (Friction Index)**
    *   **Type:** Scorecard
    *   **Metric:** `false_positive_rate` (Aggregation: `AVG`, Type: `Number -> Percent`)
    *   **Caption:** Indicates the proportion of legitimate transactions incorrectly blocked. This directly measures customer friction, a key challenge in ATO detection.

*   **CHART 5: Estimated Revenue Protected**
    *   **Type:** Scorecard
    *   **Metric:** `estimated_revenue_protected` (Aggregation: `SUM`, Type: `Number -> Currency`)
    *   **Caption:** Represents the total monetary value of fraudulent transactions successfully prevented. This directly measures the financial impact and value of the fraud detection system.

**Data Source for Time Series:** `driiiportfolio.fraud_analysis_data.fraud_kpis_precalculated_view`

*   **CHART 6: Daily Fraud Rate Over Time**
    *   **Type:** Time Series Chart
    *   **Dimension:** `transaction_date`
    *   **Metric:** `SAFE_DIVIDE(fraud_txns, total_txns)` (Calculated Field in Looker Studio, Type: `Number -> Percent`)
    *   **Caption:** Visualizes daily fluctuations in the fraud rate, helping to identify trends, seasonal patterns, or sudden spikes. Addresses the need to "Track operational and business metrics."

#### **PAGE 2: User & Device Anomalies**

**Purpose:** Focuses on identifying suspicious user behaviors and device sharing patterns, addressing the JD requirement to "Perform analyses to identify fraud patterns."

**Data Source:** `driiiportfolio.fraud_analysis_data.transactions_dashboard_view`

*   **CHART 7: Top Users by Fraudulent Transactions & Total Spend**
    *   **Type:** Table or Bar Chart
    *   **Dimension:** `user_id`
    *   **Metrics:**
        *   `Fraudulent Transactions Count`: `SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)` (Calculated Field)
        *   `Total Spend`: `amount` (Aggregation: `SUM`)
    *   **Sorting:** `Fraudulent Transactions Count` (Descending)
    *   **Caption:** Identifies users with the highest number of fraudulent transactions and their total spending, guiding investigations into potential fraud rings or compromised accounts.

*   **CHART 8: Excessive Device Sharing**
    *   **Type:** Bar Chart
    *   **Dimension:** `device_id`
    *   **Metric:** `user_id` (Aggregation: `COUNT_DISTINCT`)
    *   **Filtering:** Exclude null/unknown `device_id`s; Filter for `COUNT_DISTINCT(user_id) > 5`.
    *   **Sorting:** `user_id` (COUNT_DISTINCT, Descending)
    *   **Caption:** Displays device IDs used by an unusually high number of distinct users, indicating potential botnet activity or fraud rings.

#### **PAGE 3: Geographical Fraud Analysis**

**Purpose:** Pinpoints geographical fraud hotspots and cross-country transaction anomalies, crucial for "analyzing complex fraud scenarios."

**Data Source:** `driiiportfolio.fraud_analysis_data.transactions_dashboard_view`

*   **CHART 9: Fraud by IP Country/City**
    *   **Type:** Geo Chart (Filled Map)
    *   **Geo Dimension:** `transaction_ip_country` (Set Field Type to `Geo -> Country`)
    *   **Drill-Down Dimension:** `transaction_ip_city` (Set Field Type to `Geo -> City`)
    *   **Metric:** `SAFE_DIVIDE(SUM(is_fraud), COUNT(transaction_id))` (Calculated Field, Type: `Number -> Percent`)
    *   **Color:** Sequential color scale based on Fraud Rate (e.g., green to red).
    *   **Caption:** Visualizes fraud rates by IP country and city, highlighting geographical hotspots where fraudulent activities are more prevalent. Drill-down allows granular analysis.

*   **CHART 10: Cross-Country Transactions Analysis**
    *   **Type:** Table or Bar Chart
    *   **Dimensions:** `user_id`, `user_registered_country`, `transaction_ip_country`
    *   **Metrics:**
        *   `Transaction Count`: `transaction_id` (Aggregation: `COUNT_DISTINCT`)
        *   `Fraud Rate`: `SAFE_DIVIDE(SUM(is_fraud), COUNT(transaction_id))` (Calculated Field, Type: `Number -> Percent`)
    *   **Filtering:** Include only records where `is_cross_country_txn` is `1`.
    *   **Sorting:** `Transaction Count` (Descending)
    *   **Caption:** Analyzes transactions where the IP country differs from the user's registered country. This is a strong indicator of potential Account Takeover (ATO) or high-risk activity.

---

### **4. Business Problem & Job Description Alignment: Dashboard Insights**

The dashboard robustly addresses the core business problem of ATO fraud and fulfills the requirements of the Apple SDS Digital Goods Technical Fraud Analyst role:

*   **Addresses ATO Fraud & Friction-Right Balance:**
    *   **`Cross-Country Transactions Analysis` (Chart 10)**: Directly surfaces ATO indicators where transaction origin differs from user registration.
    *   **`False Positive Rate` (Chart 4)**: Quantifies customer friction, ensuring the system maintains a "friction-right" balance crucial for Apple's user experience.
    *   **`System Block Rate` (Chart 2) & `System Review Rate` (Chart 3)**: Reflect the system's automated responses to suspected fraud, directly showcasing the ML decisioning layer in action.

*   **
