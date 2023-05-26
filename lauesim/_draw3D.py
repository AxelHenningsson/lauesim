import vtk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle
from vtkmodules.vtkCommonColor import vtkNamedColors
from PIL import Image
from scipy.ndimage import zoom
from matplotlib.image import imsave

def draw( image, setup, sample ):


    renderer = vtk.vtkRenderer()
    x0,y0,z0 = setup.source

    if 1 :
        for point in sample.points:

            # Incident Rays
            x,y,z = point
            ray_source = vtk.vtkLineSource()
            ray_source.SetPoint1(x0,y0,z0)
            ray_source.SetPoint2(x,y,z)
            ray_mapper = vtk.vtkPolyDataMapper()
            ray_mapper.SetInputConnection(ray_source.GetOutputPort())
            ray_actor = vtk.vtkActor()
            property = ray_actor.GetProperty()
            property.SetLineWidth(2)
            property.SetColor(55/255., 0, 155/255.)
            property.SetOpacity(0.1)
            ray_actor.SetMapper(ray_mapper)
            renderer.AddActor(ray_actor)

            # Sample
            voxel = vtk.vtkCubeSource()
            voxel.SetXLength(50)
            voxel.SetYLength(50)
            voxel.SetZLength(50)
            voxel.SetCenter(x,y,z)
            voxel_mapper = vtk.vtkPolyDataMapper()
            voxel_mapper.SetInputConnection(voxel.GetOutputPort())
            voxel_actor = vtk.vtkActor()
            voxel_actor.SetMapper(voxel_mapper)
            voxel_property = vtk.vtkProperty()
            voxel_property.SetColor(0.1,0.3,0.3)
            voxel_property.SetOpacity(0.4)
            voxel_actor.SetProperty(voxel_property)
            renderer.AddActor(voxel_actor)

        
    # The Detector
    detector = vtk.vtkCubeSource()
    detector.SetXLength(setup.pixelsize*setup.detector_shape[0]/100.)
    detector.SetYLength(2*np.abs(setup.d0[1]))
    detector.SetZLength(2*np.abs(setup.d0[2]))
    detector.SetCenter(setup.d0[0],0,0)
    detector_mapper = vtk.vtkPolyDataMapper()
    detector_mapper.SetInputConnection(detector.GetOutputPort())
    detector_actor = vtk.vtkActor()
    detector_actor.SetMapper(detector_mapper)
    detector_property = vtk.vtkProperty()
    detector_property.SetColor(0.99, 0.99, 0.99)
    detector_property.SetOpacity(1.0)
    detector_actor.SetProperty(detector_property)

    array = image.copy()
    array = np.ascontiguousarray(array)

    imsave('imrot.png', array, cmap='gray_r')
    reader = vtk.vtkPNGReader()
    reader.SetFileName("imrot.png")
    reader.Update()
    texture = vtk.vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())
    texture.SetInterpolate(10)
    transform = vtk.vtkTransform()
    dd = 0.000038
    transform.Scale(dd, dd, 1.0)
    dx = setup.pixelsize*setup.detector_shape[0]
    dy = setup.pixelsize*setup.detector_shape[1]
    transform.Translate(dx*0.51, dy*0.51, 0)
    texture.SetTransform( transform  )
    #texture.Update()
    detector_actor.SetTexture(texture)
    renderer.AddActor(detector_actor)


    # Beam stop
    beamstop = vtk.vtkCubeSource()
    beamstop.SetXLength(setup.pixelsize*setup.detector_shape[0]/50.)
    beamstop.SetYLength(setup.beamstop_shape[0]*setup.pixelsize)
    beamstop.SetZLength(setup.beamstop_shape[1]*setup.pixelsize)
    beamstop.SetCenter(setup.d0[0]*0.95, 0, 0)
    beamstop_mapper = vtk.vtkPolyDataMapper()
    beamstop_mapper.SetInputConnection(beamstop.GetOutputPort())
    beamstop_actor = vtk.vtkActor()
    beamstop_actor.SetMapper(beamstop_mapper)
    beamstop_property = vtk.vtkProperty()
    beamstop_property.SetColor(0.4, 0.4, 0.4)
    beamstop_property.SetOpacity(0.999)
    beamstop_actor.SetProperty(beamstop_property)
    renderer.AddActor(beamstop_actor)


    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1200, 700)
    renderWindow.SetMultiSamples(150)
    renderWindow.SetPosition(450,-950)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    interactor.Initialize()
    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)
    colors = vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("LightSlateGray"))
    renderWindow.AddRenderer(renderer)
    renderWindow.Render()
    interactor.Start()
