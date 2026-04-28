-- Query 1: Daily Fraud Rate & Revenue Impact (Executive Monitoring)
SELECT
    DATE(timestamp) AS transaction_date,
    COUNT(transaction_id) AS total_txns,
    SUM(is_fraud) AS fraud_txns,
    ROUND(SUM(is_fraud)*1.0 / COUNT(transaction_id), 4) AS daily_fraud_rate,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2) AS financial_exposure
FROM 
    `driiiportfolio.fraud_analysis_data.transactions_temp`
GROUP BY 
    transaction_date
ORDER BY 
    transaction_date DESC;

-----------
-- Query 2: High-Risk User Velocity (ATO Detection)
SELECT
    user_id,
    COUNT(transaction_id) AS txn_count,
    SUM(is_fraud) AS confirmed_fraud_count,
    ROUND(SUM(amount), 2) AS total_spend
FROM 
    `driiiportfolio.fraud_analysis_data.transactions_temp`
GROUP BY 
    user_id
HAVING 
    confirmed_fraud_count > 3
ORDER BY 
    confirmed_fraud_count DESC;

-----------
-- Query 3: Excessive Device Sharing (Botnet / Fraud Ring Detection)
SELECT
    device_id,
    COUNT(DISTINCT user_id) AS unique_users_on_device,
    COUNT(transaction_id) AS total_device_txns,
    SUM(is_fraud) AS fraud_count_on_device
FROM 
    `driiiportfolio.fraud_analysis_data.transactions_temp`
GROUP BY 
    device_id
HAVING 
    unique_users_on_device > 5
ORDER BY 
    unique_users_on_device DESC;
