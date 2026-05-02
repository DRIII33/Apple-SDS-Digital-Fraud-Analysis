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
