import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    from lauesim import dct
    my_dct_model = dct.model()
    my_dct_model.collect()
    my_dct_model.show()