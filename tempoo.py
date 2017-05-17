import numpy as np
from scipy import io
from skimage import measure
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from mayavi import mlab as ml

import vtk
from vtk.util import numpy_support

import SimpleITK as sitk

from shapecontext import histogram as ht
from time import time

from ipywidgets import interact, fixed
from mypca import pcaupdate as pcup
from histcost import costfunction as ctfunc

def rigid_registration(fixed_image, moving_image):
    fixed_image = sitk.GetImageFromArray(fixed_image)
    moving_image = sitk.GetImageFromArray(moving_image)

    initial_transform = sitk.CenteredTransformInitializer(fixed_image, moving_image, sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)
    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)

    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=500,
                                                      convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=True)
    final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                  sitk.Cast(moving_image, sitk.sitkFloat32))
    moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0,
                                     moving_image.GetPixelID())

    return sitk.GetArrayFromImage(moving_resampled)

print ("......Loading ref shape.........")

location = '/Users/devansh20la/Documents/Vision lab/Data/141225_Data for Poly/E10.5/'
filename = ['E14.mat','E16.mat', 'E15.mat', 'E18.mat', 'E19.mat', 'E35.mat', 'E36.mat', 'E37.mat']
temp = io.loadmat(str(location) + str(filename[0]))
# temp1 = io.loadmat(str(location) + str(filename[1]))

input_image = temp['dataLib']['inputData'][0][0]
input_volume = np.array(temp['dataLib']['groundTruth'][0][0]==1,dtype='float32')

# input_image1 = temp1['dataLib']['inputData'][0][0]
# input_volume1 = np.array(temp1['dataLib']['groundTruth'][0][0]==1,dtype='float32')

# newvolume = rigid_registration(fixed_image=input_volume, moving_image=input_volume1)
# name = '/Users/devansh20la/Documents/Vision lab/mydata/' + str('E14')

# targets = np.load('target.npy')
# io.savemat('target.mat',{'foo': targets})

verts, faces, normals, values = measure.marching_cubes(input_volume, spacing=(1,1,1), step_size=3, gradient_direction='descent')
# verts1, faces1, normals1, values1 = measure.marching_cubes(newvolume, spacing = (1,1,1), step_size=3, gradient_direction='descent')

io.savemat('imagepoints.mat',{'foo':verts})
# print np.mean(verts,axis=0)
# print verts1.shape[0]




