#from CollisionDetection import Test123
import CollisionHelper
import cv2

def avoidCollisionsFromDepthImage(frame, test):
    print('hello from collisionDetection')
    #Make it look for brightest zones instead of pixel
    downScaledFrame = cv2.resize(frame, (int(frame.shape[1]/16), int(frame.shape[0]/16)))
    return CollisionHelper.findSafestDirection(downScaledFrame, frame, test)

if __name__ == '__main__':
    print('this code is only run if this is called as the main')
    detectCollisions()
