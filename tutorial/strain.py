import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation
import cProfile
import pstats
from lauesim import dct

if __name__ == "__main__":
    my_dct_model = dct.model()
    N = my_dct_model.sample.points.shape[0]

    print("Diffraction computations:")
    pr = cProfile.Profile()
    pr.enable()
    my_dct_model.sample.orientation = Rotation.random(N).as_matrix()
    my_dct_model.sample.rotation_angle = np.pi/4.
    my_dct_model.collect()
    pr.disable()
    pr.dump_stats('tmp_profile_dump')
    ps = pstats.Stats('tmp_profile_dump').strip_dirs().sort_stats('cumtime')
    ps.print_stats(15)
    print("")

    #my_dct_model.xray.show_spectrum()
    my_dct_model.show_frame()