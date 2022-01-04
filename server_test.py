import time
import unittest
import UdpComms as U
import sys
import _thread

sock = U.UdpComms(udpIP="127.0.0.1", portTX=8001, portRX=8000, enableRX=True, suppressWarnings=True)


def test_something():
    print("a")
    while True:
        line = sys.stdin.readline()
        print("send data", line)
        sock.SendData(line)
        time.sleep(0.5)


def test_revice():
    print("revice")
    while True:
        data = sock.ReadReceivedData()
        if data != None:
            print("revice", data)
        time.sleep(0.5)


if __name__ == '__main__':
    _thread.start_new_thread(test_something, ())
    _thread.start_new_thread(test_revice, ())
    while True:

        data = sock.ReadReceivedData()
        if data != None:
            print("revice", data)
        time.sleep(0.5)
    time.sleep(1000)
