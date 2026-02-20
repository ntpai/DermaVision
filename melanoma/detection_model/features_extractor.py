import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

def extract_features(image_path) -> list:
    """
    extract_features function is used to extract the ABCD (Asymmetric, Border, Color, Diameter) and
    GLCM (Textures) from the given image

    @param image_path: requires path to image.
    @return: [Asymmetry, Border, Color, Diameter, Contrast, Energy]

    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Couldn't open the {image_path} file!")

    image = cv2.resize(image, (200, 200))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # PART A (ABCD Features)
    # A features

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Here threshold value has no use only the image is required.
    # Using binary inversion and Otsu's algorithm
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    height, width = mask.shape
    center_x = width // 2
    left_side = mask[:, :center_x]
    right_side = mask[:, center_x:]
    right_flipped = cv2.flip(right_side, 1)
    diff = cv2.absdiff(left_side, right_flipped)
    asymmetry = np.count_nonzero(diff) / (np.count_nonzero(mask) + 1)

    # B features
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)
        border = (perimeter ** 2) / (4 * np.pi * area) if area > 0 else 0
    else:
        border = 0
        area = 0

    # C features (Color Standard Deviation)

    mean, std_dev = cv2.meanStdDev(image, mask)
    color_std = np.mean(std_dev)

    # D features
    diameter = np.sqrt(4 * area / np.pi) if area > 0 else 0

    # PART B GLCM Features
    glcm = graycomatrix(gray, distances=[1], angles=[0], levels=256,
                        symmetric=True, normed=True)

    contrast = graycoprops(glcm, 'contrast')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]

    return [asymmetry, border, color_std, diameter, contrast, energy]