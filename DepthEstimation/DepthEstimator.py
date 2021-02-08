import numpy as np
import cv2
from matplotlib import pyplot as plt

def estimateDepth(frame1, frame2):
    print('this is the depth estimator')
    #depthImage = frame
    depthImage = findMatches(frame1, frame2)
    return depthImage

def loadImage(path):
    # use os.path.join to make it work on all OS systems
    img = cv2.imread(path)
    return img


def showImage(imgName, image):
    cv2.imshow(imgName, image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        return

def findDistanceFromMatches(matches, kp1, kp2):
    good = []
    for m in matches:
        if m.distance < 60:
            good.append(m)
    # good = matches

    pts1 = np.float32([kp1[m.queryIdx].pt for m in good])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good])

    z1 = np.array([[complex(c[0], c[1]) for c in pts1]])
    z2 = np.array([[complex(c[0], c[1]) for c in pts2]])

    kp_dist1 = abs(z1.T - z1)
    kp_dist2 = abs(z2.T - z2)

    FM_dist = abs(z2 - z1)

    tup = (pts1, pts2, FM_dist)

    # sorted(tup, key = lambda x:x[1])
    return tup


def colorBasedOnDifference(distance):
    blue = 255
    red = 255
    if distance > 500:
        distance = 500
    x = distance / 500 * 255
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

    #newFrame1 = image1
    newFrame2 = image2.copy()

    for i in range(len(goodKp2)):
        c = colorBasedOnDifference(distance[0][i])
        #newFrame1 = cv2.circle(newFrame1, (int(goodKp1[i][0]), int(goodKp1[i][1])), radius=10, color=c, thickness=10)
        newFrame2 = cv2.circle(newFrame2, (int(goodKp2[i][0]), int(goodKp2[i][1])), radius=10, color=c, thickness=10)

    # matches = sorted(matches, key = lambda x:x.distance)
    # img3 = cv2.drawMatches(gray1, kp1, gray2, kp2, matches[:10], None, flags=4)
    # plt.imshow(img3)

    #cv2.imshow('frame1', newFrame1)
    #showImage('frame2', image2)
    return newFrame2


def disparity(img1, img2):
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    #disparity = stereo.compute(img1, img2)
    disparity = stereo.compute(img2, img1)
    plt.imshow(disparity, 'gray')
    plt.show()

if __name__ == '__main__':
    img1 = loadImage('../Source/test7.png')
    img2 = loadImage('../Source/test8.png')

    showImage('input', img1)

    findMatches(img1, img2)

    disp1 = cv2.imread('../Source/disparity1.png', 0)
    disp2 = cv2.imread('../Source/disparity2.png', 0)
    disparity(disp1, disp2)
