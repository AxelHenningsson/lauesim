import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

class dctSetup(object):

    def __init__(self, source, detector_shape, pixelsize, beamstop_shape):
        self.source = source
        self.working_distance = np.abs(source[0])
        self.detector_shape = detector_shape
        self.pixelsize = pixelsize
        self.beamstop_shape = beamstop_shape
        self.frame = np.zeros(detector_shape)
        self.d0   = np.array( [ self.working_distance, -detector_shape[0]*pixelsize/2., -detector_shape[1]*pixelsize/2.] )

    def add_rays(self, sources, directions, intensity):
        s   = ( self.working_distance - sources[:,0] )/directions[:,0]
        p3d = sources + s.reshape(len(s),1)*directions
        p2d = p3d - self.d0
        det_y = np.round(p2d[:,1]/self.pixelsize).astype(int)
        det_z = np.round(p2d[:,2]/self.pixelsize).astype(int)
        mask = (det_z < self.detector_shape[0] )*( det_y < self.detector_shape[1] )*( det_z>0 )*( det_y>0 )
        det_y = det_y[mask]
        det_z = det_z[mask]
        self.frame[det_z, det_y] += intensity[mask]

    def render(self):
        self.frame = gaussian_filter(self.frame, sigma=5)
        self.frame += np.abs( np.random.normal(0, np.max(self.frame)/7., size=self.frame.shape) )
        a = self.detector_shape[0]//2 - self.beamstop_shape[0]//2
        b = self.detector_shape[0]//2 + self.beamstop_shape[0]//2
        c = self.detector_shape[1]//2 - self.beamstop_shape[1]//2
        d = self.detector_shape[1]//2 + self.beamstop_shape[1]//2
        self.frame[a:b,c:d] = 0
        return self.frame

if __name__ == "__main__":
    N = 512
    sources = (np.random.rand(N,3)-0.5)*0.5
    directions = np.zeros((N,3))
    directions[:,0]=1
    intensity = np.ones((N,))

    source = np.array([-1,0,0])
    detector_shape = (1024,1024)
    pixelsize = 2./detector_shape[0]
    beamstop_shape = (128,128)

    dct = dctSetup(source, detector_shape, pixelsize, beamstop_shape)
    dct.add_rays(sources, directions, intensity)

    plt.imshow(dct.frame, cmap='gray')
    plt.show()