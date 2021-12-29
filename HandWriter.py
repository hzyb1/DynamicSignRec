import cv2
import HandTrackingModule as htm
import StaticSign
import numpy as np
import util


def handWrite():
    wCam, hCam = 1280, 720
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = htm.handDetector(detectionCon=0.75)

    drawColor = (0, 255, 0)
    eraserColor = (0, 0, 0)
    brushThickness = 15
    eraserThickness = 50
    xp, yp = 0, 0
    imgCanvas = np.zeros((hCam, wCam, 3), np.uint8)

    distanceThreshold = 40

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (wCam, hCam), cv2.INTER_CUBIC)

        img = detector.findHands(img)
        lmLists = detector.findPosition(img, draw=False)

        if len(lmLists) == 1:
            lmList = lmLists[0]
            x1, y1 = lmList[8][:2]
            x2, y2 = lmList[4][:2]
            x3, y3 = lmList[12][:2]

            if util.getDistance((x1, y1), (x2, y2)) < distanceThreshold:
                print("Drawing Mode")
                x1 = int((x1 + x2) / 2)
                y1 = int((y1 + y2) / 2)
                print((x1, y1))
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1
            elif StaticSign.isTow(lmLists) and util.getDistance((x1, y1), (x3, y3)) < distanceThreshold:
                x1 = int((x1 + x3) / 2)
                y1 = int((y1 + y3) / 2)
                print((x1, y1))
                cv2.circle(img, (x1, y1), 15, eraserColor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(img, (xp, yp), (x1, y1), eraserColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), eraserColor, eraserThickness)

                xp, yp = x1, y1
            else:
                xp, yp = 0, 0
            if StaticSign.isZero(lmLists):
                imgCanvas = np.zeros((hCam, wCam, 3), np.uint8)

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.imshow("Image", img)
        # cv2.imshow("Canvas", imgCanvas)
        idKey = cv2.waitKey(1)
        if idKey == 27:  # 27 为 ESC 键对应的 ASCII 码
            # 关闭所有窗口
            cv2.destroyAllWindows()
            break


def handWriteUtil(cap, wCam, hCam):
    detector = htm.handDetector(detectionCon=0.75)

    drawColor = (0, 255, 0)
    eraserColor = (0, 0, 0)
    brushThickness = 15
    eraserThickness = 50
    xp, yp = 0, 0
    imgCanvas = np.zeros((hCam, wCam, 3), np.uint8)

    distanceThreshold = 40

    count_without_hand = 0
    count_without_hand_threshold = 30
    begin_write = False

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (wCam, hCam), cv2.INTER_CUBIC)

        img = detector.findHands(img)
        lmLists = detector.findPosition(img, draw=False)

        if len(lmLists) == 1:
            begin_write = True
            count_without_hand = 0

            lmList = lmLists[0]
            x1, y1 = lmList[8][:2]
            x2, y2 = lmList[4][:2]
            x3, y3 = lmList[12][:2]

            if util.getDistance((x1, y1), (x2, y2)) < distanceThreshold:
                print("Drawing Mode")
                x1 = int((x1 + x2) / 2)
                y1 = int((y1 + y2) / 2)
                print((x1, y1))
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1
            elif StaticSign.isTow(lmLists) and util.getDistance((x1, y1), (x3, y3)) < distanceThreshold:
                x1 = int((x1 + x3) / 2)
                y1 = int((y1 + y3) / 2)
                print((x1, y1))
                cv2.circle(img, (x1, y1), 15, eraserColor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(img, (xp, yp), (x1, y1), eraserColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), eraserColor, eraserThickness)

                xp, yp = x1, y1
            else:
                xp, yp = 0, 0
            if StaticSign.isZero(lmLists):
                imgCanvas = np.zeros((hCam, wCam, 3), np.uint8)
        elif len(lmLists) == 0:
            count_without_hand = count_without_hand+1
            if begin_write and count_without_hand > count_without_hand_threshold:
                break

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.imshow("Image", img)
        # cv2.imshow("Canvas", imgCanvas)
        idKey = cv2.waitKey(1)
        if idKey == 27:  # 27 为 ESC 键对应的 ASCII 码
            # 关闭所有窗口
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    handWrite()
