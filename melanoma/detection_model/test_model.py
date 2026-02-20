import os.path
import joblib
from features_extractor import extract_features
from sys import argv, exit
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'

def test_image(image_path):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        logging.error("Missing model or scalar file!")
        return

    if not os.path.exists(image_path):
        logging.error("Image path does not exists!")
        return
    logging.info("Loading model and scalar files...")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    try:
        features = extract_features(image_path=image_path)
        logging.info("Extraction complete.")
    except Exception as e:
        logging.error(f"Error during feature extraction: {e.__str__()}")

    features_scaled = scaler.transform([features])

    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]

    result = "MALIGNANT" if prediction == 1 else "BENIGN"
    confidence = probability[prediction] * 100

    print(f"Result: {result}")
    print(f"Confidence: {confidence}")

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python test_model.py [image_path]")
        exit()
    test_image(argv[1])