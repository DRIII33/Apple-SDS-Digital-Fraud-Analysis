### Data Dictionary for `transactions_dashboard_view`

This data dictionary provides a detailed description of each column in the `transactions_dashboard_view` BigQuery view, which serves as the primary data source for the Looker Studio dashboard. This view combines enriched transaction data with user metadata for comprehensive fraud analysis.

| Column Name                                       | Data Type   | Description                                                                                                                                                                                                                                                                |
| :------------------------------------------------ | :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `transaction_id`                                  | STRING      | A unique identifier for each transaction.                                                                                                                                                                                                                   |
| `user_id`                                         | STRING      | The unique identifier for the user involved in the transaction.                                                                                                                                                                                             |
| `amount`                                          | FLOAT64     | The monetary value of the transaction.                                                                                                                                                                                                                      |
| `device_id`                                       | STRING      | The identifier for the device used to make the transaction.                                                                                                                                                                                                 |
| `ip_address`                                      | STRING      | The IP address from which the transaction originated.                                                                                                                                                                                                       |
| `ip_region`                                       | STRING      | The geographic region derived from the transaction's IP address.                                                                                                                                                                                            |
| `ip_latitude`                                     | FLOAT64     | The latitude coordinate derived from the transaction's IP address.                                                                                                                                                                                          |
| `ip_longitude`                                    | FLOAT64     | The longitude coordinate derived from the transaction's IP address.                                                                                                                                                                                         |
| `is_fraud`                                        | INT64       | A binary indicator (1 if fraudulent, 0 if legitimate) for the transaction.                                                                                                                                                                                  |
| `hour`                                            | INT64       | The hour of the day when the transaction occurred.                                                                                                                                                                                                          |
| `day_of_week`                                     | INT64       | The day of the week (0 for Monday, 6 for Sunday) when the transaction occurred.                                                                                                                                                                             |
| `month`                                           | INT64       | The month of the year when the transaction occurred.                                                                                                                                                                                                        |
| `avg_amount`                                      | FLOAT64     | The average transaction amount for the specific user, calculated based on historical transactions.                                                                                                                                                          |
| `max_amount`                                      | FLOAT64     | The maximum transaction amount observed for the specific user.                                                                                                                                                                                              |
| `total_transactions`                              | INT64       | The total number of transactions made by the specific user.                                                                                                                                                                                                 |
| `distinct_devices`                                | INT64       | The number of unique devices used by the specific user.                                                                                                                                                                                                     |
| `distinct_ips`                                    | INT64       | The number of unique IP addresses used by the specific user.                                                                                                                                                                                                |
| `account_age_days`                                | INT64       | The age of the user's account in days at the time of the transaction.                                                                                                                                                                                       |
| `is_cross_country_txn`                            | INT64       | A binary indicator (1 if the transaction's IP country differs from the user's registered country, 0 otherwise).                                                                                                                                             |
| `risk_score`                                      | FLOAT64     | The fraud risk score predicted by the machine learning model for the transaction.                                                                                                                                                                           |
| `decision`                                        | STRING      | The operational decision ('block', 'review', or 'approve') based on the risk_score.                                                                                                                                                                         |
| `transaction_timestamp`                           | DATETIME    | The date and time of the transaction, cast to DATETIME type.                                                                                                                                                                                                |
| `transaction_ip_country`                          | STRING      | The country derived from the transaction's IP address. This field was explicitly aliased in the view.                                                                                                                                                       |
| `user_registered_country`                         | STRING      | The country where the user is registered (from the merged transactions data).                                                                                                                                                                                             |
| `user_account_age_days_from_users_table`          | INT64       | The age of the user's account in days, sourced directly from the users_temp table during the view creation.                                                                                                                                                   |
| `user_registered_country_from_users_table`        | STRING      | The registered country of the user, sourced directly from the users_temp table during the view creation.                                                                                                                                                  |
| `is_compromised`                                  | INT64       | A binary indicator (1 if the user's account is compromised, 0 otherwise) from the users_temp table, joined into the view.                                                                                                                                     |

### Data Dictionary for `fraud_kpis_precalculated_view`

This data dictionary describes the columns available in the `fraud_kpis_precalculated_view` BigQuery view. This view aggregates daily operational metrics for efficient consumption by Looker Studio scorecards and time series charts, reducing computation overhead in the dashboard.

| Column Name            | Data Type | Description                                                                                                                                                           |
| :--------------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `transaction_date`     | DATE      | The calendar date for which the metrics are aggregated.                                                                                                               |
| `total_txns`           | INT64     | The total number of transactions that occurred on `transaction_date`.                                                                                                 |
| `fraud_txns`           | INT64     | The total number of fraudulent transactions (`is_fraud = 1`) on `transaction_date`.                                                                                   |
| `block_txns`           | INT64     | The total number of transactions that were automatically blocked by the system (`decision = 'block'`) on `transaction_date`.                                              |
| `review_txns`          | INT64     | The total number of transactions that were sent for manual review by the system (`decision = 'review'`) on `transaction_date`.                                          |
| `false_positives_count`| INT64     | The count of legitimate transactions (`is_fraud = 0`) that were incorrectly flagged as 'block' or 'review' by the system on `transaction_date`.                     |
| `total_legit_txns`     | INT64     | The total number of legitimate transactions (`is_fraud = 0`) on `transaction_date`.                                                                                   |
| `revenue_protected_amount`| FLOAT64   | The total monetary value of fraudulent transactions that were either blocked or sent for review (`is_fraud = 1` and `decision IN ('block', 'review')`) on `transaction_date`. |

### Data Dictionary for `fraud_kpi_summary_view`

This data dictionary outlines the aggregate KPI metrics provided by the `fraud_kpi_summary_view` BigQuery view. This view contains a single row with overall project-level metrics, optimized for Looker Studio scorecards requiring a single aggregate value.

| Column Name                   | Data Type | Description                                                                                                                                                                                             |
| :---------------------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `overall_fraud_rate`          | FLOAT64   | The overall proportion of all transactions that are fraudulent across the entire dataset.                                                                                                                 |
| `system_block_rate`           | FLOAT64   | The overall proportion of all transactions that were automatically blocked by the system across the entire dataset.                                                                                   |
| `system_review_rate`          | FLOAT64   | The overall proportion of all transactions that were sent for manual review by the system across the entire dataset.                                                                                  |
| `false_positive_rate`         | FLOAT64   | The overall proportion of legitimate transactions (`is_fraud = 0`) that were incorrectly blocked by the system (`decision = 'block'`) across the entire dataset.                                |
| `estimated_revenue_protected` | FLOAT64   | The overall total monetary value of fraudulent transactions that were either blocked or sent for review (`is_fraud = 1` and `decision IN ('block', 'review')`) across the entire dataset. |

### Data Dictionary for `transactions_enriched`

This data dictionary describes the columns in the `transactions_enriched` BigQuery table, which contains the original transaction data augmented with feature-engineered columns, ML model risk scores, and operational decisions.

| Column Name             | Data Type | Description                                                                                                                   |
| :---------------------- | :-------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `transaction_id`        | STRING    | A unique identifier for each transaction.                                                                                     |
| `user_id`               | STRING    | The unique identifier for the user involved in the transaction.                                                               |
| `amount`                | FLOAT64   | The monetary value of the transaction.                                                                                        |
| `timestamp`             | STRING    | The date and time of the transaction (stored as string after CSV export, cast to DATETIME in views).                          |
| `device_id`             | STRING    | The identifier for the device used to make the transaction.                                                                   |
| `ip_address`            | STRING    | The IP address from which the transaction originated.                                                                         |
| `ip_country`            | STRING    | The country derived from the transaction's IP address.                                                                        |
| `ip_city`               | STRING    | The city derived from the transaction's IP address.                                                                           |
| `ip_region`             | STRING    | The geographic region derived from the transaction's IP address.                                                              |
| `ip_latitude`           | FLOAT64   | The latitude coordinate derived from the transaction's IP address.                                                            |
| `ip_longitude`          | FLOAT64   | The longitude coordinate derived from the transaction's IP address.                                                           |
| `is_fraud`              | INT64     | A binary indicator (1 if fraudulent, 0 if legitimate) for the transaction.                                                    |
| `hour`                  | INT64     | The hour of the day when the transaction occurred.                                                                            |
| `day_of_week`           | INT64     | The day of the week (0-6) when the transaction occurred.                                                                      |
| `month`                 | INT64     | The month of the year when the transaction occurred.                                                                          |
| `avg_amount`            | FLOAT64   | The average transaction amount for the specific user (feature-engineered).                                                    |
| `max_amount`            | FLOAT64   | The maximum transaction amount observed for the specific user (feature-engineered).                                           |
| `total_transactions`    | INT64     | The total number of transactions made by the specific user (feature-engineered).                                              |
| `distinct_devices`      | INT64     | The number of unique devices used by the specific user (feature-engineered).                                                  |
| `distinct_ips`          | INT64     | The number of unique IP addresses used by the specific user (feature-engineered).                                             |
| `account_age_days`      | INT64     | The age of the user's account in days (feature-engineered from `users_temp`).                                                 |
| `user_registered_country`| STRING    | The country where the user is registered (from `users_temp` merged into `transactions_enriched`).                           |
| `is_cross_country_txn`  | INT64     | A binary indicator (1 if transaction IP country differs from user's registered country, 0 otherwise).                       |
| `ip_country_AU`         | BOOL      | Boolean indicator if the transaction's IP country was Australia (one-hot encoded feature).                                    |
| `ip_country_CA`         | BOOL      | Boolean indicator if the transaction's IP country was Canada (one-hot encoded feature).                                       |
| `ip_country_DE`         | BOOL      | Boolean indicator if the transaction's IP country was Germany (one-hot encoded feature).                                      |
| `ip_country_IN`         | BOOL      | Boolean indicator if the transaction's IP country was India (one-hot encoded feature).                                        |
| `ip_country_UK`         | BOOL      | Boolean indicator if the transaction's IP country was United Kingdom (one-hot encoded feature).                               |
| `ip_country_US`         | BOOL      | Boolean indicator if the transaction's IP country was United States (one-hot encoded feature).                                |
| `ip_city_Bangalore`     | BOOL      | Boolean indicator if the transaction's IP city was Bangalore (one-hot encoded feature).                                       |
| `ip_city_Berlin`        | BOOL      | Boolean indicator if the transaction's IP city was Berlin (one-hot encoded feature).                                          |
| `ip_city_Birmingham`    | BOOL      | Boolean indicator if the transaction's IP city was Birmingham (one-hot encoded feature).                                      |
| `ip_city_Brisbane`      | BOOL      | Boolean indicator if the transaction's IP city was Brisbane (one-hot encoded feature).                                        |
| `ip_city_Chicago`       | BOOL      | Boolean indicator if the transaction's IP city was Chicago (one-hot encoded feature).                                         |
| `ip_city_Delhi`         | BOOL      | Boolean indicator if the transaction's IP city was Delhi (one-hot encoded feature).                                           |
| `ip_city_Frankfurt`     | BOOL      | Boolean indicator if the transaction's IP city was Frankfurt (one-hot encoded feature).                                       |
| `ip_city_Houston`       | BOOL      | Boolean indicator if the transaction's IP city was Houston (one-hot encoded feature).                                         |
| `ip_city_London`        | BOOL      | Boolean indicator if the transaction's IP city was London (one-hot encoded feature).                                          |
| `ip_city_Los Angeles`   | BOOL      | Boolean indicator if the transaction's IP city was Los Angeles (one-hot encoded feature).                                     |
| `ip_city_Manchester`    | BOOL      | Boolean indicator if the transaction's IP city was Manchester (one-hot encoded feature).                                      |
| `ip_city_Melbourne`     | BOOL      | Boolean indicator if the transaction's IP city was Melbourne (one-hot encoded feature).                                       |
| `ip_city_Montreal`      | BOOL      | Boolean indicator if the transaction's IP city was Montreal (one-hot encoded feature).                                        |
| `ip_city_Mumbai`        | BOOL      | Boolean indicator if the transaction's IP city was Mumbai (one-hot encoded feature).                                          |
| `ip_city_Munich`        | BOOL      | Boolean indicator if the transaction's IP city was Munich (one-hot encoded feature).                                          |
| `ip_city_New York`      | BOOL      | Boolean indicator if the transaction's IP city was New York (one-hot encoded feature).                                        |
| `ip_city_Sydney`        | BOOL      | Boolean indicator if the transaction's IP city was Sydney (one-hot encoded feature).                                          |
| `ip_city_Toronto`       | BOOL      | Boolean indicator if the transaction's IP city was Toronto (one-hot encoded feature).                                         |
| `ip_city_Vancouver`     | BOOL      | Boolean indicator if the transaction's IP city was Vancouver (one-hot encoded feature).                                       |
| `risk_score`            | FLOAT64   | The fraud risk score predicted by the machine learning model for the transaction.                                             |
| `decision`              | STRING    | The operational decision ('block', 'review', or 'approve') based on the risk_score.                                           |

### Data Dictionary for `transactions_temp`

This data dictionary describes the columns in the `transactions_temp` BigQuery table, which holds the initial synthetic transaction data after geo-enrichment.

| Column Name      | Data Type | Description                                                                 |
| :--------------- | :-------- | :-------------------------------------------------------------------------- |
| `transaction_id` | STRING    | A unique identifier for each transaction.                                   |
| `user_id`        | STRING    | The unique identifier for the user involved in the transaction.             |
| `amount`         | FLOAT64   | The monetary value of the transaction.                                      |
| `timestamp`      | TIMESTAMP | The date and time of the transaction.                                       |
| `device_id`      | STRING    | The identifier for the device used to make the transaction.                 |
| `ip_address`     | STRING    | The IP address from which the transaction originated.                       |
| `ip_country`     | STRING    | The country derived from the transaction's IP address.                      |
| `ip_city`        | STRING    | The city derived from the transaction's IP address.                         |
| `ip_region`      | STRING    | The geographic region derived from the transaction's IP address.            |
| `ip_latitude`    | FLOAT64   | The latitude coordinate derived from the transaction's IP address.          |
| `ip_longitude`   | FLOAT64   | The longitude coordinate derived from the transaction's IP address.         |
| `is_fraud`       | INT64     | A binary indicator (1 if fraudulent, 0 if legitimate) for the transaction. |

### Data Dictionary for `users_temp`

This data dictionary describes the columns in the `users_temp` BigQuery table, which holds the initial synthetic user metadata.

| Column Name        | Data Type | Description                                                                 |
| :----------------- | :-------- | :-------------------------------------------------------------------------- |
| `user_id`          | STRING    | The unique identifier for each user.                                        |
| `account_age_days` | INT64     | The age of the user's account in days.                                      |
| `country`          | STRING    | The registered country of the user.                                         |
| `is_compromised`   | INT64     | A binary indicator (1 if the user's account is compromised, 0 otherwise). |v
