# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogUI_1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt5 import QtCore, QtGui, QtWidgets


# Add here more keys for extra functionality. 
myInputs = {"float":{"class":QtWidgets.QLineEdit,"getValue":"text","validator":QtGui.QDoubleValidator,"setValue":"setText"},
            "int":{"class":QtWidgets.QLineEdit,"getValue":"text","validator":QtGui.QIntValidator,"setValue":"setText"},
            "str":{"class":QtWidgets.QLineEdit,"getValue":"text","setValue":"setText"},
            "bool":{"class":QtWidgets.QCheckBox,"getValue":"isChecked","setValue":"setChecked"},
            "item":{"class":QtWidgets.QComboBox,"getValue":"currentText","setValue":"setCurrentText"}
            }

class GenericDynamicDialog(QtWidgets.QDialog):
    r"""
    
    """
    
    def __init__(self, argumentsDict=dict(), title="Generic Dynamic Dialog", parent=None):
        super(GenericDynamicDialog, self).__init__()
        
        self.argumentsDict = argumentsDict
        self.windowTitle = title
        
        self.setupUi(self)
        
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.setObjectName("Dialog")
        self.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 251))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.argumentUI = {}
        for iArgumentName, iArgumentSettings in self.argumentsDict.items():
            # Create a holding place for all the graphical elements
            self.argumentUI[iArgumentName] = {}
            # Each argument should be placed in its own horizontal layout
            self.argumentUI[iArgumentName]["horizontalLayout"] = QtWidgets.QHBoxLayout()
            self.argumentUI[iArgumentName]["horizontalLayout"].setObjectName("horizontalLayout_{}".format(iArgumentName))
            # Create argument label
            self.argumentUI[iArgumentName]["label"] = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.argumentUI[iArgumentName]["label"].setObjectName("label_{}".format(iArgumentName))
            self.argumentUI[iArgumentName]["label"].setText(iArgumentSettings["label"])
            self.argumentUI[iArgumentName]["horizontalLayout"].addWidget(self.argumentUI[iArgumentName]["label"])
            # Create an appropiate argument widget
            self.argumentUI[iArgumentName]["input"] = myInputs[iArgumentSettings["type"]]["class"](self.scrollAreaWidgetContents)
            # If necesary, add a validator
            if "validator" in myInputs[iArgumentSettings["type"]]:
                self.argumentUI[iArgumentName]["input"].setValidator(myInputs[iArgumentSettings["type"]]["validator"]())
            # If necessary, fill the combobox
            if iArgumentSettings["type"] == "item":
                self.argumentUI[iArgumentName]["input"].addItems(iArgumentSettings["items"])
            self.argumentUI[iArgumentName]["input"].setObjectName("input_{}".format(iArgumentName))
            self.argumentUI[iArgumentName]["horizontalLayout"].addWidget(self.argumentUI[iArgumentName]["input"])
            # Add the argument's horizontal layout to the vertical layout of the scroll area
            self.verticalLayout_2.addLayout(self.argumentUI[iArgumentName]["horizontalLayout"])
            
            
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.setWindowTitle(self.windowTitle)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


    def getAnswers(self):
        result = {}
        for iArgumentName, iArgumentSettings in self.argumentsDict.items():
            result[iArgumentName] = getattr(self.argumentUI[iArgumentName]["input"],myInputs[iArgumentSettings["type"]]["getValue"])()
        return result
    
    def setAnswers(self, preFill):
        for iArgumentName, iArgumentValue in preFill.items():
            iArgumentSettings = self.argumentsDict[iArgumentName]
            getattr(self.argumentUI[iArgumentName]["input"],myInputs[iArgumentSettings["type"]]["setValue"])(iArgumentValue)


if __name__ == '__main__':
    myArguments = {"err":{"type":"float","range":[0,None],"label":"Error"},
               "mean":{"type":"float","range":[0,None],"label":"Mean"},
               "complete":{"type":"bool","label":"Complete"},
               "port":{"type":"item","label":"Port","items":["Port A", "Port B", "Port C"]}}
    
    app = QtWidgets.QApplication(sys.argv)
    window = GenericDynamicDialog(myArguments)
    window.show()
    sys.exit(app.exec_())