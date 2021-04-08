from mss import mss
from PIL import Image
import numpy as np
import time
import cv2

import sys
import os


def showImage(name, image):
    cv2.imshow(name, image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        return

def loadImage(path):
    # Use os.path.join to make it work across all OS systems
    img = cv2.imread(path)
    return img

def saveImage(image):
    image = cv2.resize(image, (1280, 1024), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('vignette.jpg', image)


def loadVideo(path):
    video = cv2.VideoCapture(path)
    return video

def saveEachImageInVideo(video, savePath, name):
    camera = None
    i = 0
    while(True):
        try:
            _, image = video.read()
            #image = cv2.resize(image, (1280,1024), interpolation=cv2.INTER_CUBIC)
            image = cv2.resize(image, (1920,1080), interpolation=cv2.INTER_CUBIC)
            #image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            if camera == None:
                camera = Camera('../../Calibration/outputs/', image)
            #image = camera.undistort(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image = cv2.resize(image, (1280,1024), interpolation=cv2.INTER_CUBIC)
            #cv2.imwrite(name + savePath + str(i) + '.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
            #cv2.imwrite(name + str(i) + '.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
            #cv2.imwrite(str(i) + '.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
            cv2.imwrite(str(i).zfill(5) + '.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
            i += 1
        except:
            break
    video.release()

def showVideo(video):
    raise NotImplementedError

def mss_record(width, height, startX, startY):
    with mss() as sct:
        monitor = {'top': startY, 'left': startX, 'width': width, 'height': height}
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def captureScreen(width = 1300, height = 600, startX = 0, startY = 0):
    frame = mss_record(width, height, startX, startY)
    frame = np.array(frame)
    return frame

def captureScreenLive():
    while True:
        frame = captureScreen()
        cv2.imshow('screen', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.dirname('../../Calibration/')))
    sys.path.insert(0, os.path.abspath(os.path.dirname('../Calibration/')))
    from Camera import Camera
    #captureScreenLive()
    #video = loadVideo('/home/yarl/Downloads/video-1617541377.mp4')
    #video = loadVideo('../../Source/Video/IMG_0460.mp4')
    #video = loadVideo('/home/yarl/Downloads/IMG_0490.mp4')
    #video = loadVideo('/home/yarl/Downloads/droneVideo3.0.mp4')
    video = loadVideo('/home/yarl/Downloads/droneVideo4.0.mp4')
    #image = loadImage('/home/yarl/Downloads/vignette2.jpg')
    #saveImage(image)
    #video = loadVideo('../../Source/Video/IMG_0463.mp4')
    saveEachImageInVideo(video, './', 'droneVideo')
