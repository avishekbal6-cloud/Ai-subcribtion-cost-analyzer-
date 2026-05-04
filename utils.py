import pandas as pd
import pickle

# -------------------------------
# 🔹 Load Model & Encoders
# -------------------------------
def load_model():
    model = pickle.load(open('model.pkl', 'rb'))
    encoders = pickle.load(open('encoders.pkl', 'rb'))
    return model, encoders


# -------------------------------
# 🔹 Predict Churn Function
# -------------------------------
def predict_churn(model, encoders, data):

    # Convert input to DataFrame
    df = pd.DataFrame([data])

    # Encode categorical columns safely
    for col, encoder in encoders.items():
        if col in df.columns:
            try:
                df[col] = encoder.transform(df[col])
            except:
                # Handle unseen values
                df[col] = 0

    # Ensure column order matches training
    expected_columns = model.feature_names_in_
    df = df.reindex(columns=expected_columns, fill_value=0)

    # Prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    # Return clean output for frontend
    return {
        "prediction": "Yes" if prediction == 1 else "No",
        "confidence": round(probability * 100, 2)
    }