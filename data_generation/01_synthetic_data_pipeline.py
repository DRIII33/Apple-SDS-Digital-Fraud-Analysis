import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------------
# 1. CONFIGURATION & PARAMETERS
# -----------------------------
NUM_USERS = 1000
NUM_TRANSACTIONS = 10000
FRAUD_RATE = 0.08  # Overall baseline fraud rate
ATO_RATE = 0.05    # Account Takeover compromise rate
np.random.seed(42)

# -----------------------------
# 2. HELPER FUNCTIONS
# -----------------------------
def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def random_device():
    return f"device_{random.randint(1, 3000)}"

def random_country():
    return random.choice(["US", "UK", "CA", "IN", "DE", "AU"])

# -----------------------------
# 3. USERS TABLE GENERATION
# -----------------------------
users = pd.DataFrame({
    "user_id": [f"user_{i}" for i in range(NUM_USERS)],
    "account_age_days": np.random.randint(1, 2000, NUM_USERS),
    "country": [random_country() for _ in range(NUM_USERS)],
})

# Simulate compromised accounts (ATO targets)
users["is_compromised"] = np.random.choice([0, 1], size=NUM_USERS, p=[1-ATO_RATE, ATO_RATE])

# -----------------------------
# 4. TRANSACTIONS TABLE GENERATION
# -----------------------------
transactions = []

for i in range(NUM_TRANSACTIONS):
    user = users.sample(1).iloc[0]
    
    # Introduce temporal variability
    base_time = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    is_fraud = 0
    # Compromised users have a highly elevated risk of generating fraud
    if user["is_compromised"] == 1:
        is_fraud = np.random.choice([0,1], p=[0.6, 0.4])
    # Baseline ambient fraud injection
    elif np.random.rand() < FRAUD_RATE:
        is_fraud = 1

    # Amount distribution: legitimate purchases follow an exponential curve
    amount = np.random.exponential(scale=50)
    
    # Fraudulent transactions tend to have higher variance/amounts to maximize extraction
    if is_fraud:
        amount *= np.random.uniform(1.5, 3)

    transactions.append({
        "transaction_id": f"txn_{i}",
        "user_id": user["user_id"],
        "amount": round(amount, 2),
        "timestamp": base_time,
        "device_id": random_device(),
        "ip_address": random_ip(),
        "is_fraud": is_fraud
    })

transactions_df = pd.DataFrame(transactions)

# Export for BigQuery Upload
transactions_df.to_csv("transactions.csv", index=False)
users.to_csv("users.csv", index=False)
print(f"Data Generation Complete. {len(transactions_df)} transactions generated.")
