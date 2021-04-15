

from depthEstimator import DepthEstimator
import denseDepth

class DepthEstimatorDepthImage(DepthEstimator):
    def __init__(self, debug):
        #Make variable for using other depth image machine learning models
        self.debug = debug

    def estimateDepth(self, frame):
        depthImage = denseDepth.processImage(frame)
        return depthImage
