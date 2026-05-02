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
GEO_MISMATCH_RATE = 0.03  # 3% of transactions will have a geo-mismatch
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

def get_simulated_geo(ip_address, country):
    # For simplicity, map IP to a city within the already assigned country
    # In a real scenario, this would be an actual IP lookup service
    if country == "US":
        cities = ["New York", "Los Angeles", "Chicago", "Houston"]
    elif country == "UK":
        cities = ["London", "Manchester", "Birmingham"]
    elif country == "CA":
        cities = ["Toronto", "Vancouver", "Montreal"]
    elif country == "IN":
        cities = ["Mumbai", "Delhi", "Bangalore"]
    elif country == "DE":
        cities = ["Berlin", "Munich", "Frankfurt"]
    elif country == "AU":
        cities = ["Sydney", "Melbourne", "Brisbane"]
    else:
        cities = ["Unknown"]

    return {
        "ip_city": random.choice(cities),
        "ip_region": f"Region_{country}_{random.randint(1,3)}", # Simulated region
        "ip_latitude": round(random.uniform(-90, 90), 4), # Placeholder
        "ip_longitude": round(random.uniform(-180, 180), 4) # Placeholder
    }


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
all_possible_countries = ["US", "UK", "CA", "IN", "DE", "AU"]

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

    current_ip = random_ip()

    # --- Geo-Mismatch Logic ---
    transaction_ip_country = user["country"] # Default to user's registered country
    if np.random.rand() < GEO_MISMATCH_RATE:
        # If a geo-mismatch is to occur, choose a different country
        available_countries_for_mismatch = [c for c in all_possible_countries if c != user["country"]]
        if available_countries_for_mismatch: # Ensure there are other countries to pick from
            transaction_ip_country = random.choice(available_countries_for_mismatch)
        # If for some reason only one country is available, or user's country is the only option,
        # it will default to user["country"], effectively skipping mismatch for this transaction.
    # --- End Geo-Mismatch Logic ---

    geo_data = get_simulated_geo(current_ip, transaction_ip_country) # Pass the chosen ip_country

    transactions.append({
        "transaction_id": f"txn_{i}",
        "user_id": user["user_id"],
        "amount": round(amount, 2),
        "timestamp": base_time,
        "device_id": random_device(),
        "ip_address": current_ip,
        "ip_country": transaction_ip_country, # Use the potentially mismatched country
        "ip_city": geo_data["ip_city"],
        "ip_region": geo_data["ip_region"],
        "ip_latitude": geo_data["ip_latitude"],
        "ip_longitude": geo_data["ip_longitude"],
        "is_fraud": is_fraud
    })

transactions_df = pd.DataFrame(transactions)

# Export for BigQuery Upload
transactions_df.to_csv("transactions.csv", index=False)
users.to_csv("users.csv", index=False)
print(f"Data Generation Complete. {len(transactions_df)} transactions generated.")
