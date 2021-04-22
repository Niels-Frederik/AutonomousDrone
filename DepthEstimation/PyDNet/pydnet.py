import tensorflow as tf
import sys
import os
import argparse
import time
import datetime
from utils import *
from pydnetModel import *

# forces tensorflow to run on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

parser = argparse.ArgumentParser(description='Argument parser')

""" Arguments related to network architecture"""
parser.add_argument('--width', dest='width', type=int, default=512, help='width of input images')
parser.add_argument('--height', dest='height', type=int, default=256, help='height of input images')
parser.add_argument('--resolution', dest='resolution', type=int, default=1, help='resolution [1:H, 2:Q, 3:E]')
parser.add_argument('--checkpoint_dir', dest='checkpoint_dir', type=str, default='checkpoint/IROS18/pydnet', help='checkpoint directory')

args = parser.parse_args()

def main(_):

  with tf.Graph().as_default():
    height = args.height
    width = args.width
    placeholders = {'im0':tf.placeholder(tf.float32,[None, None, None, 3], name='im0')}

    with tf.variable_scope("model") as scope:
      model = pydnet(placeholders)

    init = tf.group(tf.global_variables_initializer(),
                   tf.local_variables_initializer())

    loader = tf.train.Saver()
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(init)
        loader.restore(sess, args.checkpoint_dir)
        #folder = '/home/yarl/Desktop/Github/AutonomousDrone/Output/ipadVideo'
        folder = '/home/yarl/Desktop/Github/AutonomousDrone/Output/droneVideo3.0'
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
            cv2.waitKey(1)

    return
    cam = cv2.VideoCapture(0)
    with tf.Session() as sess:
        sess.run(init)
        loader.restore(sess, args.checkpoint_dir)
        while True:
          img = cv2.resize(img, (width, height)).astype(np.float32) / 255.
          img = np.expand_dims(img, 0)
          start = time.time()
          disp = sess.run(model.results[args.resolution-1], feed_dict={placeholders['im0']: img})
          end = time.time()

          disp_color = applyColorMap(disp[0,:,:,0]*20, 'plasma')
          toShow = (np.concatenate((img[0], disp_color), 0)*255.).astype(np.uint8)
          toShow = cv2.resize(toShow, (width/2, height))

          cv2.imshow('pydnet', toShow)
          k = cv2.waitKey(1)
          if k == 1048603 or k == 27:
            break  # esc to quit
          if k == 1048688:
            cv2.waitKey(0) # 'p' to pause

          print("Time: " + str(end - start))
          del img
          del disp
          del toShow

        cam.release()

if __name__ == '__main__':
    tf.app.run()
