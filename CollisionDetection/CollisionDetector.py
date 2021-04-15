#from CollisionDetection import Test123
import CollisionHelper
import cv2

def avoidCollisionsFromDepthImage(frame, debug):
    print('hello from collisionDetection')
    scaleFactor = 32
    downScaledFrame = cv2.resize(frame, (int(frame.shape[1]/scaleFactor), int(frame.shape[0]/scaleFactor)))
    return CollisionHelper.findSafestDirection(downScaledFrame, frame, scaleFactor, debug)

if __name__ == '__main__':
    print('this code is only run if this is called as the main')
    detectCollisions()
