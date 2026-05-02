-- Query 5: Cross-Country Transactions (Geo-Mismatch Detection)
-- Purpose: Identifies transactions where the ip_country of the transaction differs from the user's registered country.
-- This is a strong indicator of potential Account Takeover (ATO) or high-risk activity, directly mapping to
-- "analyzing complex fraud scenarios" and "identifying fraud patterns."
-- New Query: Joins transactions_temp and users_temp to leverage both enriched datasets.
SELECT
    t.user_id,
    u.country AS user_registered_country,
    t.ip_country AS transaction_ip_country,
    COUNT(t.transaction_id) AS total_cross_country_txns,
    SUM(t.is_fraud) AS fraud_cross_country_txns,
    ROUND(SUM(t.amount), 2) AS total_amount_cross_country_txns
FROM
    `driiiportfolio.fraud_analysis_data.transactions_temp` AS t
JOIN
    `driiiportfolio.fraud_analysis_data.users_temp` AS u
ON
    t.user_id = u.user_id
WHERE
    t.ip_country <> u.country
GROUP BY
    t.user_id, u.country, t.ip_country
ORDER BY
    fraud_cross_country_txns DESC, total_cross_country_txns DESC;
```
