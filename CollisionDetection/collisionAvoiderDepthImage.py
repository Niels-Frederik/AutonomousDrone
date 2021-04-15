import cv2
from collisionAvoider import CollisionAvoider

class CollisionAvoiderDepthImage(CollisionAvoider):
    def __init__(self, frame, debug):
        self.scaleFactor = 32
        self.threshold = 0.25
        self.shift = int(self.scaleFactor/2)
        self.height = int(frame.shape[0]/self.scaleFactor)
        self.width = int(frame.shape[1]/self.scaleFactor)
        self.debug = debug
        if debug:
            self.originalWidth = self.width*self.scaleFactor
            self.originalHeight = self.height*self.scaleFactor
            downScaledShift = self.shift/self.scaleFactor
            self.upperXBound = self.width/2 + self.width*0.1 - downScaledShift
            self.lowerXBound = self.width/2 - self.width*0.1 - downScaledShift
            self.upperYBound = self.height/2 + self.height*0.1 - downScaledShift
            self.lowerYBound = self.height/2 - self.height*0.1 - downScaledShift

    def avoidCollisions(self, frame):
        downScaledFrame = cv2.resize(frame, (self.width, self.height))
        return self.findSafestDirection(downScaledFrame, self.scaleFactor)

    def findSafestDirection(self, frame, scaleFactor):
        maxValue = 0
        if self.debug: frameOriginSized = cv2.resize(frame, (self.originalWidth, self.originalHeight))

        for i in range(2, self.height-2):
            for j in range(1, self.width-1):
                if self.debug: cv2.circle(frameOriginSized, (j*self.scaleFactor + self.shift, i*self.scaleFactor + self.shift), 8, (frame[i][j]*1, 0, 0), 5)
                if frame[i][j] > maxValue:
                    maxValue = frame[i][j]
                    x = j
                    y = i

        self.directionFromPoint(x, y, maxValue)

        if self.debug:
            cv2.imshow('h', frameOriginSized)
            cv2.circle(frameOriginSized, (x*self.scaleFactor + self.shift, y*self.scaleFactor + self.shift), 8, (1, 0, 0), 5)
            cv2.imshow('j', frameOriginSized)
            cv2.waitKey(0)

    def directionFromPoint(self, x, y, maxValue):
        if maxValue < self.threshold:
            print('no viable path')
            print(maxValue)
            return 'stop'

        #determine how to get there
        if x > self.upperXBound:
            print('right')
        elif x < self.lowerXBound:
            print('left')
        else: print('no x axis changes required')

        if y > self.upperYBound:
            print('down')
        elif y < self.lowerYBound:
            print('up')
        else: print('no y axis changes required')

def findClosestSafeDirection(frame):
    #Need a threshold
    pass

def findClosestSpotToOriginal(frame, directionDesired):
    pass
