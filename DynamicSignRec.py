import cv2
import time
import JudgeSign
import HandTrackingModule as htm


# 算法描述：
# 以识别到手为开始，连续5帧没有识别到手为结束，界定所需要识别的帧的范围
# 获取到需要识别的帧的集合后，去除掉前5帧和后五帧，提取出对这些帧中的手坐标，通过坐标集合进行手势识别

def dynamicSignRec():
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)
    pTime = 0
    detector = htm.handDetector(detectionCon=0.70)
    i = 0

    postions = []

    # 判断是否开始识别手势，判断方式：以识别到手为开始，以连续5帧没有识别到手为结束
    isBegin = False
    noHandsCount = 0
    noHandsCountThreshold = 5
    print(cap.set(3, 10))
    print(cap.get(3))
    print(cap.get(4))
    text = ""

    while True:
        i = (i + 1) % 5
        success, img = cap.read()
        img = cv2.resize(img, (wCam, hCam), cv2.INTER_CUBIC)
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmLists = detector.findPosition(img)
        # print(lmList)
        if isBegin:
            postions.append(lmLists)
            if len(lmLists) == 0:
                noHandsCount = noHandsCount + 1
                if noHandsCount >= noHandsCountThreshold:
                    isBegin = False
                    if len(postions) > 10:
                        text = JudgeSign.judgeSign(postions[5:len(postions) - 5])
        else:
            if len(lmLists) != 0:
                isBegin = True
                postions = []
                postions.append(lmLists)

        # cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, text, (45, 375), cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 25)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    dynamicSignRec()
