from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
from pyqtgraph import ImageView
import mayavi_widget as hl

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(964, 708)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.getimage = QtGui.QPushButton(self.centralwidget)
        self.getimage.setGeometry(QtCore.QRect(50, 120, 110, 32))
        self.getimage.setObjectName("getimage")

        self.diff_y = ImageView(self.centralwidget)
        self.diff_y.setGeometry(QtCore.QRect(590, 10, 351, 301))
        self.diff_y.setObjectName("diff_y")

        self.diff_z = ImageView(self.centralwidget)
        self.diff_z.setGeometry(QtCore.QRect(190, 340, 371, 331))
        self.diff_z.setObjectName("diff_z")

        self.result = hl.MayaviQWidget(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(589, 339, 351, 361))
        self.result.setObjectName("widget")

        self.diff_x = ImageView(self.centralwidget)
        self.diff_x.setGeometry(QtCore.QRect(190, 10, 371, 311))
        self.diff_x.setObjectName("diff_x")

        self.runASM = QtGui.QPushButton(self.centralwidget)
        self.runASM.setGeometry(QtCore.QRect(50, 250, 110, 32))
        self.runASM.setObjectName("runASM")

        self.TrainASM = QtGui.QPushButton(self.centralwidget)
        self.TrainASM.setGeometry(QtCore.QRect(50, 80, 113, 32))
        self.TrainASM.setObjectName("TrainASM")

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 20))

        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 30, 111, 16))

        self.label_2.setObjectName("label_2")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 220, 118, 23))

        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 160, 113, 32))
        self.pushButton.setObjectName("pushButton")

        self.diff_x.raise_()
        self.getimage.raise_()
        self.diff_y.raise_()
        self.diff_z.raise_()

        self.result.raise_()
        #mayavi_widget = MayaviQWidget(container)

#     layout.addWidget(mayavi_widget, 1, 1)

        self.runASM.raise_()
        self.TrainASM.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.progressBar.raise_()
        self.pushButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.getimage.setText(_translate("MainWindow", "Get Image"))
        self.runASM.setText(_translate("MainWindow", "Run ASM"))
        self.TrainASM.setText(_translate("MainWindow", "TrainASM"))
        self.label.setText(_translate("MainWindow", "MedViewer"))
        self.label_2.setText(_translate("MainWindow", "Devansh"))
        self.pushButton.setText(_translate("MainWindow", "Select Point"))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

