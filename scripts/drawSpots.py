import cv2
import numpy as np
import math


# ==========================================#
# ========== GLobal variables ==============#
# ==========================================#
imagePath = "../practice/kuva47.png"
rectanglesPath = "./rectangles4.npy"

tempRect = np.empty((0, 2), int)
rectangle = np.empty((0, 2), int)
rectangles = np.empty((0, 4, 2), int)

img = cv2.imread(imagePath)

# ==========================================#
# ============ Functions ===================#
# ==========================================#
def draw_rectangle(event, x, y, flags, param):
    global rectangle
    global tempRect
    global rectangles
    global img

    if event == cv2.EVENT_LBUTTONDOWN:
        tempRect = np.append(tempRect, [[x, y]], axis=0)

        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        if len(tempRect) == 2:
            topLeft = [tempRect[0][0], tempRect[0][1]]
            topRight = [tempRect[1][0], tempRect[0][1]]
            bottomRight = [tempRect[1][0], tempRect[1][1]]
            bottomLeft = [tempRect[0][0], tempRect[1][1]]

            rectangle = np.append(rectangle, [topLeft], axis=0)
            rectangle = np.append(rectangle, [topRight], axis=0)
            rectangle = np.append(rectangle, [bottomRight], axis=0)
            rectangle = np.append(rectangle, [bottomLeft], axis=0)

            cv2.rectangle(
                img,
                (rectangle[0][0], rectangle[0][1]),
                (rectangle[2][0], rectangle[2][1]),
                (0, 255, 0),
                2,
            )

            tempRect = np.empty((0, 2), int)


def calcNewEndPoints(startPoint, oldEndPoint, angle):
    angle = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotate line
    newX = int(
        (cos * (oldEndPoint[0] - startPoint[0]))
        - (sin * (oldEndPoint[1] - startPoint[1]))
        + startPoint[0]
    )
    newY = int(
        (sin * (oldEndPoint[0] - startPoint[0]))
        + (cos * (oldEndPoint[1] - startPoint[1]))
        + startPoint[1]
    )

    return (newX, newY)


