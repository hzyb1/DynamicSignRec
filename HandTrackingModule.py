import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lmLists = []
        flag = False
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([cx, cy, lm.z])
                lmLists.append(lmList)
        if self.results.multi_handedness:
            for hand_label in self.results.multi_handedness:
                if hand_label.classification[0].label == "Right":
                    flag = True
                break
                print(hand_label.classification[0].label)
        if flag and len(lmLists) == 2:
            tmp = lmLists[0]
            lmLists[0] = lmLists[1]
            lmLists[1] = tmp
        return lmLists


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector(detectionCon=0.75)
    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmLists = detector.findPosition(img)
        if len(lmLists) != 0:
            print(lmLists[0][5][2], lmLists[0][6][2], lmLists[0][7][2], lmLists[0][8][2])
            print(lmLists[0][5][1], lmLists[0][6][1], lmLists[0][7][1], lmLists[0][8][1])
            print(lmLists[0][5][0], lmLists[0][6][0], lmLists[0][7][0], lmLists[0][8][0])

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
