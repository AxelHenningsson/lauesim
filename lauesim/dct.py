import numpy as np
import matplotlib.pyplot as plt
from lauesim.geometry import dctSetup
from lauesim.xrays import xrays
from lauesim.sample import crystal
from scipy.spatial.transform import Rotation
from lauesim._draw3D import draw

class model(object):

    def __init__(self):
        np.random.seed(1)
        unit_cell = [4.926, 4.926, 5.4189, 90., 90., 120.]
        sgname = 'P3221'
        orientation = Rotation.random().as_matrix()
        points = (np.random.rand(1024,3)-0.5)*1000
        points = points[np.linalg.norm(points, axis=1) < 500,:]
        self.sample = crystal(points, orientation, unit_cell, sgname)

        source = np.array([-55000, 0, 0])
        detector_shape = (1024, 1024)
        pixelsize = 25 # microns
        beamstop_shape = (256, 256)
        self.geometry = dctSetup(source, detector_shape, pixelsize, beamstop_shape)

        wavelength = np.linspace(0.1127134*0.65, 0.1127134*1.35, 100)
        std = wavelength[6]-wavelength[0]
        intensity =  np.exp( -0.5*(np.mean(wavelength)-wavelength)**2/std**2 )

        self.xray = xrays(intensity, wavelength)
        self.sample.diffract(self.geometry, self.xray)

    def collect(self):
        self.sample.diffract(self.geometry, self.xray)

    def show(self):
        image = self.geometry.render()
        draw( image, self.geometry, self.sample )


if __name__ == "__main__":
    dct = model()
    dct.collect()
    dct.show()