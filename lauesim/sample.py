import numpy as np
import matplotlib.pyplot as plt
from xfab import tools, structure
from scipy.spatial.transform import Rotation
from CifFile import ReadCif

class crystal(object):

    def __init__(self, points, orientation, unit_cell, sgname, cif=None, hkls=None):
        self.points = points
        self.unit_cell = unit_cell
        self.sgname = sgname
        self._rotation_angle = 0
        self.orientation = orientation
        self._cif   = cif
        self._hkls  = hkls
        self.F2     = self._get_structure_factors()

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        if len( orientation.shape ) == 2:
            self._orientation = np.array([orientation.copy() for _ in range(self.points.shape[0])])
        else:
            self._orientation = orientation
        assert self._orientation.shape==(self.points.shape[0], 3, 3)
        B  = tools.form_b_mat(self.unit_cell)
        self.UB = np.array([U.dot(B) for U in self._orientation])

    def _get_structure_factors(self):
        if self.cif is None:
            return np.ones((self._hkls.shape[0],))
        else:
            atom_factory = structure.build_atomlist()
            cif_dict = ReadCif(self._cif)
            cifblk =  cif_dict[list(cif_dict.keys())[0]]
            atom_factory.CIFread(
                ciffile=None,
                cifblkname=None,
                cifblk=cifblk)
            atoms = atom_factory.atomlist.atom
            structure_factors = np.zeros((self._hkls.shape[0], 2))
            for i, hkl in enumerate(self._hkls):
                structure_factors[i, :] = structure.StructureFactor(
                    hkl, self.unit_cell, self.sgname, atoms, disper=None)
            return np.sum(structure_factors**2, axis=1)

    @property
    def cif(self):
        return self._cif

    @cif.setter
    def cif(self, cif):
        self._cif = cif
        self.F2 = self._get_structure_factors()

    @property
    def hkls(self):
        return self._hkls

    @hkls.setter
    def hkls(self, hkls):
        self.F2 = self._get_structure_factors()
        self._hkls = hkls

    def diffract(self, dct_setup, xrays):
        k = self.points - dct_setup.source
        for f2,hkl in zip(self.F2, self.hkls):
            G  = self.UB.dot(hkl)
            d = 2*np.pi / np.linalg.norm(G, axis=1)
            ghat = G/np.linalg.norm(G,axis=1).reshape(G.shape[0], 1)
            khat = k/np.linalg.norm(k,axis=1).reshape(k.shape[0], 1)
            theta = np.arccos( np.sum( khat*ghat, axis=1) ) - (np.pi/2)
            wavelength = np.sin( theta ) * 2 * d
            intensity = xrays(wavelength)*f2
            if np.sum(intensity)==0: continue
            kscatter = 2*np.pi * khat / wavelength.reshape(khat.shape[0],1)
            kprime = G + kscatter
            dct_setup.add_rays(self.points, kprime, intensity)

    @property
    def rotation_angle(self, angle):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, angle):
        ang = angle - self._rotation_angle
        s, c = np.sin(ang), np.cos(ang)
        R = np.array([[c,-s,0],[s,c,0],[0,0,1]])
        self.points = R.dot( self.points.T ).T
        U = self._orientation.copy()
        for i in range(self._orientation.shape[0]):
            U[i,:,:] = R.dot(U[i,:,:])
        self.orientation = U
        self._rotation_angle = ang

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
