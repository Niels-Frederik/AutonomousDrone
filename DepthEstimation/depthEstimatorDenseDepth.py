

from depthEstimator import DepthEstimator

class DepthEstimatorDenseDepth(DepthEstimator):
    def __init__(self, debug):
        from denseDepth import DenseDepth
        #Make variable for using other depth image machine learning models
        self.debug = debug
        self.denseDepth = DenseDepth()

    def estimateDepth(self, frame):
        depthImage = self.denseDepth.processImage(frame)
        return depthImage