# ==========================================#
# ============== Main ======================#
# ==========================================#
if __name__ == "__main__":
    tempRect
    rectangle
    rectangles
    rectanglesPath
    imagePath
    img

    # open image
    img = cv2.imread(imagePath)

    # show image and wait for ESC key
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", draw_rectangle)

    # let user draw rectangles
    while True:
        # scale image to fit screen
        cv2.imshow("image", img)
        # draw rectangles in red
        for i in range(0, len(rectangles)):
            cv2.line(img, (rectangles[i][0]), rectangles[i][1], (0, 0, 255), 2)
            cv2.line(img, (rectangles[i][1]), rectangles[i][2], (0, 0, 255), 2)
            cv2.line(img, (rectangles[i][2]), rectangles[i][3], (0, 0, 255), 2)
            cv2.line(img, (rectangles[i][3]), rectangles[i][0], (0, 0, 255), 2)

        key = cv2.waitKey(20)

        # =================#
        # ===== Keys ======#
        # =================#
        # ESC
        if key == 27:
            # save rectangles to .npy file
            np.save(rectanglesPath, rectangles)
            # get rectangles from .npy file
            print(rectangles[0])
            loadedRectangles = np.load(rectanglesPath)
            print(loadedRectangles[0])
            print("saved: ")
            print(len(loadedRectangles))
            print(" rectangles")
            break

        # Enter
        elif key == 13:
            rectangles = np.append(rectangles, [rectangle], axis=0)
            rectangle = np.empty((0, 2), int)

            # clear image of drawn rectangles
            img = cv2.imread(imagePath)

        # J
        elif key == 106:
            # rotate only rectangle coordinates
            if len(rectangle) == 4:
                angle = 5

                topLeft = rectangle[0]
                topRight = rectangle[1]
                bottomRight = rectangle[2]
                bottomLeft = rectangle[3]

                # rotate from center point
                centerPoint = (
                    int((topLeft[0] + bottomRight[0]) / 2),
                    int((topLeft[1] + bottomRight[1]) / 2),
                )

                # rotate top line
                topRight = calcNewEndPoints(centerPoint, topRight, angle)
                topLeft = calcNewEndPoints(centerPoint, topLeft, angle)

                # rotate bottom line
                bottomRight = calcNewEndPoints(centerPoint, bottomRight, angle)
                bottomLeft = calcNewEndPoints(centerPoint, bottomLeft, angle)

                rectangle[0] = topLeft
                rectangle[1] = topRight
                rectangle[2] = bottomRight
                rectangle[3] = bottomLeft

                img = cv2.imread(imagePath)
                cv2.line(img, topLeft, topRight, (0, 0, 255), 2)
                cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(img, bottomRight, bottomLeft, (255, 0, 0), 2)
                cv2.line(img, bottomLeft, topLeft, (255, 255, 255), 2)

        # K
        elif key == 107:
            # rotate rectangle right 5 degrees
            if len(rectangle) == 4:
                angle = -5

                topLeft = rectangle[0]
                topRight = rectangle[1]
                bottomRight = rectangle[2]
                bottomLeft = rectangle[3]

                # rotate from center point
                centerPoint = (
                    int((topLeft[0] + bottomRight[0]) / 2),
                    int((topLeft[1] + bottomRight[1]) / 2),
                )

                # rotate top line
                topRight = calcNewEndPoints(centerPoint, topRight, angle)
                topLeft = calcNewEndPoints(centerPoint, topLeft, angle)

                # rotate bottom line
                bottomRight = calcNewEndPoints(centerPoint, bottomRight, angle)
                bottomLeft = calcNewEndPoints(centerPoint, bottomLeft, angle)

                rectangle[0] = topLeft
                rectangle[1] = topRight
                rectangle[2] = bottomRight
                rectangle[3] = bottomLeft

                img = cv2.imread(imagePath)
                cv2.line(img, topLeft, topRight, (0, 0, 255), 2)
                cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(img, bottomRight, bottomLeft, (255, 0, 0), 2)
                cv2.line(img, bottomLeft, topLeft, (255, 255, 255), 2)

        # A
        elif key == 97:
            # move rectangle left
            if len(rectangle) == 4:
                for i in range(0, len(rectangle)):
                    rectangle[i] = (rectangle[i][0] - 1, rectangle[i][1])

                img = cv2.imread(imagePath)
                cv2.line(img, rectangle[0], rectangle[1], (0, 0, 255), 2)
                cv2.line(img, rectangle[1], rectangle[2], (0, 255, 0), 2)
                cv2.line(img, rectangle[2], rectangle[3], (255, 0, 0), 2)
                cv2.line(img, rectangle[3], rectangle[0], (255, 255, 255), 2)

        # D
        elif key == 100:
            # move rectangle right
            if len(rectangle) == 4:
                for i in range(0, len(rectangle)):
                    rectangle[i] = (rectangle[i][0] + 1, rectangle[i][1])

                img = cv2.imread(imagePath)
                cv2.line(img, rectangle[0], rectangle[1], (0, 0, 255), 2)
                cv2.line(img, rectangle[1], rectangle[2], (0, 255, 0), 2)
                cv2.line(img, rectangle[2], rectangle[3], (255, 0, 0), 2)
                cv2.line(img, rectangle[3], rectangle[0], (255, 255, 255), 2)

        # W
        elif key == 119:
            # move rectangle up
            if len(rectangle) == 4:
                for i in range(0, len(rectangle)):
                    rectangle[i] = (rectangle[i][0], rectangle[i][1] - 1)

                img = cv2.imread(imagePath)
                cv2.line(img, rectangle[0], rectangle[1], (0, 0, 255), 2)
                cv2.line(img, rectangle[1], rectangle[2], (0, 255, 0), 2)
                cv2.line(img, rectangle[2], rectangle[3], (255, 0, 0), 2)
                cv2.line(img, rectangle[3], rectangle[0], (255, 255, 255), 2)

        # S
        elif key == 115:
            # move rectangle down
            if len(rectangle) == 4:
                for i in range(0, len(rectangle)):
                    rectangle[i] = (rectangle[i][0], rectangle[i][1] + 1)

                img = cv2.imread(imagePath)
                cv2.line(img, rectangle[0], rectangle[1], (0, 0, 255), 2)
                cv2.line(img, rectangle[1], rectangle[2], (0, 255, 0), 2)
                cv2.line(img, rectangle[2], rectangle[3], (255, 0, 0), 2)
                cv2.line(img, rectangle[3], rectangle[0], (255, 255, 255), 2)

            # backspace
        elif key == 8:
            # clear rectangle
            tempRect = np.empty((0, 2), int)
            rotatedAngle = 0
            # array to hold four corners of rectangle
            rectangle = np.empty((0, 2), int)
            img = cv2.imread(imagePath)
