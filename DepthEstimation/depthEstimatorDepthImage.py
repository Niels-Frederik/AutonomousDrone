

from depthEstimator import DepthEstimator
from denseDepth import DenseDepth

class DepthEstimatorDepthImage(DepthEstimator):
    def __init__(self, debug):
        #Make variable for using other depth image machine learning models
        self.debug = debug
        self.denseDepth = DenseDepth()

    def estimateDepth(self, frame):
        depthImage = self.denseDepth.processImage(frame)
        return depthImage
