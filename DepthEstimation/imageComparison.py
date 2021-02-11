import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import cv2



def valuateImage(image):
    cv2.imshow('normal', image)
    norm_img = np.zeros((image.shape[0],image.shape[1]))
    image = cv2.normalize(image, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    cv2.imshow('normalized', image)
    windows = [[],[],[],[],[]]
    #k = 64
    k = 16
    mid = int(k/2)
    for i in range(0, image.shape[0]-k, k):
        for j in range(0, image.shape[1]-k, k):
            arr = image[i:i+k, j:j+k]
            windows[0].append(np.sum(arr[:,:,0]))
            windows[1].append(np.sum(arr[:,:,1]))
            windows[2].append(np.sum(arr[:,:,2]))
            windows[3].append(i+mid)
            windows[4].append(j+mid)
            
    windows[0] = [x/(k*k) for x in windows[0]]
    windows[1] = [x/(k*k) for x in windows[1]]
    windows[2] = [x/(k*k) for x in windows[2]]
    
    rList = windows[0]
    gList = windows[1]
    bList = windows[2]
    xList = windows[3]
    yList = windows[4]
    #plot3d(rList, gList, bList)
    colorBoxes = findSimilar(rList, gList, bList, xList, yList)
    image1 = image.copy()
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    for colorBox in colorBoxes:
        r = colorBox[0][0]
        g = colorBox[0][1]
        b = colorBox[0][2]
        for box in colorBox:
            drawColorBox(image1, r, g, b, box[3], box[4])
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    cv2.imshow('color', image1)
    if cv2.waitKey(0) & ord('q'):
        return

def valuateArea(arr):
    #w = np.sum(arr)
    w = [np.sum(arr[:,:,0]), np.sum(arr[:,:,1]), np.sum(arr[:,:,2])]
    print(w)
    return w

def plot3d(r, g, b):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(r, g, b)
    ax.set_xlabel('red')
    ax.set_ylabel('green')
    ax.set_zlabel('blue')
    plt.show()

def findSimilar(rList, gList, bList, xList, yList):
    colorBoxes = [[]]
    colorBoxes[0].append([rList[0], gList[0], bList[0], xList[0], yList[0]])
    #for point in windows:
    for i in range(1,len(rList)):
        boxFound = False
        for box in colorBoxes:
            distanceToBox = dPyt(rList[i], gList[i], bList[i], box[0][0], box[0][1], box[0][2])
            if distanceToBox < 20:
                box.append([rList[i], gList[i], bList[i], xList[i], yList[i]])
                boxFound = True
                break
        if not boxFound :
            colorBoxes.append([[rList[i], gList[i], bList[i], xList[i], yList[i]]])

    print(len(colorBoxes))
    return colorBoxes

def dPyt(r1, g1, b1, r2, g2, b2):
    rdiff = r1-r2
    gdiff = g1-g2
    bdiff = b1-b2
    pyt = math.sqrt((rdiff*rdiff)+(gdiff*gdiff)+(bdiff*bdiff))
    return pyt

def drawColorBox(image, r, g, b, x, y):
    cv2.circle(image, (y, x), radius=5, color=(b, g, r), thickness=10)

def splitColorBoxOnPosition(colorBoxes):
    XYColorBoxes = [[]]

    #for colorBox in colorBoxes:


    #for colorBox in colorBoxes:
        #point1 = colorBox[0]
        #for box in colorBox:
            #distanceToP1 = dPyt(point1[0], point1[1], point1[2], box[0], box[1], box[2])
        #colorBox = sorted(colorBox, key=lambda x: dPyt(point1[0], point1[1], point1[2], x[0], x[1], x[2]))
        #previousLargestDistance = 0
        #for box in colorBox:
        #    bo
            
            
            

if __name__ == '__main__':
    import VideoIO
    image1 = VideoIO.loadImage('../Source/Images/indoor3.png')
    #image1 = VideoIO.loadImage('../Source/Images/Strawberries.jpg')
    #image1 = VideoIO.loadImage('../Source/Images/red.png')
    while(True):
        print('hi')
        valuateImage(image1)
        break;
