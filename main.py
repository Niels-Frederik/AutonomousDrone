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


def start(path = None, localTest = False, remoteTest = False):
    socket = getSocket(remoteTest)
    if path != None:
        runFromVideo(path, socket, localTest, remoteTest)
    else:
        runLive(socket, localTest, remoteTest)

def runFromVideo(path, socket, localTest, remoteTest):
    video = VideoIO.loadVideo(path)
    ret, frame = video.read()
    camera = Camera('./Calibration/outputs/', frame)
    print(camera.cameraMatrix)
    while video.isOpened():
        ret, frame = video.read()
        #frame = camera.undistort(frame)
        mainLoop(camera, frame, socket, localTest, remoteTest)


def runLive(socket, localTest, remoteTest):
    frame = VideoIO.captureScreen()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    camera = Camera('./Calibration/outputs/', frame)
    while True:
        frame = VideoIO.captureScreen()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = camera.undistort(frame)
        mainLoop(camera, frame, socket, localTest, remoteTest)

i = 0
def mainLoop(camera, frame, socket, test, remoteTest):
    testMode = test or remoteTest
    global i
    if i%60 == 0:
        depthImage = DepthEstimator.estimateDepthImage(frame, testMode)
        CollisionDetector.avoidCollisionsFromDepthImage(depthImage, testMode)
        #RoutePlanner.planRoute()
        DroneController.control()

        visualizer(frame, depthImage, socket, test)
    i += 1



def visualizer(frame, processedFrame, socket, test):
    #Update the values of the frontend
    #cv2.imshow('screen', frame)
    #cv2.imshow('processed', processedFrame)

    #frame = pil.fromarray(frame)
    #frame = frame.resize((640, 320), pil.LANCZOS)
    #frame = np.array(frame)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #stacked = np.hstack((frame, processedFrame[0]))
    stacked = processedFrame

    if socket != None:
        socket.sendMessage('test1', stacked)

    if test:
        cv2.imshow('stacked', stacked)
        #cv2.imshow('a', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()

    #gui.updateImages(frame, processedFrame)

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
    print('hello from main')
    #start('Source/Video/IndoorDrone.mp4', True)
    #start('Source/Video/IMG_0460.mp4', True)
    #start('Source/Video/IMG_0463.mp4', True, True)
    start('Source/Video/droneVideo4.0.mp4', True)
    #start(test = True)

