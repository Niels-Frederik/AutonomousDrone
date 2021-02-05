import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

def loadImage(path):
    #use os.path.join to make it work on all OS systems
    img = cv2.imread(path)
    return img


def showImage(imgName, image):
    cv2.imshow(imgName, image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
       return

def handleImage(image):
    #Do something
    print('not implemented')
    findBlobs(image)

def findBlobs(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image = cv2.imread('/Users/martinholst/Desktop/2.png', cv2.IMREAD_GRAYSCALE)

    surf = cv2.SURF()
    mask = np.uint8(np.ones(gray.shape))
    surf_points = surf.detect(gray, mask)
    blobImg = cv2.drawKeypoints(image, keypoint, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return blobImg

    #detector = cv2.SimpleBlobDetector()
    #keypoints = detector.detect(image)
    #blobImg = cv2.drawKeypoints(image, keypoint, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
def findDistanceFromMatches(matches, kp1, kp2):
    good = []
    for m in matches:
        if m.distance < 60:
            good.append(m)
    #good = matches
    
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good])

    z1 = np.array([[complex(c[0],c[1]) for c in pts1]])
    z2 = np.array([[complex(c[0],c[1]) for c in pts2]])

    kp_dist1 = abs(z1.T - z1)
    kp_dist2 = abs(z2.T - z2)

    FM_dist = abs(z2 - z1)

    tup = (pts1, pts2, FM_dist)

    #sorted(tup, key = lambda x:x[1])
    return tup

def colorBasedOnDifference(distance):

    blue = 255
    red = 255
    if distance > 500:
        print(distance)
        distance = 500
    x = distance/500 * 255
    blue = blue - x
    red = abs(red - blue)

    tup = (int(blue), 0, int(red))
    return tup

def findMatches(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    kp1, descriptor1 = orb.detectAndCompute(gray1, None)
    kp2, descriptor2 = orb.detectAndCompute(gray2, None)
    bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bfMatcher.match(descriptor1, descriptor2)

    goodKp1, goodKp2, distance = findDistanceFromMatches(matches, kp1, kp2)
    
    newFrame1 = image1
    newFrame2 = image2

    for i in range(len(goodKp2)):
        c = colorBasedOnDifference(distance[0][i])
        print(c)
        newFrame1 = cv2.circle(newFrame1, (int(goodKp1[i][0]),int(goodKp1[i][1])), radius=10, color=c, thickness=10)
        newFrame2 = cv2.circle(newFrame2, (int(goodKp2[i][0]),int(goodKp2[i][1])), radius=10, color=c, thickness=10)


    #matches = sorted(matches, key = lambda x:x.distance)
    #img3 = cv2.drawMatches(gray1, kp1, gray2, kp2, matches[:10], None, flags=4)
    #plt.imshow(img3)

    cv2.imshow('frame1', newFrame1)
    showImage('frame2', newFrame2)

def disparity():
    img1 = cv2.imread('/Users/martinholst/Desktop/test7.png', 0)
    img2 = cv2.imread('/Users/martinholst/Desktop/test8.png', 0)
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(img1, img2)
    plt.imshow(disparity, 'gray')
    plt.show()

#img = loadImage('/Users/martinholst/Desktop/test1.png')
#img2 = loadImage('/Users/martinholst/Desktop/test2.png')

#img = loadImage('/Users/martinholst/Desktop/test3.png')
#img2 = loadImage('/Users/martinholst/Desktop/test4.png')

img = loadImage('/Users/martinholst/Desktop/test5.png')
img2 = loadImage('/Users/martinholst/Desktop/test6.png')

showImage('without blobs', img)
#blobImg = findBlobs(img)
#showImage('with blobs', blobImg)

findMatches(img, img2)

disparity()
