import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.calibration import CalibratedClassifierCV # Added for probability calibration

# 1. LOAD DATA
# In a production environment, data would be loaded directly from BigQuery
# For this script, we'll load from the generated CSVs.
print("Loading dataframes from CSVs...")
transactions_df = pd.read_csv("transactions.csv")
transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
users_df = pd.read_csv("users.csv")

# 2. FEATURE ENGINEERING (Translating raw data into behavioral signals)

# Extract temporal features
transactions_df['hour'] = transactions_df['timestamp'].dt.hour
transactions_df['day_of_week'] = transactions_df['timestamp'].dt.dayofweek
transactions_df['month'] = transactions_df['timestamp'].dt.month

# User-level aggregations to capture historical behavior
user_features = transactions_df.groupby('user_id').agg(
    avg_amount=('amount', 'mean'),
    max_amount=('amount', 'max'),
    total_transactions=('transaction_id', 'count'),
    distinct_devices=('device_id', 'nunique'),
    distinct_ips=('ip_address', 'nunique')
).reset_index()

# Merge user-level features back to main transaction dataset
transactions_df = pd.merge(transactions_df, user_features, on='user_id', how='left')

# Merge users_df to get user's registered country and account age
# Explicitly rename 'country' from users_df to avoid potential conflicts and ensure clarity
users_country_info = users_df[['user_id', 'account_age_days', 'country']].rename(columns={'country': 'user_registered_country'})
transactions_df = pd.merge(transactions_df, users_country_info, on='user_id', how='left')

# Create a flag for cross-country transactions
transactions_df['is_cross_country_txn'] = (transactions_df['ip_country'] != transactions_df['user_registered_country']).astype(int)

# --- One-hot encode categorical geolocation features for the MODEL features (X) only ---
# Create a copy of transactions_df for model feature preparation to preserve original categorical columns
X_model_data = transactions_df.copy()

geo_categorical_features_for_model = ['ip_country', 'ip_city']
X_model_data = pd.get_dummies(X_model_data, columns=geo_categorical_features_for_model, prefix=geo_categorical_features_for_model)

# Define the final list of features for the model (X)
features = [
    'amount', 'hour', 'day_of_week', 'month',
    'avg_amount', 'max_amount', 'total_transactions', 'distinct_devices', 'distinct_ips',
    'account_age_days', 'ip_latitude', 'ip_longitude', 'is_cross_country_txn'
] + [col for col in X_model_data.columns if col.startswith('ip_country_') or col.startswith('ip_city_')]

# Ensure all features exist in X_model_data, if not, create dummy columns filled with 0 (for consistency)
for f in features:
    if f not in X_model_data.columns:
        X_model_data[f] = 0

X = X_model_data[features].fillna(0) # Fill NaNs if any after merges
y = transactions_df['is_fraud'] # Target variable from original transactions_df

# Train/Test Split (Stratified to maintain fraud baseline)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Random Forest with class_weight='balanced' to handle fraud data imbalance natively
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Model Evaluation (on test set with original thresholds for initial assessment)
y_pred = model.predict(X_test)
print("\n--- Model Evaluation (Original Thresholds on Test Set) ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall: {recall_score(y_test, y_pred):.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# 4. DECISIONING LAYER (Core Operational Output)
# Maps to JD: "Decision orders in mass or individually"
# Adjusted thresholds based on PR curve analysis to improve recall
def decision_engine_adjusted(fraud_probability, block_threshold=0.25, review_threshold=0.10):
    """
    Translates model probability into actionable business outcomes,
    balancing security with customer friction, with adjusted thresholds.
    """
    if fraud_probability > block_threshold:
        return "block"    # High confidence fraud: Auto-decline
    elif fraud_probability > review_threshold:
        return "review"   # Gray area: Send to manual review queue
    else:
        return "approve"  # Low risk: Frictionless checkout

# Apply risk scores and decisions to the entire dataset using adjusted thresholds
# CalibratedClassifierCV is used for probabilities, fit on full data for overall business metrics
calibrated_model = CalibratedClassifierCV(model, method='isotonic', cv=5)
calibrated_model.fit(X, y) # Fit on full data for overall probabilities

transactions_df['risk_score'] = calibrated_model.predict_proba(X)[:, 1]
transactions_df['decision'] = transactions_df['risk_score'].apply(decision_engine_adjusted)

# 5. BUSINESS IMPACT METRICS
fraud_rate = transactions_df['is_fraud'].mean()
block_rate = (transactions_df['decision'] == 'block').mean()
review_rate = (transactions_df['decision'] == 'review').mean()
approve_rate = (transactions_df['decision'] == 'approve').mean()

# Calculate False Positive Rate (FPR) - Crucial for customer experience
total_good_txns = transactions_df[transactions_df['is_fraud'] == 0].shape[0]
false_positives = transactions_df[(transactions_df['is_fraud'] == 0) & (transactions_df['decision'].isin(['block', 'review']))].shape[0]
fpr = false_positives / total_good_txns if total_good_txns > 0 else 0

# Calculate Revenue Protected (True Positives that were blocked or reviewed and would have been fraud)
revenue_protected_blocked = transactions_df[(transactions_df['decision'] == 'block') & (transactions_df['is_fraud'] == 1)]['amount'].sum()
revenue_protected_reviewed = transactions_df[(transactions_df['decision'] == 'review') & (transactions_df['is_fraud'] == 1)]['amount'].sum()
revenue_protected = revenue_protected_blocked + revenue_protected_reviewed

# Calculate true positive rates for different decisions
true_positives_blocked = transactions_df[(transactions_df['decision'] == 'block') & (transactions_df['is_fraud'] == 1)].shape[0]
true_positives_reviewed = transactions_df[(transactions_df['decision'] == 'review') & (transactions_df['is_fraud'] == 1)].shape[0]

total_fraud = transactions_df[transactions_df['is_fraud'] == 1].shape[0]
recall_blocked = true_positives_blocked / total_fraud if total_fraud > 0 else 0
recall_blocked_and_reviewed = (true_positives_blocked + true_positives_reviewed) / total_fraud if total_fraud > 0 else 0

print("\n--- Apple SDS Analytics Summary (Post-Modeling with Adjusted Thresholds) ---")
print(f"Overall Fraud Rate: {fraud_rate:.2%}")
print(f"System Block Rate: {block_rate:.2%}")
print(f"System Review Rate: {review_rate:.2%}")
print(f"System Approve Rate: {approve_rate:.2%}")
print(f"False Positive Rate (Friction Index - Block/Review): {fpr:.2%}")
print(f"Recall (Blocked Fraud): {recall_blocked:.2%}")
print(f"Recall (Blocked + Reviewed Fraud): {recall_blocked_and_reviewed:.2%}")
print(f"Estimated Revenue Protected: ${revenue_protected:,.2f}")

# Export the enriched dataset (with risk scores and decisions) for potential dashboard integration
transactions_df.to_csv("transactions_final.csv", index=False)
print("\nEnriched dataset 'transactions_final.csv' is ready for further analysis/upload.")
