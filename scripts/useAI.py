import pathlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import tensorflow as tf

from tensorflow import keras

import cv2
import sys

# ==========================================#
# ========== GLobal variables ==============#
# ==========================================#
imgPath = "../original_images/to_be_cut/kuva22.png"
rectangles = np.load("rectangles.npy")
class_names = ["free", "occupied"]

batch_size = 32
img_height = 150
img_width = 150

TF_MODEL_FILE_PATH = (
    "model.tflite"  # The default path to the saved TensorFlow Lite model
)

interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
signature_keys = interpreter.get_signature_list()
classify_lite = interpreter.get_signature_runner("serving_default")


# ==========================================#
# ============= Functions ==================#
# ==========================================#
# function to estimate if the spot is free or not
def estimateParkingSpot(img):
    global interpreter
    global classify_lite
    global class_names
    global img_height
    global img_width

    # change image opened with cv2 to PIL image
    color_converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(color_converted)

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions_lite = classify_lite(sequential_input=img_array)["dense_1"]
    score_lite = tf.nn.softmax(predictions_lite)

    return class_names[np.argmax(score_lite)], 100 * np.max(score_lite)


def cutImage(img, i):
    rect = rectangles[i]

    mask = np.zeros(img.shape[0:2], dtype=np.uint8)
    cv2.drawContours(mask, [rect], -1, (255, 255, 255), -1, cv2.LINE_AA)
    res = cv2.bitwise_and(img, img, mask=mask)
    spot = cv2.boundingRect(rect)

    cropped = res[spot[1] : spot[1] + spot[3], spot[0] : spot[0] + spot[2]]
    cropped = cv2.resize(cropped, (150, 150))
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    cropped[:, :, 2] = cv2.equalizeHist(cropped[:, :, 2])
    cropped = cv2.cvtColor(cropped, cv2.COLOR_HSV2BGR)
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    return cropped


# ==========================================#
# =============== Main =====================#
# ==========================================#
if __name__ == "__main__":
    img = cv2.imread(imgPath)
    predictions = []
    scores = []

    sys.stdout.write(
        "\n\nMake sure the following keys and values are inserted to the classify_lite() function (row 50):\n\r%s\n\n\r"
        % (signature_keys)
    )

    for i in range(0, len(rectangles)):
        spot = cutImage(img, i)
        prediction, score = estimateParkingSpot(spot)
        predictions.append(prediction)
        # round score to two decimals
        score = round(score, 2)
        scores.append(score)

    # print rectangles to image
    img2 = cv2.imread(imgPath)
    for i in range(0, len(rectangles)):
        rect = rectangles[i]
        if predictions[i] == "occupied":
            cv2.drawContours(img2, [rect], -1, (0, 0, 255), 3)
        else:
            cv2.drawContours(img2, [rect], -1, (0, 255, 0), 3)
        # show predicitons inside rectangles

        cv2.putText(
            img2,
            str(scores[i]) + "%",
            (rect[0][0], rect[0][1] + 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    # show image using cv2
    img2 = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("image", img2)
    cv2.waitKey(0)
