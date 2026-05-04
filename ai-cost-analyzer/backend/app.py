from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app)

# Load data
df = pd.read_csv('data/netflix.csv')

# Load model
model = pickle.load(open('model.pkl', 'rb'))
encoders = pickle.load(open('encoders.pkl', 'rb'))

# ---------------- HOME ----------------
@app.route('/')
def home():
    return "✅ API Running"

# ---------------- REVENUE ----------------
@app.route('/revenue')
def revenue():
    return jsonify({
        "total_revenue": float(df['monthly_fee'].sum())
    })

# ---------------- CHURN ----------------
@app.route('/churn')
def churn():
    rate = (df['churned'] == 'Yes').mean() * 100
    return jsonify({"churn_rate": round(rate, 2)})

# ---------------- WATCH ----------------
@app.route('/watch-time')
def watch():
    avg = df['avg_watch_time_minutes'].mean()
    return jsonify({"average_watch_time": round(avg, 2)})

# ---------------- FILTERED CHART ----------------
@app.route('/revenue-by-plan')
def revenue_by_plan():
    country = request.args.get('country')
    plan = request.args.get('plan')

    filtered = df

    if country and country != "All Countries":
        filtered = filtered[filtered['country'] == country]

    if plan and plan != "All Plans":
        filtered = filtered[filtered['subscription_type'] == plan]

    result = filtered.groupby('subscription_type')['monthly_fee'].sum().to_dict()
    return jsonify(result)

# ---------------- PREDICT ----------------
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    country = encoders['country'].transform([data['country']])[0]
    plan = encoders['subscription_type'].transform([data['subscription']])[0]

    input_df = pd.DataFrame([{
        'age': int(data['age']),
        'country': country,
        'subscription_type': plan,
        'monthly_fee': float(data['monthly_fee']),
        'avg_watch_time_minutes': float(data['watch_time'])
    }])

    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    return jsonify({
        "churn": "Yes" if pred == 1 else "No",
        "confidence": round(prob * 100, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)