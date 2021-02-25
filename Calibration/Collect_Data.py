import cv2
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname('../DepthEstimation/')))     
import VideoIO

path = './inputs/'
outPath = './outputs/'
video = VideoIO.loadVideo(path + 'IMG_0461.mp4')
i = 0

while video.isOpened():
    ret, image = video.read()

    fileName = ''
    foundAvailableName = False
    while not foundAvailableName:
        numberString = str(i)
        if i < 10:
            numberString = '0' + numberString
        fileName = 'Pattern_' + numberString + '.jpg'
        if os.path.exists(outPath + fileName):
            i += 1
        else:
            foundAvailableName = True

    cv2.imshow('name', image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite(outPath +fileName, image)
        i += 1
