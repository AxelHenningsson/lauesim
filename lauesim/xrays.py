import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



class xrays(object):

    def __init__(self, intensity, wavelength):
        self.intensity  = intensity
        self.wavelength = wavelength
        self.f = interp1d(wavelength, intensity, kind='linear', fill_value=0, bounds_error=False)

    def __call__(self, lamdas):
        return self.f(lamdas)
    
    def show_spectrum(self):
        plt.figure(figsize=(10,5))
        plt.title('X-ray Spectrum')
        E = self.wavelength_to_energy(self.wavelength)
        plt.plot( E, self.intensity, 'ko--')
        plt.xlabel('Photon Energy [keV]')
        plt.ylabel('Relative Intensity  [-]')
        plt.grid('on')
        plt.show()

    def wavelength_to_energy(self, wavelength):
        h        = 6.62607015 * 10**(-34)
        keV      = 1.60217663 * 10**(-16)
        c        = 299792458
        angstrom = 10**(-10)
        E = (h*c / keV) / ( wavelength * angstrom )
        return E


if __name__ == "__main__":
    pass