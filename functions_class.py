import numpy as np
from scipy import io
from skimage import measure
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab as ml
import SimpleITK as sitk
from shapecontext import histogram as ht
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