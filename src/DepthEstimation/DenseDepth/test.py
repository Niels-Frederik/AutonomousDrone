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


#Helper methods - can be deleted 
def mss_record(width, height, startX, startY):
    with mss() as sct:
        monitor = {'top': startY, 'left': startX, 'width': width, 'height': height}
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def captureScreen(width = 640, height = 480, startX = 0, startY = 0):
    frame = mss_record(width, height, startX, startY)
    frame = np.array(frame)
    return frame

# Argument Parser
parser = argparse.ArgumentParser(description='High Quality Monocular Depth Estimation via Transfer Learning')
parser.add_argument('--model', default='./nyu.h5', type=str, help='Trained Keras model file.')
parser.add_argument('--input', default='./examples/*.png', type=str, help='Input filename or folder.')
#parser.add_argument('--model', default='nyu.h5', type=str, help='Trained Keras model file.')
#parser.add_argument('--input', default='examples/*.png', type=str, help='Input filename or folder.')
args = parser.parse_args()

# Custom object needed for inference and training
custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}

print('Loading model...')

# Load model into GPU / CPU
model = load_model(args.model, custom_objects=custom_objects, compile=False)

print('\nModel loaded ({0}).'.format(args.model))

if True:
    while(True):
        print(datetime.now())
        images = []
        #images.append(mss_record(480, 640, 240, 320))
        images.append(mss_record(2048, 1080, 0,0))
        images[0] = images[0].resize((640, 480), pil.LANCZOS)
        #for i in range(2):
            #for j in range(2):
                #images.append(mss_record(480,640, 480*j, 640*i))
        image = load_image(images)
        outputs = predict(model, image)
        viz = display_images(outputs.copy(), image.copy())
        plt.imshow(viz)
        plt.show()


