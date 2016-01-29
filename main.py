import sys
from GUI import *
from PyQt5 import QtCore, QtGui, QtWidgets
from stegPNG import steg, desteg

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.DoSteg)
        self.ui.pushButton_Decode.clicked.connect(self.Unsteg)

    def DoSteg(self):
        if (self.ui.ContainerNameLine.text() and
                self.ui.FileNameLine.text() and
                not self.ui.PasswordLine.text()):
            steg(self.ui.ContainerNameLine.text(),
                 self.ui.FileNameLine.text())
        elif (self.ui.ContainerNameLine.text() and
                  self.ui.FileNameLine.text() and
                  self.ui.PasswordLine.text()):
            steg(self.ui.ContainerNameLine.text(),
                 self.ui.FileNameLine.text(),
                 CryptoPassword=self.ui.PasswordLine.text(),
                 UseCryptography=True)

    def Unsteg(self):
        if (self.ui.ContainerNameLine_Decode.text() and
                not self.ui.PasswordLine_Decode.text()):
            desteg(self.ui.ContainerNameLine_Decode.text())
        elif (self.ui.ContainerNameLine_Decode.text() and
                  self.ui.PasswordLine_Decode.text()):
            desteg(self.ui.ContainerNameLine_Decode.text(),
                   CryptoPassword=self.PasswordLine_Decode.text(),
                   UseCryptography=True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())