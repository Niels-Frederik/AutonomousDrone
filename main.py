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

import CollisionDetector
import DroneController
import DepthEstimator
import RoutePlanner
import VideoIO
from Camera import Camera
from Connection import Connector

#gui = GUI()

def start(path = None, localTest = False, remoteTest = False):
    socket = None
    if remoteTest:
        try:
            socket = handShake()
        except:
            socket = None
    if path != None:
        video = VideoIO.loadVideo(path)
        ret1, frame1 = video.read()
        camera = Camera('./Calibration/outputs/', frame1)
        while video.isOpened():
            ret2, frame2 = video.read()
            frame2 = camera.undistort(frame2)
            mainLoop(camera, frame1, frame2, socket, localTest, remoteTest)
            ret1 = ret2
            frame1 = frame2
    else:
        frame1 = VideoIO.captureScreen()
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        camera = Camera('./Calibration/outputs/', frame1)
        while True:
            frame2 = VideoIO.captureScreen()
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            frame2 = camera.undistort(frame2)
            mainLoop(camera, frame1, frame2, socket, localTest, remoteTest)
            frame1 = frame2

def mainLoop(camera, frame1, frame2, socket, test, remoteTest):
    depthImage = DepthEstimator.estimateDepth(frame1, frame2, test or remoteTest)
    #depthImage = frame2
    CollisionDetector.detectCollisions(depthImage)
    RoutePlanner.planRoute()
    DroneController.control()

    visualizer(frame2, depthImage, socket, test)
        #if socket != None:
            #socket.sendMessage('test1', frame1)

    

def visualizer(frame, processedFrame, socket, test):
    #Update the values of the frontend
    #cv2.imshow('screen', frame)
    #cv2.imshow('processed', processedFrame)
    stacked = np.hstack((frame, processedFrame))

    if socket != None:
        socket.sendMessage('test1', stacked)

    if test:
        cv2.imshow('stacked', stacked)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()

    #gui.updateImages(frame, processedFrame)

def handShake():
    #return Connector('212.237.131.28', 15003)
    #return Connector('192.168.1.83', 15003)
    return Connector('127.0.0.1', 15003)

if __name__ == '__main__':
    print('hello from main')
    #start('Source/Video/IndoorDrone.mp4', True)
    #start('Source/Video/IMG_0460.mp4', True)
    start('Source/Video/IMG_0463.mp4', False, True)
    #start(test = True)

