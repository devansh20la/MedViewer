# MedViewer
Medical Image segmentation using active shape models on high frequency ultrasound data. The algorithm performs training as well as segmentation of Brain Ventricle of mouse embryo from high frequency ultrasound images. We use simple ITK to perform registration of images and save the registration results, the further processing is performed on the saved dataset. I cannot post the dataset for obvious reaons. The program also contains a graphical user interface over the entire algorithm.

Steps to run the codes:
1) Install all the dependencies listed below. If you are using conda make sure to create a new environment to prevent the library conflicts.
  
from PyQt4 import QtGui, QtCore \
from scipy import io \
import numpy as np \
import pyqtgraph as pg \
import SimpleITK as sitk \
from mayavi import mlab as ml \
from pyface.qt import QtGui, QtCore \
from traits.api import HasTraits, Instance, on_trait_change \
from traitsui.api import View, Item \
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor \

2) Perform registration of the dataset on any reference image from the dataset and save the results using initial_registration.py (Since my dataset was arranged as dictionary of dictionary you might need to change the loading function)

3) Run GUI.py to run the graphical user interface and follow the buttons. A brief description of each button is provided below:
  3a) Train ASM: Select the pre registered training ground truth label with the first selection as the reference image. The       mean shape obtained after training is shown as a pop-up. Please note you need to close the figure to prevent the GUI         from plotting the final result on the same figure. (The step assumes dataset is saved a numpy array)
  3b) Get Image: Select the target image or testing image.
  3c) ASM requires a very good initialization and the intial centroid must be defined inside function_class.py->matching:         boxrange.
  3d) Click on run ASM

4) Additional features of the GUI:
  4a) Use the slider below each widget to change slices in each direction.
  4b) Use the horizontal slider to adjust lower and upper thresholding values.

Thank you 

<img width="968" alt="img" src="https://cloud.githubusercontent.com/assets/16810812/26176559/8c7494ea-3b24-11e7-859b-21df6130ffb4.png">
