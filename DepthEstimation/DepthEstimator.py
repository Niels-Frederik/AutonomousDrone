import numpy as np
import cv2
from matplotlib import pyplot as plt
import imageComparison as IC
from FeatureMatcher import FeatureMatcher
import ANMS
import denseDepth


featureMatcher = FeatureMatcher()
def estimateDepthImage(frame, test):
    print('this is the depth estimator')

    depthImage = denseDepth.processImage(frame)
    return depthImage

def estimateDepthFeatureMatcher(frame, test):
    if featureMatcher == None:
        featureMatcher = FeatureMatcher()
    depthImage = featureMatcher.findMatches(frame, test)
    #ANMS.findKeyPoints(frame)
    #depthImage = findBlobs(frame, test)
    #depthImage = findMatches(frame, test)

def findBlobs(image, test):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.SimpleBlobDetector_create()
    #showImage('test', image)
    keypoints = detector.detect(image)
    if test:
        image = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return image

def disparity(img2, img1):
    img1 = cv2.cvtColor(img1, cv2.COLOR_RGBA2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGBA2GRAY)
    disparity = stereo.compute(img1, img2)
    return disparity





if __name__ == '__main__':
    img1 = loadImage('../Source/test7.png')
    img2 = loadImage('../Source/test8.png')

    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    stereo.setTextureThreshold(100)
    #stereo.setPreFilterSize(5)
    #stereo.setPreFilterCap(61)
    stereo.setMinDisparity(-15)
    stereo.setUniquenessRatio(15)
    stereo.setSpeckleRange(5)
    stereo.setSpeckleWindowSize(4)

    showImage('input', img1)

    findMatches(img1, img2)

    disp1 = cv2.imread('../Source/disparity1.png')
    disp2 = cv2.imread('../Source/disparity2.png')
    disparity(disp1, disp2)
