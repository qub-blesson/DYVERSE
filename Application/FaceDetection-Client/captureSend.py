"""Webcam video streaming
Using OpenCV to capture frames from webcam.
Compress each frame to jpeg and save it.
Using socket to read from the jpg and send
it to remote address.
"""

import cv2
from socket import *
import time

cap = cv2.VideoCapture(0)

FPS = cap.get(5)
setFPS = 1      # Change this for load testing
ratio = int(FPS)/setFPS

host = "90.211.228.235" # Change this to the server IP
port = 4096
addr = (host, port)
buf = 4096

def sendFile(fName):
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(fName, addr)
    f = open(fName, "rb")
    data = f.read(buf)
    while data:
       if(s.sendto(data, addr)):
           data = f.read(buf)
           time.sleep(0.03) # Give receiver time to save. Larger data requires longer.
    f.close()
    s.close()
    print "Image sent."

def captureFunc():
    count = 0
    print "FPS:", setFPS
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            count = count + 1
            if count == ratio:
                print "Start time: ", time.time()
                cv2.imwrite("img.jpg", frame)
                sendFile("img.jpg")
                count = 0

if __name__ == '__main__':
    captureFunc()
    cap.release()
