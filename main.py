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

import CollisionDetector
import DroneController
import DepthEstimator
import RoutePlanner
import VideoIO
from GUI import GUI

#gui = GUI()

def start(path = None, test = False):
    #if test:
        #_thread.start_new_thread(gui.setup, ())
    if path != None:
        video = VideoIO.loadVideo(path)
        ret1, frame1 = video.read()
        while video.isOpened():
            ret2, frame2 = video.read()
            mainLoop(frame1, frame2, test)
            ret1 = ret2
            frame1 = frame2
    else:
        frame1 = VideoIO.captureScreen()
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        while True:
            frame2 = VideoIO.captureScreen()
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            mainLoop(frame1, frame2, test)
            frame1 = frame2

def mainLoop(frame1, frame2, test = False):
    depthImage = DepthEstimator.estimateDepth(frame1, frame2, test)
    CollisionDetector.detectCollisions(depthImage)
    RoutePlanner.planRoute()
    DroneController.control()
    if test:
        visualizer(frame2, depthImage)

    

def visualizer(frame, processedFrame):
    #Update the values of the frontend
    #cv2.imshow('screen', frame)
    #cv2.imshow('processed', processedFrame)
    stacked = np.hstack((frame, processedFrame))
    cv2.imshow('stacked', stacked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit()

    #gui.updateImages(frame, processedFrame)

if __name__ == '__main__':
    print('hello from main')
    start('Source/Video/IndoorDrone.mp4', True)
    #start(test = True)

