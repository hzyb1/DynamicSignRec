import cv2
import os
import time
import HandTrackingModule as htm
from DynamicSign import HelloSign
import StaticSign

isJudgeMotivate = False

helloSign = HelloSign()

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionCon=0.70)
tipIds = [4, 8, 12, 16, 20]
i = 0



text = ""
while True:
    i = (i + 1) % 5
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmLists = detector.findPosition(img)
    # print(lmList)
    if len(lmLists) != 0:
        if not isJudgeMotivate:
            if helloSign.isStaticHello(lmLists):
                helloSign.lastWrists[0] = lmLists[0][0]
                helloSign.lastWrists[1] = lmLists[1][0]
                isJudgeMotivate = True
            elif StaticSign.isZero(lmLists):
                text = "0"
            elif StaticSign.isOne(lmLists):
                text = "1"
            elif StaticSign.isTow(lmLists):
                text = "2"
            elif StaticSign.isThree(lmLists):
                text = "3"
            elif StaticSign.isFour(lmLists):
                text = "4"
            elif StaticSign.isFive(lmLists):
                text = "5"
            else:
                text = ""

        elif i%5==0:
            res = helloSign.isHello(lmLists)
            if res == "break":
                isJudgeMotivate = False
                text = ""
                # helloSign = HelloSign()
            elif res == "hello":
                text = "hello"

    # cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, text, (45, 375), cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 25)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

