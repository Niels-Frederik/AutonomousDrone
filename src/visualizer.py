import cv2
import numpy as np

class Visualizer():
    def __init__(self, localTest, remoteTest, socket):
        self.localTest = localTest
        self.remoteTest = remoteTest
        self.socket = socket

    def visualize(self, frame, processedFrame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.resize(frame, ((320, 240)))
        stacked = np.hstack((frame/255, processedFrame))

        if self.remoteTest:
            self.remoteVisualize(stacked)

        if self.localTest:
            self.localVisualize(stacked)

    def remoteVisualize(self, image):
        if self.socket != None:
            self.socket.sendMessage('test1', image)

    def localVisualize(self, image):
        cv2.imshow('stacked', image)
        cv2.waitKey(1)
