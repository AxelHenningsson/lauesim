import numpy as np
import matplotlib.pyplot as plt
from xfab import tools
from scipy.spatial.transform import Rotation

class crystal(object):

    def __init__(self, points, orientation, unit_cell, sgname):
        self.points = points
        self.orientation = orientation
        self.unit_cell = unit_cell
        self.sgname = sgname
        self._rotation_angle = 0
        self.B  = tools.form_b_mat(unit_cell)

    def diffract(self, dct_setup, xrays):
        sintlmin = np.sin(np.radians(0.01))/np.mean(xrays.wavelength)
        sintlmax = np.sin(np.radians(5))/np.mean(xrays.wavelength)
        self.hkls = tools.genhkl_all(self.unit_cell, sintlmin, sintlmax, sgname=self.sgname)
        Gs = self.orientation.dot(self.B.dot(self.hkls.T)).T
        k = self.points - dct_setup.source

        for G in Gs:
            d = 2*np.pi / np.linalg.norm(G)
            ghat = G/np.linalg.norm(G)
            khat = k/np.linalg.norm(k,axis=1).reshape(k.shape[0],1)
            theta = np.arccos( khat.dot(ghat) ) - (np.pi/2)
            wavelength = np.sin( theta ) * 2 * d
            intensity = xrays(wavelength)
            if np.sum(intensity)==0: continue
            kscatter = 2*np.pi * khat / wavelength.reshape(khat.shape[0],1)
            kprime = G + kscatter
            dct_setup.add_rays(self.points, kprime, intensity)

    @property
    def rotation_angle(self, angle):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, angle):
        s, c = np.sin(angle), np.cos(angle)
        R = np.array([[c,-s,0],[s,c,0],[0,0,1]])
        self.points = R.dot( self.points.T ).T
        self.orientation = R.dot(self.orientation)
        self._rotation_angle = angle

if __name__ == "__main__":
    np.random.seed(1)
    unit_cell = [4.926, 4.926, 5.4189, 90., 90., 120.]
    sgname = 'P3221'
    orientation = Rotation.random().as_matrix()
    points = (np.random.rand(1024,3)-0.5)*1000
    points = points[np.linalg.norm(points, axis=1) < 500,:]
    cr = crystal(points, orientation, unit_cell, sgname)

    source = np.array([-55000, 0, 0])
    detector_shape = (1024, 1024)
    pixelsize = 25 # microns
    beamstop_shape = (256, 256)
    from lauesim.geometry import dctSetup
    dct_setup = dctSetup(source, detector_shape, pixelsize, beamstop_shape)

    wavelength = np.linspace(0.1127134*0.65, 0.1127134*1.35, 100)
    std = wavelength[6]-wavelength[0]
    intensity =  np.exp( -0.5*(np.mean(wavelength)-wavelength)**2/std**2 )

    from xrays import xrays
    xray = xrays(intensity, wavelength)

    cr.rotation_angle = np.radians(120.0)
    cr.diffract(dct_setup, xray)

    plt.imshow(dct_setup.render(), cmap='gray')
    plt.show()
