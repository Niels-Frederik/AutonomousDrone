import os
import glob
import argparse
import matplotlib

from datetime import datetime
import PIL.Image as pil
from mss import mss
from PIL import Image
import numpy as np
import cv2


# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
import keras
from keras.models import load_model
from DenseDepth.layers import BilinearUpSampling2D
from DenseDepth.utils import predict, load_images, load_image, display_images
from matplotlib import pyplot as plt

class DenseDepth():
    def __init__(self):
        custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}
        self.model = load_model('./DepthEstimation/DenseDepth/nyu.h5', custom_objects=custom_objects, compile=False)
        #keras.backend.set_learning_phase(0)
        #self.model.__call__(training=False)

    def processImage(self, image):
        image = Image.fromarray(image)
        images = []
        images.append(image)
        images[0] = images[0].resize((640, 480), pil.LANCZOS)
        #images[0] = images[0].resize((224, 224), pil.LANCZOS)
        #images[0] = images[0].resize((320, 320), pil.LANCZOS)
        image = load_image(images)
        outputs = predict(self.model, image, batch_size=1)
        output = np.array([[val[0] for val in sublist] for sublist in outputs[0]])
        output = cv2.resize(output, (320, 240))
        return output
