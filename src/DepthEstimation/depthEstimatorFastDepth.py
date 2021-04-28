from depthEstimator import DepthEstimator

class DepthEstimatorFastDepth(DepthEstimator):
    def __init__(self, debug):
        from fastDepth import FastDepth
        self.debug = debug
        self.fastDepth = FastDepth()

    def estimateDepth(self, frame):
        depthImage = self.fastDepth.predict(frame)
        return depthImage
