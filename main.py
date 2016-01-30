import sys
import os
from UI import *
from PyQt5 import QtWidgets
from Steganography import steg, desteg
from Converter import ConvertToPNG

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Связываем объекты с действиями
        self.ui.Encode_Container_ToolButton.clicked.connect(self.Encode_Container_Choose)
        self.ui.Encode_InputFile_ToolButton.clicked.connect(self.Encode_InputFile_Choose)
        self.ui.Encode_Password_pushButton.clicked.connect(self.Encode_Start)

        self.ui.Decode_Container_ToolButton.clicked.connect(self.Decode_Container_Choose)
        self.ui.Decode_Password_pushButton.clicked.connect(self.Decode_Start)

        self.ui.Converter_Container_ToolButton.clicked.connect(self.Converter_Path_Choose)
        self.ui.Converter_pushButton.clicked.connect(self.Convert_Start)

    def Encode_Container_Choose(self):
        self.ui.Encode_Container_LineEdit.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0])
    def Encode_InputFile_Choose(self):
        self.ui.Encode_InputFile_LineEdit.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0])
    def Decode_Container_Choose(self):
        self.ui.Decode_Container_LineEdit.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0])
    def Converter_Path_Choose(self):
        self.ui.Converter_Container_LineEdit.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0])


    def Convert_Start(self):
        if self.ui.Converter_Container_LineEdit.text():
            ConvertToPNG(self.ui.Converter_Container_LineEdit.text())
    def Encode_Start(self):
        if (self.ui.Encode_Container_LineEdit.text() and
                self.ui.Encode_InputFile_LineEdit.text() and
                not self.ui.Encode_Password_LineEdit.text()):
            steg(self.ui.Encode_Container_LineEdit.text(),
                 self.ui.Encode_InputFile_LineEdit.text(),
                 UseCryptography=False)
        elif (self.ui.Encode_Container_LineEdit.text() and
                  self.ui.Encode_InputFile_LineEdit.text() and
                  self.ui.Encode_Password_LineEdit.text()):
            steg(self.ui.Encode_Container_LineEdit.text(),
                 self.ui.Encode_InputFile_LineEdit.text(),
                 CryptoPassword=self.ui.Encode_Password_LineEdit.text(),
                 UseCryptography=True)
    def Decode_Start(self):
        if (self.ui.Decode_Container_LineEdit.text() and
                not self.ui.Decode_Password_LineEdit.text()):
            desteg(self.ui.Decode_Container_LineEdit.text(),
                   UseCryptography=False)
        elif (self.ui.Decode_Container_LineEdit.text() and
                  self.ui.Decode_Password_LineEdit.text()):
            desteg(self.ui.Decode_Container_LineEdit.text(),
                   CryptoPassword=self.ui.Decode_Password_LineEdit.text(),
                   UseCryptography=True)

#Комментарии
#Помощник

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())