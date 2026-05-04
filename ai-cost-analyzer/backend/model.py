import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv('data/netflix.csv')

# =========================
# CLEAN DATA
# =========================
df = df.dropna()

# =========================
# SELECT REQUIRED FEATURES (ONLY 5)
# =========================
features = [
    'age',
    'country',
    'subscription_type',
    'monthly_fee',
    'avg_watch_time_minutes'
]

# =========================
# ENCODE CATEGORICAL DATA
# =========================
encoders = {}

for col in ['country', 'subscription_type']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# =========================
# TARGET COLUMN (FIXED)
# =========================
df['churned'] = df['churned'].map({'Yes': 1, 'No': 0})

X = df[features]
y = df['churned']

# =========================
# TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# =========================
# EVALUATE MODEL
# =========================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

# =========================
# SAVE MODEL + ENCODERS
# =========================
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(encoders, open('encoders.pkl', 'wb'))

print("✅ Model and encoders saved successfully!")