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


class shapemodels():
    def __init__(self, data):
        self.refverts = data.verts
        self.reffaces = data.faces
        self.refnormals = data.normals
        self.refvalues = data.values
        self.final = ht(data.verts)

    def show(self):
        ml.figure()
        temp = self.meanshape
        temp = np.reshape(temp, (-1, 3), order='F')
        ml.points3d(temp[:, 0], temp[:, 1], temp[:, 2], colormap="copper", scale_factor=0.5)

    # ml.show()

    def correspondence(self,data,defboxrange):

        print ("....Shape context.....")
        final = self.final
        final1 = ht(data.verts)

        print("...........Matching............")

        points1 = np.argwhere(final[:, :, :, 0] == 1)
        points2 = np.argwhere(final1[:, :, :, 0] == 1)

        newpoints = []
        threshold = 600
        costhist = []
        lowenergy = 0
        highenergy = 0

        for point in points1:
            prevcost = 1e5
            histogram = np.delete(final[point[0], point[1], point[2], :], 0)
            boxrange = final1[point[0]-defboxrange:point[0] + defboxrange+1, point[1] - defboxrange:point[1] + defboxrange+1, point[2] - defboxrange:point[2] + defboxrange+1, :]
            allmatches = np.argwhere(boxrange[:, :, :, 0] == 1)
            # print len(allmatches)
            if len(allmatches)>0:
                for targetpoint in allmatches:
                    matchedhisto = np.delete(boxrange[targetpoint[0], targetpoint[1], targetpoint[2], :], 0)
                    cost = ctfunc(histogram, matchedhisto)
                    if cost < prevcost:
                        matchedpoint = targetpoint + point - (defboxrange, defboxrange, defboxrange)
                        prevcost = cost
                
                costhist.append(prevcost)
                if prevcost < threshold:
                    newpoints.append(matchedpoint)
                    lowenergy = lowenergy + 1
                else:
                    newpoints.append((0, 0, 0))
                    highenergy = highenergy + 1
            else:
                newpoints.append((0,0,0))            

        # plt.figure()
        # plt.hist(costhist)
        if (highenergy/(lowenergy + highenergy)) > 0.5:
            flag = 1
        else:
            flag = 0
        # print flag
        return np.array(newpoints),flag


    def initializeshapemodel(self, data):
        self.shapeparams, self.meanshape, self.eigenvectors = pcup(data)


    def matching(self, target_image, userpoint):
        dx, dy, dz = np.gradient(target_image)
        grad_mag = np.sqrt(np.square(dx) + np.square(dy) + np.square(dz))
        grad_mag = np.abs(grad_mag)
        reconshape = self.meanshape
        verts = np.reshape(reconshape, (-1, 3), order='F')
        verts = verts + userpoint

        target_points = np.zeros((verts.shape[0], verts.shape[1]))
        p, q, r = np.shape(target_image)
        boxrange = np.array([3, 3, 3])

        print("..........Matching Target Points.......")
        for l in range(0, verts.shape[0]):
            change = -10;
            new_point = (verts[l, :]).astype(np.int)
            if new_point[0] >= p: new_point[0] = p - 1
            if new_point[1] >= q: new_point[1] = q - 1
            if new_point[2] >= r: new_point[2] = r - 1
            if new_point[0] < 0: new_point[0] = 0
            if new_point[1] < 0: new_point[1] = 0
            if new_point[2] < 0: new_point[2] = 0
            box = grad_mag[new_point[0] - 3:new_point[0] + 4, new_point[1] - 3:new_point[1] + 4,
                  new_point[2] - 3:new_point[2] + 4]
            i, j, k = np.unravel_index(box.argmax(), box.shape)
            target_points[l, :] = (i, j, k) + verts[l, :] - boxrange

        return target_points

# print ("......Loading ref shape.........")

# location = '/Users/devansh20la/Documents/Vision lab/mydata/'
# filename = ['E14.npy', 'E16.npy','E15.npy', 'E18.npy', 'E19.npy', 'E35.npy', 'E36.npy', 'E37.npy']

# data1 = inputdata(str(location) + str(filename[0]))
# data1.marchingcube()
# print data1.verts.shape[0]

# data2 = inputdata(str(location) + str(filename[2]))
# data2.marchingcube()

# print ("...Initializing reference shape....")
# activeshape = shapemodels(data1)

# print ("......Loading entire dataset.........")

# DD = {}
# N = len(filename)

# temp = np.zeros((data1.verts.shape[0], (N - 1) * 3))

# for i in range(1, N):
#     DD[filename[i]] = inputdata(str(location) + str(filename[i]))
#     DD[filename[i]].marchingcube()
#     print DD[filename[i]].verts.shape[0]
#     flag = 1
#     defboxrange = 10
#     while (flag==1):
#         temp[:, 3 * (i - 1):3 * (i - 1) + 3],flag = activeshape.correspondence(DD[filename[i]],defboxrange)
#         defboxrange = defboxrange + 2




# # print("...Removing non corresponding points.....")
# # idx = np.unique(np.argwhere(temp == 0)[:, 0])

# # temp = np.delete(temp, idx, 0)
# # X = np.reshape(temp, (-1, N-1), order='F')

# # if maxpoints<DD[filename[i]].verts.shape[0]:
# # 	maxpoints = DD[filename[i]].verts.shape[0]
# # if minpoints>DD[filename[i]].verts.shape[0]:
# # 	minpoints = DD[filename[i]].verts.shape[0]


# # X = np.zeros((3*data1.verts.shape[0],N-1))

# # for i in range(1,N):
# # 	temp = DD[filename[i]].verts
# # 	temp = temp - np.mean(temp,axis=0)
# # 	temp = np.reshape(temp,(-1,1))
# # 	X[0:temp.shape[0],i-1] = temp[:,0]

# # for i in range(3*minpoints,3*maxpoints):
# # 	idx = np.argwhere(X[i,:]==0)
# # 	nidx = np.argwhere(X[i,:]!=0)
# # 	mn = np.mean(X[i,nidx])
# # 	X[i,idx] = mn



# # activeshape.initializeshapemodel(X)
# # activeshape.show()

# # # b = activeshape.shapeparams
# # userpoint = (10,10,10)dat
# # temp = io.loadmat('/Users/devansh20la/Documents/Vision lab/Data/141225_Data for Poly/E10.5/E15.mat')
# # target_image = temp['dataLib']['inputData'][0][0]
# # target = activeshape.matching(target_image, userpoint)
# # np.save('target',target)

# # ml.figure('Segmentation PCA')
# # # # ml.triangular_mesh([vert[0] for vert in target],[vert[1] for vert in target],[vert[2] for vert in target],data1.faces) 
# # ml.points3d(target[:, 0], target[:, 1], target[:, 2], colormap="copper", scale_factor=0.5)
# # # activeshape.show(1,faces=None)
# # ml.show()
# # plt.show()
# # activeshape.show(1,faces = None)
# # data1 = inputdata(str(location) + str(filename[1]))

# # print ("...Updating parameters.....")
# # activeshape.updateparamas(data1)
# # activeshape.updateparamas(data1)
