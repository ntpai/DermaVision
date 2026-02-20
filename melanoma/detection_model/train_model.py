import os
import joblib
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from features_extractor import extract_features
import numpy as np

dataset_path = 'dataset'
MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
SCALER_FILE_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

def load_data(dir_path):
    features = []
    labels  = []
    categories = ['benign', 'malignant']

    for category in categories:
        _label = 0 if category == 'benign' else 1 # To determine if the image is benign or malignant
        image_dir = os.path.join(dir_path, category)
        if not os.path.exists(image_dir):
            print(f"Folder for {category} not found in the dataset!")
            continue
        for image_file in os.listdir(image_dir):
            image_path = os.path.join(image_dir, image_file)
            try:
                _features = extract_features(image_path)
                features.append(_features)
                labels .append(_label)
            except Exception as e:
                print(f"Image {image_path} skipped! : {e}")

    return np.array(features), np.array(labels)

def train():
    x, y = load_data(dataset_path)
    if len(x) == 0 :
        print("Error Loading data!")
        return

    print(f"Extracted {len(x)} features!")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10)

    scalar = StandardScaler()
    x_train_scalar = scalar.fit_transform(x_train)
    x_test_scalar = scalar.transform(x_test)

    model = SVC(kernel='rbf', probability=True)
    print("Training model")
    model.fit(x_train_scalar, y_train)

    predictions = model.predict(x_test_scalar)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy {accuracy * 100:.2f}%")

    joblib.dump(model, MODEL_FILE_PATH)
    joblib.dump(scalar, SCALER_FILE_PATH)
    print(f"Model & scalar saved to {MODEL_FILE_PATH} & {SCALER_FILE_PATH}")

if __name__ == "__main__":
    train()