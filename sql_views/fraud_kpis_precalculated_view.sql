CREATE OR REPLACE VIEW `driiiportfolio.fraud_analysis_data.fraud_kpis_precalculated_view` AS
SELECT
    DATE(transaction_timestamp) AS transaction_date,
    COUNT(transaction_id) AS total_txns,
    SUM(is_fraud) AS fraud_txns,
    SUM(CASE WHEN decision = 'block' THEN 1 ELSE 0 END) AS block_txns,
    SUM(CASE WHEN decision = 'review' THEN 1 ELSE 0 END) AS review_txns,
    SUM(CASE WHEN is_fraud = 0 AND (decision = 'block' OR decision = 'review') THEN 1 ELSE 0 END) AS false_positives_count,
    SUM(CASE WHEN is_fraud = 0 THEN 1 ELSE 0 END) AS total_legit_txns,
    SUM(CASE WHEN is_fraud = 1 AND (decision = 'block' OR decision = 'review') THEN amount ELSE 0 END) AS revenue_protected_amount
FROM
    `driiiportfolio.fraud_analysis_data.transactions_dashboard_view`
GROUP BY
    transaction_date
ORDER BY
    transaction_date;
