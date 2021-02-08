import os
import sys
import cv2
sys.path.insert(0, os.path.abspath(os.path.dirname('CollisionDetection/')))
sys.path.insert(0, os.path.abspath(os.path.dirname('Controller/'))) 
sys.path.insert(0, os.path.abspath(os.path.dirname('DepthEstimation/'))) 
sys.path.insert(0, os.path.abspath(os.path.dirname('RoutePlanner/'))) 

import CollisionDetector
import DroneController
import DepthEstimator
import RoutePlanner
import VideoIO



def start(path = None, test = False):
    if path != None:
        video = VideoIO.loadVideo(path)
        while video.isOpened():
            ret, frame = video.read()
            mainLoop(frame, test)
    else:
        while True:
            frame = VideoIO.captureScreen()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mainLoop(frame, test)

def mainLoop(frame, test = False):
    depthImage = DepthEstimator.estimateDepth(frame)
    CollisionDetector.detectCollisions(depthImage)
    RoutePlanner.planRoute()
    DroneController.control()
    if test:
        visualizer(frame, None)

    

def visualizer(frame, newFrame):
    cv2.imshow('screen', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()













if __name__ == '__main__':
    print('hello from main')
    frame = VideoIO.captureScreen()
    start('Source/Video/IndoorDrone.mp4', True)
    #start(test = True)

