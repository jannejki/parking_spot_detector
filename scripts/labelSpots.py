import cv2
import numpy as np
import os
import glob
import time

# ==========================================#
# ========== GLobal variables ==============#
# ==========================================#
croppedPath = "../cropped/"
freePath = "../dataset/occupied/"
occupiedPath = "../dataset/free/"

imagesLabelledFile = "imagesLabelled.txt"
lastWrittenPath = ""
# ==========================================#
# ============== Main ======================#
# ==========================================#
if __name__ == "__main__":
    with open(imagesLabelledFile, "r") as f:
        imagesLabelled = f.read()
        imagesLabelled = int(imagesLabelled)
        f.close()

    i = imagesLabelled
    while i < len(glob.glob(croppedPath + "*.png")):
        i = i + 1
        print(i)
        img = cv2.imread(croppedPath + str(i) + ".png")
        with open(imagesLabelledFile, "w") as f:
            f.write(str(i))
            f.close()

        # double the size of the image
        img = cv2.resize(img, (0, 0), fx=2, fy=2)

        cv2.imshow("image", img)

        key = cv2.waitKey(0)

        # =================#
        # ===== Keys ======#
        # =================#

        # ESC
        if key == 27:
            cv2.destroyAllWindows()
            break

        # K
        elif key == ord("k"):
            cv2.imwrite(freePath + str(i) + ".png", img)
            lastWrittenPath = freePath + str(i) + ".png"

        # J
        elif key == ord("j"):
            cv2.imwrite(occupiedPath + str(i) + ".png", img)
            lastWrittenPath = occupiedPath + str(i) + ".png"

        # backspace
        elif key == 8:
            i = i - 2
            os.remove(lastWrittenPath)
            print("Removed last written image: " + lastWrittenPath)
