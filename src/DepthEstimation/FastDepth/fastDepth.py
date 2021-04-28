
import cv2
import numpy as np
import models
import torch
from torchvision.transforms import ToTensor
import os
from os import path

class FastDepth():
    def __init__(self):
        checkpoint = torch.load('./DepthEstimation/FastDepth/results/mobilenet-nnconv5dw-skipadd-pruned.pth.tar', map_location='cpu')
        if type(checkpoint) is dict:
            self.model = checkpoint['model']
        else:
            self.model = checkpoint
        self.model.eval()
        self.toTensor = ToTensor()

    def predict(self, img):
        img = cv2.resize(img, (224, 224))
        tensor = self.toTensor.__call__(img)
        pred = self.model(tensor[None, ...])
        depth_img = np.squeeze(pred.data.cpu().numpy())

        #d_min = np.min(depth_img)
        #d_max = np.max(depth_img)
        d_min = 1
        d_max = 6

        output = (depth_img - d_min) / (d_max - d_min)
        output = cv2.resize(output, (360, 240))
        return output
