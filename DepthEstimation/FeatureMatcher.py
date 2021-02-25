import cv2
import numpy as np

class FeatureMatcher():
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=3000, scoreType=cv2.ORB_FAST_SCORE)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.keypoints = []
        self.descriptors = []

    def findMatches(self, image, test):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kp, descriptor = self.orb.detectAndCompute(gray, None)
        self.keypoints.append(kp)
        self.descriptors.append(descriptor)

        if len(self.keypoints) == 1:
            return image

        matches = self.matcher.match(self.descriptors.pop(0), descriptor)
        goodKps, distances = self.findDistanceBetweenMatches(matches, self.keypoints.pop(0), kp)

        #Removing the largest outliers
        length = len(distances)
        largeDist = distances[length-50]
        numberRemoved = 0
        if largeDist > sum(distances)/len(distances)*1.5:
            for i in range(75):
                #if largeDist * 1.5 < distances[length-1-i]:
                if True:
                    numberRemoved = i
                else:
                    break;

        print('number skipped: ' + str(numberRemoved))

        if test:
            newFrame = image.copy()
            maxDist = distances[len(distances)-1-numberRemoved]
            for i in range(len(goodKps)-numberRemoved):
                c = self.colorBasedOnDistance(distances[i], maxDist)
                cv2.circle(newFrame, (int(goodKps[i][0]), int(goodKps[i][1])), radius=5, color=c, thickness=5)
            return newFrame
        return image

    def findDistanceBetweenMatches(self, matches, kp1, kp2):
        good = []
        for m in matches:
            if m.distance < 20:
                good.append(m)

        pts1 = np.float32([kp1[m.queryIdx].pt for m in good])
        pts2 = np.float32([kp2[m.trainIdx].pt for m in good])

        z1 = np.array([[complex(c[0], c[1]) for c in pts1]])
        z2 = np.array([[complex(c[0], c[1]) for c in pts2]])

        kp_dist1 = abs(z1.T - z1)
        kp_dist2 = abs(z2.T - z2)

        FM_dist = abs(z2 - z1)
        FM_dist = FM_dist[0]

        #tup = (pts2, FM_dist)

        zipped = list(zip(pts2, FM_dist))
        zipped.sort(key=lambda x: x[1])
        tup = zip(*zipped)
        tup = list(tup)
        return tup

    def colorBasedOnDistance(self, distance, maxDist):
        maxDist = maxDist*1.5
        blue = 255
        red = 255
        x = distance / maxDist * 255
        blue = blue - x
        red = abs(red - blue)
        tup = (int(blue), 0, int(red))
        return tup
