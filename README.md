# L A U E S I M
Barebones simulation of diffraction from crystals using divergent chromatic X-rays and flat detectors.

**NOTE:** *This is a toy sientific project to gain a better understanding of the so called Laue Diffraction geometry in which a divergent and white beam of X-rays is allowed to illuminate a polycrytsal giving rise to diffraction that is recorded on a flat 2d area detector. Use it to learn about diffraction and have fun!*

# Example
----------

```python
    from lauesim import dct
    my_dct_model = dct.model()
    my_dct_model.collect()
    my_dct_model.show()
```
![laue](https://github.com/AxelHenningsson/lauesim/assets/31615210/0c40da89-5277-4435-a978-78da331fd234)
The default model features a single 0.5mm diameter single crystal of aplha quartz. The model parameters can be tweaked trhough attributes of the components. FOr instance to rotate the sample do:
```python
    my_dct_model.sample.rotation_angle = np.pi/2.
    my_dct_model.collect()
    my_dct_model.show_frame()
```
This then gives a different diffraction pattern
![image](https://github.com/AxelHenningsson/lauesim/assets/31615210/4ecb3c77-2744-440d-bc29-14c09c38e326)

# Installation
----------
Clone the repo and go to the root

    git clone https://github.com/AxelHenningsson/lauesim.git
    cd lauesim

Create a new pip environment and install

    python3 -m venv env
    pip install -e .
