import cv2

class CollisionAvoider():
    def __init__(self, frame, debug):
        self.scaleFactor = 32
        self.height = int(frame.shape[0]/self.scaleFactor)
        self.width = int(frame.shape[1]/self.scaleFactor)
        self.debug = debug

    def avoidCollisions(self, frame):
        pass