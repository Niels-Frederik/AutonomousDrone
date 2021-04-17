import psdrone3
import cv2
from controller import Controller

class DroneController(Controller):
    def __init__(self, debug):
        drone = psdrone3.Drone()
        drone.startup()
        drone.reset()
        while(drone.getBattery()[0] == -1): time.sleep(0.1)
        if debug: print("Battery: " + str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]))
        drone.useDemoMode(True)
        drone.setConfigAllID()
        drone.sdVideo()
        drone.frontCam()
        CDC = drone.ConfigDataCount
        while CDC == drone.ConfigDataCount: time.sleep(0.0001)
        drone.startVideo()
        drone.showVideo()
        self.drone = drone
        self.IMC = drone.VideoImageCount

    def getNewImage(self):
        while self.drone.VideoImageCount == self.IMC: time.sleep(0.01) # wait for new frame
        self.IMC = drone.VideoImageCount
        img = drone.VideoImage
        if debug:
            cv2.imshow('droneFrame', img)
            cv2.waitKey(1)
        return img

    def stop(self):
        self.drone.hover()
        super().stop()

    def takeoff(self):
        self.drone.takeoff()
        super().takeoff()

    def land(self):
        self.drone.land()
        super().land()

    def rotateLeft(self):
        self.drone.turnLeft()
        super().rotateLeft()

    def rotateRight(self):
        self.drone.turnRight()
        super().rotateRight()

    def moveForward(self):
        self.drone.moveForward()
        super().moveForward()

    def moveBackward(self):
        self.drone.moveBackward()
        super().moveBackward()

    def moveLeft(self):
        self.drone.moveLeft()
        super().moveLeft()

    def moveRight(self):
        self.drone.moveRight()
        super().moveRight()
