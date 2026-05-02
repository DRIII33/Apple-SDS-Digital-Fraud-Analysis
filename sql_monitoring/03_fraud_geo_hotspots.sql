-- Query 4: Fraud by IP Country/City (Geographical Fraud Hotspots)
-- Purpose: Pinpoints specific geographical locations (ip_country, ip_city) that are experiencing higher fraud rates or volumes.
-- This is crucial for "performing analyses to identify fraud patterns" related to geographic origin.
-- New Query: Directly leverages the newly added ip_country and ip_city fields for geographical analysis.
SELECT
    ip_country,
    ip_city,
    COUNT(transaction_id) AS total_txns,
    SUM(is_fraud) AS fraud_txns,
    ROUND(SUM(is_fraud)*1.0 / COUNT(transaction_id), 4) AS fraud_rate_by_location,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2) AS financial_exposure_by_location
FROM
    `driiiportfolio.fraud_analysis_data.transactions_temp`
GROUP BY
    ip_country,
    ip_city
ORDER BY
    fraud_txns DESC, fraud_rate_by_location DESC;
