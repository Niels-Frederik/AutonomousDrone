import numpy as np
import cv2



class Camera():
    def __init__(self, folder, image):
        #folder = './Calibration/outputs/'
        self.rms = np.load(folder + 'rms.npy')
        self.cameraMatrix = np.load(folder + 'cameraMatrix.npy')
        self.distCoeffs = np.load(folder + 'distCoeffs.npy')
        self.rvecs = np.load(folder + 'rvecs.npy')
        self.tvecs = np.load(folder + 'tvecs.npy')
        h, w = image.shape[:2]
        self.newCameraMatrix, self.roi = cv2.getOptimalNewCameraMatrix(self.cameraMatrix, self.distCoeffs, (w,h), 1)

    def undistort(self, image):
        newImage = cv2.undistort(image, self.cameraMatrix, self.distCoeffs, None, self.newCameraMatrix)
        x, y, w, h = self.roi
        newImageCrop = newImage[y:y+h, x:x+w]
        return newImageCrop


