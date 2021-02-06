import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname('CollisionDetection/')))
sys.path.insert(0, os.path.abspath(os.path.dirname('Controller/'))) 
sys.path.insert(0, os.path.abspath(os.path.dirname('DepthEstimation/'))) 
sys.path.insert(0, os.path.abspath(os.path.dirname('RoutePlanner/'))) 

import CollisionDetector
import DroneController
import DepthEstimator
import RoutePlanner

if __name__ == '__main__':
    print('hello from main')
    DepthEstimator.estimateDepth()
    CollisionDetector.detectCollisions()
    RoutePlanner.planRoute()
    DroneController.control()

