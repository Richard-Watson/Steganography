# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from stegPNG import steg, desteg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(321, 334)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ContainerNameLine = QtWidgets.QLineEdit(self.centralwidget)
        self.ContainerNameLine.setGeometry(QtCore.QRect(10, 40, 141, 20))
        self.ContainerNameLine.setObjectName("ContainerNameLine")
        self.ContainerNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.ContainerNameLabel.setGeometry(QtCore.QRect(10, 10, 141, 20))
        self.ContainerNameLabel.setScaledContents(False)
        self.ContainerNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ContainerNameLabel.setObjectName("ContainerNameLabel")
        self.FileNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.FileNameLabel.setGeometry(QtCore.QRect(10, 70, 141, 20))
        self.FileNameLabel.setScaledContents(False)
        self.FileNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FileNameLabel.setObjectName("FileNameLabel")
        self.FileNameLine = QtWidgets.QLineEdit(self.centralwidget)
        self.FileNameLine.setGeometry(QtCore.QRect(10, 100, 141, 20))
        self.FileNameLine.setObjectName("FileNameLine")
        self.PasswordLine = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordLine.setGeometry(QtCore.QRect(170, 40, 141, 20))
        self.PasswordLine.setObjectName("PasswordLine")
        self.PasswordLabel = QtWidgets.QLabel(self.centralwidget)
        self.PasswordLabel.setGeometry(QtCore.QRect(170, 10, 141, 20))
        self.PasswordLabel.setScaledContents(False)
        self.PasswordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 70, 141, 50))
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.PasswordLabel_Decode = QtWidgets.QLabel(self.centralwidget)
        self.PasswordLabel_Decode.setGeometry(QtCore.QRect(170, 170, 141, 20))
        self.PasswordLabel_Decode.setScaledContents(False)
        self.PasswordLabel_Decode.setAlignment(QtCore.Qt.AlignCenter)
        self.PasswordLabel_Decode.setObjectName("PasswordLabel_Decode")
        self.PasswordLine_Decode = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordLine_Decode.setGeometry(QtCore.QRect(170, 200, 141, 20))
        self.PasswordLine_Decode.setObjectName("PasswordLine_Decode")
        self.pushButton_Decode = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Decode.setGeometry(QtCore.QRect(170, 230, 141, 50))
        self.pushButton_Decode.setDefault(False)
        self.pushButton_Decode.setFlat(False)
        self.pushButton_Decode.setObjectName("pushButton_Decode")
        self.ContainerNameLabel_Decode = QtWidgets.QLabel(self.centralwidget)
        self.ContainerNameLabel_Decode.setGeometry(QtCore.QRect(10, 170, 141, 20))
        self.ContainerNameLabel_Decode.setScaledContents(False)
        self.ContainerNameLabel_Decode.setAlignment(QtCore.Qt.AlignCenter)
        self.ContainerNameLabel_Decode.setObjectName("ContainerNameLabel_Decode")
        self.ContainerNameLine_Decode = QtWidgets.QLineEdit(self.centralwidget)
        self.ContainerNameLine_Decode.setGeometry(QtCore.QRect(10, 200, 141, 20))
        self.ContainerNameLine_Decode.setObjectName("ContainerNameLine_Decode")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 321, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.DoSteg)
        self.pushButton_Decode.clicked.connect(self.Unsteg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Стеганография"))
        self.ContainerNameLabel.setText(_translate("MainWindow", "Название контейнера"))
        self.FileNameLabel.setText(_translate("MainWindow", "Название файла"))
        self.PasswordLabel.setText(_translate("MainWindow", "Пароль"))
        self.pushButton.setText(_translate("MainWindow", "Зашифровать"))
        self.PasswordLabel_Decode.setText(_translate("MainWindow", "Пароль"))
        self.pushButton_Decode.setText(_translate("MainWindow", "Расшифровать"))
        self.ContainerNameLabel_Decode.setText(_translate("MainWindow", "Название контейнера"))

    def DoSteg(self):
        if (self.ContainerNameLine.text() and
            self.FileNameLine.text() and
            not self.PasswordLine.text()):
                steg(self.ContainerNameLine.text(),
                     self.FileNameLine.text(),
                     UseCryptography=False)
        elif (self.ContainerNameLine.text() and
            self.FileNameLine.text() and
            self.PasswordLine.text()):
                steg(self.ContainerNameLine.text(),
                     self.FileNameLine.text(),
                     CryptoPassword=self.PasswordLine.text())

    def Unsteg(self):
        if self.ContainerNameLine_Decode.text() and not self.PasswordLine_Decode.text():
            desteg(self.ContainerNameLine_Decode.text(),
                   UseCryptography=False)
        elif self.ContainerNameLine_Decode.text() and self.PasswordLine_Decode.text():
            desteg(self.ContainerNameLine_Decode.text(),
                   CryptoPassword=self.PasswordLine_Decode.text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

