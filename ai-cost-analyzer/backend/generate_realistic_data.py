import pandas as pd
import random

countries = ["India", "USA", "UK", "Canada", "Germany"]
plans = ["Basic", "Standard", "Premium"]

data = []

for i in range(1000):
    age = random.randint(18, 60)
    country = random.choice(countries)
    plan = random.choice(plans)

    # Monthly fee based on plan
    if plan == "Basic":
        fee = random.choice([200, 300])
    elif plan == "Standard":
        fee = random.choice([500, 800])
    else:
        fee = random.choice([1000, 1500])

    # Watch time behavior
    watch_time = random.randint(1, 300)

    # 🎯 REALISTIC CHURN LOGIC
    churn_prob = 0

    if watch_time < 50:
        churn_prob += 0.5
    elif watch_time < 100:
        churn_prob += 0.3
    else:
        churn_prob -= 0.3

    if plan == "Basic":
        churn_prob += 0.3
    elif plan == "Premium":
        churn_prob -= 0.2

    if fee > 1000 and watch_time < 100:
        churn_prob += 0.4

    churn = "Yes" if random.random() < churn_prob else "No"

    data.append({
        "age": age,
        "country": country,
        "subscription_type": plan,
        "monthly_fee": fee,
        "avg_watch_time_minutes": watch_time,
        "churned": churn
    })

# Save CSV
df = pd.DataFrame(data)
df.to_csv("data/netflix.csv", index=False)

print("✅ Realistic dataset with 1000 rows created!")