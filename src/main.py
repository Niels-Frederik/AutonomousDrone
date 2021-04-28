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
sys.path.insert(0, os.path.abspath(os.path.dirname('DepthEstimation/PyDNet/')))

from collisionAvoider import CollisionAvoider
from collisionAvoiderDepthImage import CollisionAvoiderDepthImage
from depthEstimator import DepthEstimator
from depthEstimatorDenseDepth import DepthEstimatorDenseDepth
from depthEstimatorPydnet import DepthEstimatorPydnet
from droneController import DroneController
from controller import Controller
from visualizer import Visualizer
import depthEstimator
import RoutePlanner
import VideoIO
from Camera import Camera
from Connection import Connector
import PIL.Image as pil

class Main():
    def __init__(self, localTest, remoteTest, debug, videoPath = None, mode = 0):
        self.localTest = localTest
        self.remoteTest = remoteTest
        self.debug = debug
        self.frameNumber = 0

        self.initializeVideo(videoPath)
        self.socket = getSocket(remoteTest)
        self.visualizer = Visualizer(localTest, remoteTest, self.socket)
        self.initializeHelpers(mode)

    def initializeVideo(self, videoPath):
        if videoPath != None:
            self.video = VideoIO.loadVideo(videoPath)
            self.live = False
        else:
            self.live = True

    def initializeHelpers(self, mode):
        if self.live:
            self.droneController = DroneController(self.debug)
            frame = self.droneController.getNewImage()
            #frame = VideoIO.captureScreen()
        else:
            self.droneController = Controller(self.debug)
            _, frame = self.video.read()
        self.camera = Camera('./Calibration/outputs/', frame)

        #check mode - 0=feature, 1=densedepth, 2=pydnet
        if mode == 0:
            self.depthEstimator = DepthEstimator(self.debug)
            self.collisionAvoider = CollisionAvoider(self.droneController, self.debug)
            #Visualizer
        elif mode == 1:
            self.depthEstimator = DepthEstimatorDenseDepth(self.debug)
            depthImage = self.depthEstimator.estimateDepth(frame)
            self.collisionAvoider = CollisionAvoiderDepthImage(depthImage, self.droneController, self.debug)
            #Visualizer
        elif mode == 2:
            self.depthEstimator = DepthEstimatorPydnet(self.debug)
            depthImage = self.depthEstimator.estimateDepth(frame)
            self.collisionAvoider = CollisionAvoiderDepthImage(depthImage, self.droneController, self.debug)

    def start(self):
        if self.live:
            self.droneController.takeoff()
            self.runLive()
        else:
            self.runVideo()

    def runVideo(self):
        while True:
            _, frame = self.video.read()
            self.handleFrame(frame)
            #if self.frameNumber%60 == 0:
                #self.handleFrame(frame)
            #self.frameNumber += 1

    def runLive(self):
        while True:
            #frame = VideoIO.captureScreen()
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.droneController.getNewImage()
            #if self.frameNumber%60 == 0:
                #self.handleFrame(frame)
            #self.frameNumber += 1
            self.handleFrame(frame)

    def handleFrame(self, frame):
        depthImage = self.depthEstimator.estimateDepth(frame)
        self.collisionAvoider.avoidCollisions(depthImage)
        self.visualizer.visualize(frame, depthImage)

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
    #videoPath = '../Source/Video/droneVideo4.0.mp4'
    videoPath = '../Source/Video/ipadVideo.mp4'
    localTest = True
    remoteTest = False
    debug = True
    #main = Main(localTest, remoteTest, debug, mode=2)
    main = Main(localTest, remoteTest, debug, videoPath, mode=2)
    main.start()
    #start(video, localTest, remoteTest, debug)

