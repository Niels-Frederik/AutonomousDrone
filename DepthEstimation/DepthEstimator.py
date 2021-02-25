import numpy as np
import cv2
from matplotlib import pyplot as plt
import imageComparison as IC

def estimateDepth(frame1, frame2, test):
    print('this is the depth estimator')

    #depthImage = frame2
    #depthImage = findBlobs(frame2, test)
    depthImage = findMatches(frame1, frame2, test)

    #frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGBA2GRAY)
    #frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGBA2GRAY)
    #depthImage = disparity(frame1, frame2)
    return frame2, depthImage

def loadImage(path):
    # use os.path.join to make it work on all OS systems
    img = cv2.imread(path)
    return img


def showImage(imgName, image):
    cv2.imshow(imgName, image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        return

def findBlobs(image, test):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.SimpleBlobDetector_create()
    #showImage('test', image)
    keypoints = detector.detect(image)
    if test:
        image = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return image

def findDistanceFromMatches(matches, kp1, kp2):
    good = []
    for m in matches:
        if m.distance < 20:
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

    #sorted(tup, key = lambda x:x[2][0])
    #tup.sort(key=lambda x: x[0])
    #zipped = list(zip(pts1, pts2, FM_dist))
    #zipped.sort(key=lambda x: x[2])
    return tup


def colorBasedOnDifference(distance, maxDist):
    blue = 255
    red = 255
    x = distance / maxDist * 255
    blue = blue - x
    red = abs(red - blue)

    tup = (int(blue), 0, int(red))
    return tup


def findMatches(image1, image2, test):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(patchSize=111, nfeatures=3000, scoreType=cv2.ORB_FAST_SCORE)
    #orb = cv2.ORB_create(edgeThreshold=15, patchSize=31, nlevels=8, fastThreshold=20, scaleFactor=1.2, WTA_K=2,scoreType=cv2.ORB_HARRIS_SCORE, firstLevel=0, nfeatures=500)
    kp1, descriptor1 = orb.detectAndCompute(gray1, None)
    kp2, descriptor2 = orb.detectAndCompute(gray2, None)
    bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bfMatcher.match(descriptor1, descriptor2)
    #descriptor = cv2.xfeatures2d.BEBLID_create(0.75)
    #kp1 = orb.detect(gray1, None)
    #descriptor1 = descriptor.compute(gray1, kp1)
    #kp2 = orb.detect(gray2, None)
    #descriptor2 = descriptor.compute(gray2, kp2)
    #matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    #nn_matches = matcher.knnMatch(descriptor1, descriptor2, 2)

    goodKp1, goodKp2, distance = findDistanceFromMatches(matches, kp1, kp2)

    maxDist = distance[0][0]
    for dist in distance[0]:
        if dist > maxDist:
            maxDist = dist
    #newFrame1 = image1
    if test:
        newFrame2 = image2.copy()
        for i in range(len(goodKp2)):
            c = colorBasedOnDifference(distance[0][i], maxDist)
            #newFrame1 = cv2.circle(newFrame1, (int(goodKp1[i][0]), int(goodKp1[i][1])), radius=10, color=c, thickness=10)
            cv2.circle(newFrame2, (int(goodKp2[i][0]), int(goodKp2[i][1])), radius=5, color=c, thickness=5)
        return newFrame2

    # matches = sorted(matches, key = lambda x:x.distance)
    # img3 = cv2.drawMatches(gray1, kp1, gray2, kp2, matches[:10], None, flags=4)
    # plt.imshow(img3)

    #cv2.imshow('frame1', newFrame1)
    #showImage('frame2', image2)
    return image2


stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
stereo.setTextureThreshold(100)
#stereo.setPreFilterSize(5)
#stereo.setPreFilterCap(61)
stereo.setMinDisparity(-15)
stereo.setUniquenessRatio(15)
stereo.setSpeckleRange(5)
stereo.setSpeckleWindowSize(4)
def disparity(img2, img1):
    disparity = stereo.compute(img1, img2)
    #disparity = stereo.compute(img2, img1)
    #plt.imshow(disparity, 'gray')
    #plt.show()
    return disparity

if __name__ == '__main__':
    img1 = loadImage('../Source/test7.png')
    img2 = loadImage('../Source/test8.png')

    showImage('input', img1)

    findMatches(img1, img2)

    disp1 = cv2.imread('../Source/disparity1.png', 0)
    disp2 = cv2.imread('../Source/disparity2.png', 0)
    disparity(disp1, disp2)
