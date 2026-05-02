-- Query 1: Daily Fraud Rate & Revenue Impact (Executive Monitoring)
-- Purpose: Provides a high-level overview of daily fraud trends and associated financial exposure.
-- Maps to JD: "Track operational and business metrics"
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
