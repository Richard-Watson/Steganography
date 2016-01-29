import sys
from GUI import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.DoSteg)
        self.ui.pushButton_Decode.clicked.connect(self.Unsteg)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())