# This file contains function to recreate the image used for extracting features from the image
# Input: Image path
# Output: base64 of edited image
# reason for base64 is to include in the HTML without storing the edited image
# NOTE:
# Border is not being added to the masked image.
import cv2
import base64
from .predictor import predict_melanoma
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def visualizer(image_path) -> None | dict:
    """
    visualizer
    @param image_path: full path of the image
    @return: dict of base64 encoded webp filetype of masked and contour images | None (if failed to read the image)

    visualizer function is used to create the border of how the computer detects the boundary of the cancer.
    Returns dict { "masked_image", "contour_image" }
    """
    image = cv2.imread(image_path)
    if image is None:
        logging.error("Failed to read image.")
        return None

    image = cv2.resize(image, (200,200))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _,mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contour_img = image.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

    def return_label():
        predict = predict_melanoma(image_path)
        return predict['label']

    # added border function, might remove it later
    def add_border(img, _label):
        top = int(0.05 * img.shape[0]) # top, bottom, left, right code was added from cv2 example
        bottom = top
        left = int(0.05 * img.shape[1])
        right = left
        color_value = (0, 0, 255) if _label == 'Malignant' else (255, 0, 0)
        border_image = cv2.copyMakeBorder(img,
                                          top= top,
                                          bottom=bottom,
                                          left=left,
                                          right=right,
                                          borderType=cv2.BORDER_CONSTANT,
                                          value=color_value)
        return border_image

    def to_base(img):
        encode_param = (cv2.IMWRITE_WEBP_QUALITY, 100)
        return_val, buffer = cv2.imencode('.webp', img, encode_param)
        if return_val:
            return base64.b64encode(buffer).decode('utf-8')
        else:
            return None

    label = return_label()
    border_mask_image = add_border(mask, label)
    border_contour_image = add_border(contour_img, label)

    return {
        "mask_image": to_base(border_mask_image),
        "contour_image": to_base(border_contour_image)
    }
