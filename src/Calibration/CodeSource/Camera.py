from scipy import linalg

class Camera(object):
    def __init__(self, P):
        self.P = P
        self.K = None # calibration matrix
        self.R = None # rotation
        self.t = None # translation
        self.c = None # camera Center

    #Projects from points and normalize coordinates
    def project(self, X):
        x = dot(self.P, X)
        for i in range(3):
            x[i] /= x[2]
        return x
        
    #Factorize the camera matrix into K, R, t as P = K[R|t]
    def factor(self):
        K, R = linalg.rq(self.P[:,:3])

        T = diag(sign(diag(K)))
        if linalg.det(T) < 0:
            T[1,1] *= -1

        self.K = dot(K, T)
        self.R = dot(T, R)
        self.t = dot(linalg.inv(self.K), self.P[:, 3])

        return self.K, self.R, self.t

    def center(self):
        if self.c is not None:
            return self.c
        else:
            self.factor()
            self.c = -dot(self.R.T, self.t)
            return self.c
