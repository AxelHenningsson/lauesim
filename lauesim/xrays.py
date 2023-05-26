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


if __name__ == "__main__":
    pass