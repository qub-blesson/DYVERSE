# Face Detection (FD) Client
This is the webcam video streaming client of the face detection application. It captures frames in real time and send them to the remote server for analysis.

## Tested Platform
We have tested FD Client with macOS High Sierra version 10.13.6

## Requirement
- [Python](https://www.python.org/)
- [OpenCV](https://opencv.org/)

## How to use
1. Update *host* in captureSend.py
2. Update *setFPS* (frames per second) for load testing
3. ```python captureSend.py```
