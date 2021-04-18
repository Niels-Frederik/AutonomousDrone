import os
import glob
import argparse
import matplotlib

from datetime import datetime
import PIL.Image as pil
from mss import mss
from PIL import Image
import numpy as np


# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
from layers import BilinearUpSampling2D
from utils import predict, load_images, load_image, display_images
from matplotlib import pyplot as plt

class DenseDepth():
    def __init__(self):
        print('Loading model...')
        parser = argparse.ArgumentParser(description='High Quality Monocular Depth Estimation via Transfer Learning')
        parser.add_argument('--model', default='DepthEstimation/DenseDepth/nyu.h5', type=str, help='Trained Keras model file.')
        args = parser.parse_args()
        custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}
        self.model = load_model(args.model, custom_objects=custom_objects, compile=False)
        print('Model loaded ({0}).'.format(args.model))

    def processImage(self, image):
        image = Image.fromarray(image)
        images = []
        images.append(image)
        images[0] = images[0].resize((640, 480), pil.LANCZOS)
        image = load_image(images)
        outputs = predict(self.model, image)
        #output = [[val for subsublist in sublist for val in subsublist] for sublist in output]
        output = np.array([[val[0] for val in sublist] for sublist in outputs[0]])
        return output
