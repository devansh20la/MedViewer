import sys
import sip

sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)   

from PyQt4 import QtGui, QtCore
from scipy import io
import numpy as np
import finallll
import pyqtgraph as pg
import SimpleITK as sitk
import toberuined as code
from mayavi import mlab as ml
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

class inputdata():
    def __init__(self, loc):
        self.volume = np.load(str(loc))

    def marchingcube(self):
        self.verts, self.faces, self.normals, self.values = measure.marching_cubes(self.volume, step_size=3,gradient_direction='descent')

    def show(self, flag):
        ml.figure()
        if flag:
            ml.points3d(self.verts[:, 0], self.verts[:, 1], self.verts[:, 2], colormap="copper", scale_factor=0.5)
        else:
            ml.triangular_mesh([vert[0] for vert in self.verts], [vert[1] for vert in self.verts],
                               [vert[2] for vert in self.verts], self.faces)
        # ml.show()


class Window(QtGui.QMainWindow, finallll.Ui_MainWindow,inputdata):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.getimage.clicked.connect(self.getmatrix)
        self.TrainASM.clicked.connect(self.training)
        self.runASM.clicked.connect(self.checker)


    def getmatrix(self):
		name = QtGui.QFileDialog.getOpenFileName()
		temp = io.loadmat(str(name))
		# self.image_1 = inputdata(temp)
		self.target_image = temp['dataLib']['inputData'][0][0]
		self.diff_x.setImage(self.target_image.T,axes={'x':0, 'y':1, 't':2},xvals= np.linspace(0,np.shape(self.target_image)[0]-1))
		self.diff_y.setImage(self.target_image.T,axes={'x':2, 'y':0, 't':1},xvals= np.linspace(0,np.shape(self.target_image)[2]-1))
		self.diff_z.setImage(self.target_image.T,axes={'x':1, 'y':2, 't':0},xvals= np.linspace(0,np.shape(self.target_image)[1]-1))

    def training(self):
		filename = QtGui.QFileDialog.getOpenFileNames()
		print ("......Loading ref shape.........")
		# print (filename[0])
		data1 = code.inputdata(filename[0])
		data1.marchingcube()

		print ("...Initializing reference shape....")
		self.activeshape = code.shapemodels(data1)

		print ("......Loading entire dataset.........")

		DD = {}
		N = len(filename)

		temp = np.zeros((data1.verts.shape[0], (N - 1) * 3))

		for i in range(1, N):
		    DD[filename[i]] = code.inputdata(filename[i])
		    DD[filename[i]].marchingcube()
		    # print DD[filename[i]].verts.shape[0]
		    flag = 1
		    defboxrange = 10
		    while (flag==1):
		        temp[:, 3 * (i - 1):3 * (i - 1) + 3],flag = self.activeshape.correspondence(DD[filename[i]],defboxrange)
		        defboxrange = defboxrange + 2

		print("...Removing non corresponding points.....")
		idx = np.unique(np.argwhere(temp == 0)[:, 0])

		temp = np.delete(temp, idx, 0)
		X = np.reshape(temp, (-1, N-1), order='F')
		self.activeshape.initializeshapemodel(X)
		self.activeshape.show()

    def finalmatching(self,userpoint):
		# userpoint = (10,10,10)
		# temp = io.loadmat('/Users/devansh20la/Documents/Vision lab/Data/141225_Data for Poly/E10.5/E15.mat')
		# target_image = temp['dataLib']['inputData'][0][0]
		target = self.activeshape.matching(self.target_image, userpoint)

		# ml.figure('Segmentation PCA')
		self.result.visualization.scene.mlab.points3d(target[:, 0], target[:, 1], target[:, 2], colormap="copper", scale_factor=0.5)
		# ml.show()

    def checker(self):
		self.finalmatching((65.3884201, 72.77578735, 22.8884201))

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	# print GUI.image_1.input_volume[:,:,10]
	sys.exit(app.exec_())

run()
