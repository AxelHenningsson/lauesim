import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation

if __name__ == "__main__":
    from lauesim import dct
    my_dct_model = dct.model()
    N = my_dct_model.sample.points.shape[0]
    my_dct_model.sample.orientation = Rotation.random(N).as_matrix()
    my_dct_model.sample.rotation_angle = np.pi/4.
    my_dct_model.collect()
    my_dct_model.xray.show_spectrum()
    my_dct_model.show_frame()