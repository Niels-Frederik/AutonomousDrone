import tensorflow as tf
import sys
import os
import argparse
import time
import datetime
from utils import *
from pydnetModel import *

# forces tensorflow to run on CPU

class Pydnet():
    def __init__(self):
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        self.width = 512
        self.height = 256
        self.resolution = 1 #1:H, 2:Q, 3:E
        self.checkpoint_dir = './DepthEstimation/PyDNet/checkpoint/IROS18/pydnet'
        from os import path
        with tf.Graph().as_default():
            self.placeholders = {'im0':tf.placeholder(tf.float32,[None, None, None, 3], name='im0')}
            with tf.variable_scope("model") as scope:
              self.model = pydnet(self.placeholders)

            init = tf.group(tf.global_variables_initializer(),
                           tf.local_variables_initializer())
            self.loader = tf.train.Saver()
            self.sess = tf.Session()
            self.sess.run(init)
            self.loader.restore(self.sess, self.checkpoint_dir)

    def processImage(self, frame):
        img = cv2.resize(frame, (self.width, self.height)).astype(np.float32)/255.
        img = np.expand_dims(img, 0)
        disp = self.sess.run(self.model.results[self.resolution-1], feed_dict={self.placeholders['im0']: img})
        #disp_color = applyColorMap(disp[0,:,:,0]*20, 'plasma')
        #r = disp_color.copy()
        #for i in range(len(r)):
        #    for j in range(len(r[i])):
        #        #r[i, j, 0] = r[i, j, 0]/r[i, j, 1] * 255
        #        r[i, j, 0] = (r[i, j, 0]-r[i, j, 1]) * 2
        #r[:, :, 1] = 0
        #r[:, :, 2] = 0
        #output = cv2.cvtColor(r, cv2.COLOR_RGB2GRAY)

        outputInverse = disp[0,:,:,0]*20
        #output = cv2.bitwise_not(output)
        output = (1-outputInverse)

        #cv2.imshow('k', output)
        #cv2.waitKey(0)
        #depthImage = (np.concatenate((img[0], disp_color), 0)*255.).astype(np.uint8)
        #depthImage = cv2.resize(depthImage, (frame.shape[1], frame.shape[0]))
        #return depthImage
        #return disp_color
        output = cv2.resize(output, (320, 240))
        return output

def main(_):
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    parser = argparse.ArgumentParser(description='Argument parser')
    """ Arguments related to network architecture"""
    parser.add_argument('--width', dest='width', type=int, default=512, help='width of input images')
    parser.add_argument('--height', dest='height', type=int, default=256, help='height of input images')
    parser.add_argument('--resolution', dest='resolution', type=int, default=1, help='resolution [1:H, 2:Q, 3:E]')
    parser.add_argument('--checkpoint_dir', dest='checkpoint_dir', type=str, default='checkpoint/IROS18/pydnet', help='checkpoint directory')

    args = parser.parse_args()

    with tf.Graph().as_default():
        height = args.height
        width = args.width
        placeholders = {'im0':tf.placeholder(tf.float32,[None, None, None, 3], name='im0')}

        with tf.variable_scope("model") as scope:
          model = pydnet(placeholders)

        init = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

        loader = tf.train.Saver()

        with tf.Session() as sess:
            sess.run(init)
            loader.restore(sess, args.checkpoint_dir)
            #folder = '/home/yarl/Desktop/Github/AutonomousDrone/Output/ipadVideo'
            #folder = '/home/yarl/Desktop/Github/AutonomousDrone/Output/droneVideo3.0'
            folder = '../../../Output/droneVideo3.0'
            for filename in os.listdir(folder):
                img = cv2.imread(os.path.join(folder, filename))
                img = cv2.resize(img, (width, height)).astype(np.float32)/255.
                img = np.expand_dims(img, 0)
                start = time.time()
                disp = sess.run(model.results[args.resolution-1], feed_dict={placeholders['im0']: img})
                end = time.time()

                disp_color = applyColorMap(disp[0,:,:,0]*20, 'plasma')
                toShow = (np.concatenate((img[0], disp_color), 0)*255.).astype(np.uint8)
                toShow = cv2.resize(toShow, (int(width/2), int(height)))

                cv2.imshow('pydnet', toShow)
                cv2.waitKey(1000)

if __name__ == '__main__':
    tf.app.run()
