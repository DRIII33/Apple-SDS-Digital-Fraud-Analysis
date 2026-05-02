CREATE OR REPLACE VIEW `driiiportfolio.fraud_analysis_data.transactions_dashboard_view` AS
SELECT
    t.* EXCEPT(timestamp, user_registered_country, ip_country), -- Exclude ip_country here as we'll select it with an alias
    CAST(t.timestamp AS DATETIME) AS transaction_timestamp,
    t.ip_country AS transaction_ip_country, -- Explicitly include and alias ip_country
    t.user_registered_country,
    u.account_age_days AS user_account_age_days_from_users_table,
    u.country AS user_registered_country_from_users_table,
    u.is_compromised
FROM
    `driiiportfolio.fraud_analysis_data.transactions_enriched` AS t
JOIN
    `driiiportfolio.fraud_analysis_data.users_temp` AS u
ON
    t.user_id = u.user_id;
