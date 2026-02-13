from predictor import extract_features

path = "/home/dev/DermaVision/melanoma/detection_model/train/benign/melanoma_0.jpg"

features = extract_features(path)

print(features)