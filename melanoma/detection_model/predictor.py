import joblib
import os
import numpy as np
from .features_extractor import extract_features
import logging

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    logging.info("Loading Model & Scaler files.")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except FileNotFoundError:
    logging.error("Model or Scaler file not found!")
    model = None
    scaler = None

def predict_melanoma(image_path):
    if model is None or scaler is None:
        return {
            "labels": "Error",
            "confidence": 0.0,
            "message": "Check logs"
        }
    try:
        features = extract_features(image_path)
        features_array = np.array([features])
        scaled_features = scaler.transform(features_array)

        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0]

        result_label = "Malignant" if prediction == 1 else "Benign"
        confidence = probability[prediction] * 100
        return {
            "label": result_label,
            "probability": round(confidence, 2),
            "features": features,
            "message": "Analysis successful"
        }

    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return {
            "label": "Error",
            "probability": 0.0,
            "message": "Check server logs"
        }
