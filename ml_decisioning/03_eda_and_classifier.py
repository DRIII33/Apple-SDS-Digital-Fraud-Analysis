import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# -----------------------------
# 1. DATA INGESTION
# -----------------------------
print("Loading transaction data...")
transactions = pd.read_csv("transactions.csv")
transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])

# -----------------------------
# 2. FEATURE ENGINEERING
# -----------------------------
print("Engineering behavioral and temporal features...")
# Temporal signals
transactions['hour'] = transactions['timestamp'].dt.hour
transactions['day_of_week'] = transactions['timestamp'].dt.dayofweek

# User-level behavioral aggregations (Historical context)
user_features = transactions.groupby('user_id').agg(
    avg_amount=('amount', 'mean'),
    max_amount=('amount', 'max'),
    total_transactions=('transaction_id', 'count'),
    distinct_devices=('device_id', 'nunique'),
    distinct_ips=('ip_address', 'nunique')
).reset_index()

# Merge features back to the main dataset
transactions = pd.merge(transactions, user_features, on='user_id', how='left')

# -----------------------------
# 3. PREDICTIVE MODELING (ML CLASSIFIER)
# -----------------------------
print("Training Random Forest Classifier...")
# Select features for the model
features = ['amount', 'hour', 'day_of_week', 'avg_amount', 
            'max_amount', 'total_transactions', 'distinct_devices', 'distinct_ips']

X = transactions[features].fillna(0)
y = transactions['is_fraud']

# Train/Test Split (Stratified to maintain baseline fraud distribution)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize model with class_weight='balanced' to handle the imbalanced nature of fraud data
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# -----------------------------
# 4. OPERATIONAL DECISIONING LAYER
# -----------------------------
print("Applying decisioning logic...")

def decision_engine(fraud_probability):
    """
    Translates model probability into actionable business outcomes.
    Balancing fraud capture (Precision) with Customer Experience (False Positives).
    """
    if fraud_probability > 0.70:
        return "block"    # High confidence fraud -> Auto-decline
    elif fraud_probability > 0.40:
        return "review"   # Gray area -> Send to manual review queue
    else:
        return "approve"  # Low risk -> Frictionless checkout

# Apply model probabilities and decision logic to the entire dataset
transactions['risk_score'] = model.predict_proba(X)[:, 1]
transactions['decision'] = transactions['risk_score'].apply(decision_engine)

# -----------------------------
# 5. BUSINESS IMPACT DASHBOARD METRICS
# -----------------------------
print("\n" + "="*40)
print(" 🍏 APPLE SDS BUSINESS IMPACT METRICS ")
print("="*40)

# Calculate Core KPIs
overall_fraud_rate = transactions['is_fraud'].mean()
block_rate = (transactions['decision'] == 'block').mean()

# Calculate False Positive Rate (Good users impacted by friction)
total_good_txns = transactions[transactions['is_fraud'] == 0].shape[0]
false_positives = transactions[(transactions['is_fraud'] == 0) & (transactions['decision'].isin(['block', 'review']))].shape[0]
fpr = false_positives / total_good_txns

# Calculate Revenue Protected (True Positives successfully blocked)
revenue_protected = transactions[(transactions['decision'] == 'block') & (transactions['is_fraud'] == 1)]['amount'].sum()

print(f"Overall Fraud Exposure: {overall_fraud_rate:.2%}")
print(f"System Block Rate: {block_rate:.2%}")
print(f"False Positive Rate (Friction Index): {fpr:.2%} (Target: Minimize)")
print(f"Estimated Revenue Protected: ${revenue_protected:,.2f}")
print("="*40)
