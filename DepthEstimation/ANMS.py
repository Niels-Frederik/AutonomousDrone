#Efficient adaptive non-maximal suppression algorithms for homogeneous spatial keypoint distribution
#https://github.com/BAILOOL/ANMS-Codes

import numpy as np
from random import shuffle
import cv2
from ssc import ssc


def findKeyPoints(image):
    print('test0')
    fast = cv2.FastFeatureDetector_create()
    print('test1')
    keypoints = fast.detect(image, None)
    print('test2')
    image2 = image.copy()
    cv2.drawKeypoints(image, keypoints, color=(255, 0, 0), outImage=image2)
    print('test3')
    cv2.imshow("detected FAST keypoints", image2) 
    cv2.waitKey(0)

    #shuffle(keypoints)

    selected_keypoints = ssc(
        keypoints, 500, 0.1, image.shape[1], image.shape[0]
    )

    image3 = image.copy()
    cv2.drawKeypoints(image, selected_keypoints, color=(255, 0, 0), outImage=image3)
    cv2.imshow("Selected keypoints", image3)
    cv2.waitKey(0)

    br = cv2.BRISK_create()
    kp, des = br.compute(image, selected_keypoints)

