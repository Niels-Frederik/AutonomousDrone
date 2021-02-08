from mss import mss
from PIL import Image
import numpy as np
import time
import cv2

def showImage(name, image):
    cv2.imshow(name, image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        return

def loadImage(path):
    # Use os.path.join to make it work across all OS systems
    img = cv2.imread(path)
    return img


def loadVideo(path):
    video = cv2.VideoCapture(path)
    return video

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
    captureScreenLive()
