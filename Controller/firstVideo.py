##### Suggested clean drone startup sequence #####
import time, sys
import Drone_API

print('hihihihi')

drone = Drone_API.Drone() 
print("Battery: test")

drone.startup()
#drone.reset()
drone.printBlue('ready')
while (drone.getBattery()[0]==-1): time.sleep(0.1) #Reset completed ? 
print("Battery:"+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]))
drone.useDemoMode(True) #15 basic datasets per second 
drone.getNDpackage(["demo","vision detect"]) #Packets to decoded
time.sleep(0.5)

##### Mainprogram #####
CDC = drone.ConfigDataCount
drone.setConfigAllID()
drone.sdVideo()
drone.frontCam()
while CDC==drone.ConfigDataCount: time.sleep(0.001) #Wait until it is done 
drone.startVideo() #Start video-function
drone.showVideo() #Display the video

print("<space> to toggle front- and groundcamera, any other key to stop") 
IMC = drone.VideoImageCount #Number of encoded videoframes
stop = False
ground = False #To toggle front- and groundcamera

while drone.VideoImageCount==IMC: time.sleep(0.01) #Wait for next image 
IMC = drone.VideoImageCount #Number of encoded videoframes
key = drone.getKey()
if key==" ":
    if ground: ground = False
    else: ground = True
    drone.groundVideo(ground) #Toggle between front- and groundcamera.
elif key and key!=" ": stop=True