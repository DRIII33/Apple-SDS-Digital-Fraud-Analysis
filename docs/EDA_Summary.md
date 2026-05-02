### EDA Summary and Key Findings

**Author:** Daniel Rodriguez III - Technical Fraud Analyst

### EDA Summary and Key Findings

This document summarizes the key findings from the Exploratory Data Analysis (EDA) conducted on the synthetic `transactions` and `users` datasets. The EDA focused on validating data quality, understanding feature distributions, and confirming the successful enrichment of geolocation data and fraud patterns.

### 1. Data Quality and Types

**transactions_df**
*   **No Missing Values**: All 10,000 entries across 12 columns are non-null, indicating a clean dataset for immediate use.
*   **Data Types**: `transaction_id`, `user_id`, `device_id`, `ip_address`, `ip_country`, `ip_city`, `ip_region` are `object` (string) as expected. `amount`, `ip_latitude`, `ip_longitude` are `float64`, and `is_fraud` is `int64`. The `timestamp` column was initially `object` but was successfully converted to `datetime` for time-series analysis in subsequent steps.

**users_df**
*   **No Missing Values**: All 1,000 entries across 4 columns are non-null.
*   **Data Types**: `user_id`, `country` are `object`, while `account_age_days` and `is_compromised` are `int64`.

### 2. Distribution of Key Features

**transactions_df**
*   **Amount**: Ranges from $0.01 to $1273.62, with a mean of $56.45. The standard deviation ($66.29) is higher than the mean, and the max value is significantly larger than the 75th percentile ($74.51), suggesting a right-skewed distribution which is typical for transaction amounts, especially with fraud (fraudulent transactions tend to have higher amounts).
*   **ip_latitude & ip_longitude**: These show wide ranges (-89.97 to 89.95 for latitude, -179.97 to 179.96 for longitude), consistent with global coverage. The mean values are close to zero, which is expected for randomly distributed coordinates.

**users_df**
*   **Account Age Days**: Ranges from 2 days to 1999 days (approx 5.5 years), with a mean of 1036 days. This provides a good distribution of user account maturity.

### 3. Geolocation Data Validation

*   The newly added `ip_country`, `ip_city`, `ip_region`, `ip_latitude`, and `ip_longitude` fields are present and populated correctly in `transactions_df`, confirming the successful enrichment during the data generation phase.
*   `ip_country` distribution shows a balanced representation of the simulated countries (US, UK, CA, IN, DE, AU), aligning with the `users_df['country']` distribution, which was used to derive the simulated geo-data. Each country has between 15% and 18% of the transactions.
*   `ip_city` and `ip_region` also show expected distributions based on the simulated helper functions, validating the setup for geographical analysis in Looker Studio.

### 4. Fraud and Compromised Users Distribution

**transactions_df**
*   **is_fraud**: The dataset shows an `is_fraud` distribution of `0` (legitimate) for 9038 transactions and `1` (fraudulent) for 962 transactions. This results in an overall fraud rate of **9.62%** (962/10000), which is slightly higher than the configured `FRAUD_RATE = 0.08` (8%) due to the ATO compromise injection logic, indicating a realistic class imbalance for fraud detection scenarios.

**users_df**
*   **is_compromised**: 949 users are not compromised (`0`), while 51 users are marked as compromised (`1`). This represents **5.1%** of users, closely aligning with the configured `ATO_RATE = 0.05` (5%), validating the simulation of compromised accounts.

### 5. Initial Insights and Patterns

*   **Class Imbalance**: Both `is_fraud` and `is_compromised` columns exhibit significant class imbalance, which is typical for fraud datasets. This highlights the need for models and evaluation metrics that can handle imbalance effectively (e.g., precision, recall, F1-score, `class_weight='balanced'` in `RandomForestClassifier`).
*   **Geolocation Potential**: The `ip_country`, `ip_city`, and `ip_region` fields, along with `ip_latitude` and `ip_longitude`, are now available for geographical analysis. This will be crucial for identifying fraud rings operating from specific locations or anomalous transactions originating from unexpected regions for a given user. For instance, a user's `country` from `users_df` versus the transaction's `ip_country` can be a powerful fraud signal.
*   **ATO Connection**: The `is_compromised` flag in `users_df` is directly linked to the `is_fraud` flag in `transactions_df` through the data generation logic (compromised users have a higher probability of generating fraud). This provides a clear target for identifying the impact of ATO on transaction fraud.

Overall, the EDA confirms that the synthetic data is well-structured, contains the necessary enriched fields, and accurately reflects the intended fraud and user behavior patterns, making it suitable for subsequent analysis, monitoring, and machine learning phases.
