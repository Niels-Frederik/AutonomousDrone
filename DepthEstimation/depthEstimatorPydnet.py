from depthEstimator import DepthEstimator

class DepthEstimatorPydnet(DepthEstimator):
    def __init__(self, debug):
        from pydnet import Pydnet
        self.debug = debug
        #self.pydnet = None
        self.pydnet = Pydnet()

    def estimateDepth(self, frame):
        depthImage = self.pydnet.processImage(frame)
        return depthImage
