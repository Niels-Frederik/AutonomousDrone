import numpy as np
import cv2
from matplotlib import pyplot as plt
import imageComparison as IC
#from DepthEstimator/DepthEstimation
from FeatureMatcher import FeatureMatcher

featureMatcher = FeatureMatcher()
def estimateDepth(frame1, frame2, test):
    print('this is the depth estimator')

    #depthImage = frame2
    #depthImage = findBlobs(frame2, test)
    #depthImage = findMatches(frame2, test)
    depthImage = featureMatcher.findMatches(frame2, test)

    #frame1 = cv2.cvtColor(frame1, cv2.COLOR_RGBA2GRAY)
    #frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGBA2GRAY)
    #depthImage = disparity(frame1, frame2)
    return depthImage

def findBlobs(image, test):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.SimpleBlobDetector_create()
    #showImage('test', image)
    keypoints = detector.detect(image)
    if test:
        image = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return image

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
