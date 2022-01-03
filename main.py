# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time

import mediapipe as mp
import cv2
import DynamicSignRec
import HandWriter
import _thread
import UdpComms as U

g_flag = False
g_text = ""
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)


def sever(delay):
    global g_flag, g_text
    # socket = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
    while True:
        # print("server", time.ctime(time.time()))
        data = sock.ReadReceivedData()
        if data != None:
            print("revice data", data)
            g_flag = True
            g_text = data.strip()
        time.sleep(delay)


def sendAns(data):
    sock.SendData(data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    _thread.start_new_thread(sever, (0.5,))
    wCam, hCam = 1280, 720
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)
    while True:
        # print("main", g_flag, g_text)
        if g_flag:
            if g_text != "handWrite":
                ans = DynamicSignRec.dynamicSignRecUtil(cap, wCam, hCam)

                if ans == g_text:
                    data = "True"
                else:
                    data = "False"
                print("receive", g_text, "rec result", ans)
                print("send data", data)
                sock.SendData(data)
            else:
                HandWriter.handWriteUtil(cap, wCam, hCam)
                sock.SendData("True")
                #假装都写对
            g_flag = False
        time.sleep(0.5)
    time.sleep(10)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
