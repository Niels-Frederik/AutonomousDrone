import numpy as np
import cv2
from matplotlib import pyplot as plt

folder = "./outputs/"
rms = np.load(folder + "rms.npy")
cameraMatrix = np.load(folder + "cameraMatrix.npy")
distCoeffs = np.load(folder + "distCoeffs.npy")
rvecs = np.load(folder + "rvecs.npy")
vects = np.load(folder + "tvecs.npy")




def undistort(image):
    h, w = image.shape[:2]

    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w,h), 1)

    newImage = cv2.undistort(image, cameraMatrix, distCoeffs, None, newCameraMatrix)
    x,y,w,h = roi
    newImageCrop = newImage[y:y+h, x:x+w]
    return newImageCrop



def disparity(img1, img2):
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=9)
    #disparity = stereo.compute(img1, img2)
    disparity = stereo.compute(img1, img2)
    plt.imshow(disparity, 'gray')
    plt.show()





#image = cv2.imread('input/IMG_0453.jpg',0)
#image = cv2.imread('input/IMG_0455.jpg',0)
image = cv2.imread('test/IMG_0457.jpg',0)
undistortImage1 = undistort(image)
#image2 = cv2.imread('input/IMG_0454.jpg',0)
#image2 = cv2.imread('input/IMG_0456.jpg',0)
image2 = cv2.imread('test/IMG_0458.jpg',0)
undistortImage2 = undistort(image2)

disparity(undistortImage1, undistortImage2)
