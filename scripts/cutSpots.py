from PIL import Image, ImageDraw
import numpy as np
import cv2
import os
import sys
import glob

# ==========================================#
# ========== GLobal variables ==============#
# ==========================================#
rectangles = np.load("./rectangles.npy")

imgPath = "../original_images/to_be_cut/"
croppedPath = "../cropped/"
freePath = "../dataset/free/"
occupiedPath = "../dataset/occupied/"

imagesLabelledFile = "imagesLabelled.txt"

# ==========================================#
# ============== Functions =================#
# ==========================================#
def clear():
    with open(imagesLabelledFile, "w") as f:
        f.write("0")
        f.close()

    j = 0
    # get amount of files in directories
    freeAmount = len(glob.glob(freePath + "*.png"))
    occupiedAmount = len(glob.glob(occupiedPath + "*.png"))
    totalAmount = freeAmount + occupiedAmount

    # remove directories from teachDir
    for filename in os.listdir(freePath):
        os.remove(freePath + filename)
        j = j + 1
        progress = (100 / totalAmount) * j
        sys.stdout.flush()
        sys.stdout.write("Deleting old dataset files: %i %% \r" % (progress))

    for filename in os.listdir(occupiedPath):
        os.remove(occupiedPath + filename)
        j = j + 1
        progress = (100 / totalAmount) * j
        sys.stdout.flush()
        sys.stdout.write("Deleting old dataset files: %i %% \r" % (progress))

    sys.stdout.write("\n\r")


# ==========================================#
# ============== Main ======================#
# ==========================================#
if __name__ == "__main__":
    rectangles
    imgPath
    croppedPath

    imgAmount = len(glob.glob(imgPath + "*.png"))

    j = 0
    i = 0

    clear()

    for filename in os.listdir(imgPath):
        img = cv2.imread(imgPath + filename)

        for points in rectangles:
            i = i + 1
            mask = np.zeros(img.shape[0:2], dtype=np.uint8)
            cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
            res = cv2.bitwise_and(img, img, mask=mask)
            rect = cv2.boundingRect(points)  # returns (x,y,w,h) of the rect
            cropped = res[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]
            # save cropped to file
            # resize cropped image to 150x150
            cropped = cv2.resize(cropped, (150, 150))

            # image too blue, fix colors
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
            cropped[:, :, 2] = cv2.equalizeHist(cropped[:, :, 2])
            cropped = cv2.cvtColor(cropped, cv2.COLOR_HSV2BGR)
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            equ = cv2.equalizeHist(cropped)
            res = np.stack((equ,) * 3, axis=-1)

            cv2.imwrite(croppedPath + str(i) + ".png", cropped)

        j = j + 1

        progress = (100 / imgAmount) * j
        sys.stdout.write("cropping %i %% \r" % (progress))
    print("\nimages cropped!")
