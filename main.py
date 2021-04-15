import os
import sys
import cv2
import _thread
import time
import numpy as np


sys.path.insert(0, os.path.abspath(os.path.dirname('CollisionDetection/')))
sys.path.insert(0, os.path.abspath(os.path.dirname('Controller/')))
sys.path.insert(0, os.path.abspath(os.path.dirname('DepthEstimation/')))
sys.path.insert(0, os.path.abspath(os.path.dirname('RoutePlanner/')))
sys.path.insert(0, os.path.abspath(os.path.dirname('Calibration/')))
sys.path.insert(0, os.path.abspath(os.path.dirname('DepthEstimation/DenseDepth/')))

import CollisionDetector
import DroneController
import DepthEstimator
import RoutePlanner
import VideoIO
from Camera import Camera
from Connection import Connector
import PIL.Image as pil

class Main():
    def __init__(self, localTest, remoteTest, debug, videoPath = None):
        if videoPath != None:
            self.video = VideoIO.loadVideo(videoPath)
            _, frame = self.video.read()
            self.live = False
        else:
            self.live = True
            frame = VideoIO.captureScreen()
        self.localTest = localTest
        self.remoteTest = remoteTest
        self.debug = debug

        self.socket = getSocket(remoteTest)
        self.camera = Camera('./Calibration/outputs/', frame)
        #which method is used
        #depthEstimator
        #CollisionDetector
        #Visualizer
        self.frameNumber = 0

    def start(self):
        if self.live:
            self.runLive()
        else:
            self.runVideo()

    def runVideo(self):
        while True:
            _, frame = self.video.read()
            if self.frameNumber%60 == 0:
                self.handleFrame(frame)
            self.frameNumber += 1

    def runLive(self):
        while True:
            frame = VideoIO.captureScreen()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.frameNumber%60 == 0:
                self.handleFrame(frame)
            self.frameNumber += 1

    def handleFrame(self, frame):
        depthImage = DepthEstimator.estimateDepthImage(frame, self.debug)
        CollisionDetector.avoidCollisionsFromDepthImage(depthImage, self.debug)
        DroneController.control()
        self.visualizer(frame, depthImage)


    def visualizer(self, frame, processedFrame):
        #cv2.imshow('screen', frame)
        #cv2.imshow('processed', processedFrame)

        #frame = pil.fromarray(frame)
        #frame = frame.resize((640, 320), pil.LANCZOS)
        #frame = np.array(frame)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #stacked = np.hstack((frame, processedFrame[0]))
        stacked = processedFrame

        if self.remoteTest and self.socket != None:
            self.socket.sendMessage('test1', stacked)

        if self.localTest:
            cv2.imshow('stacked', stacked)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()

def getSocket(remoteTest):
    if remoteTest:
        try:
            return Connector('127.0.0.1', 15003)
            #return Connector('212.237.131.28', 15003)
            #return Connector('192.168.1.83', 15003)
        except:
            return None
    return None

if __name__ == '__main__':
    videoPath = 'Source/Video/droneVideo4.0.mp4'
    localTest = True
    remoteTest = False
    debug = True
    main = Main(localTest, remoteTest, debug, videoPath)
    main.start()
    #start(video, localTest, remoteTest, debug)
    #start('Source/Video/IndoorDrone.mp4', True)
    #start('Source/Video/IMG_0460.mp4', True)
    #start('Source/Video/IMG_0463.mp4', True, True)
    #start('Source/Video/droneVideo4.0.mp4', True)

