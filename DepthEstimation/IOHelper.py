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
    raise NotImplementedError


def loadVideo(path):
    raise NotImplementedError

def showVideo(video):
    raise NotImplementedError

def mss_record():
    with mss() as sct:
        monitor = {'top': 0, 'left': 0, 'width': 1300, 'height': 600}
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def captureScreen():
    frame = mss_record()
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
