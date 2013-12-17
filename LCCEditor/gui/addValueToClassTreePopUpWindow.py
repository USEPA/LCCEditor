'''
    Created on Aug 30, 2013

    Last Modified 9/30/13

'''

import PySide
from PySide import QtCore, QtGui
from PySide.QtGui import *
import pylet
from inspect import stack

class AddValueToClassTreePopUpWindow(QDialog):
    '''
    classdocs
    '''

    def __init__(self,main):
        '''
        Constructor
        '''
        # initialize the class from the super class
        super(AddValueToClassTreePopUpWindow,self).__init__()

        self.main = main
        # create layout
        self.layout=QGridLayout()                   # create a grid widget
        self.layout.setSpacing(10)                  # set the spacing between widgets

        # Create widgets and add them to the layout

        # -- valueId Widget
        # ---- create IntValidator widget
        # -- class filter widget
        targetString  = "The class you have selected is " + self.main.selectedClass.text(0).upper()
        self.targetClassMessage = QLabel(targetString)
        self.valueAddedToClassLabel = QLabel("Current List of Values")         # create class Id name label widget
        self.valueAddedToClassSelectionField = QListWidget()
        #tempcont = []
        #for number in self.main.tempLccObj.values.keys():
        #   tempcont.append(str(number))
        
        # create a list that we can remove the items already included and excluded.
        includedList = []
        excludedList = []
        excludedList.extend(self.main.tempLccObj.classes[self.main.selectedClass.text(0)].getValueIds())

        for excludedKeys in self.main.tempLccObj.values.keys():
            if self.main.tempLccObj.values[excludedKeys].excluded:
                excludedList.append(self.main.tempLccObj.values[excludedKeys].valueId)
        
        for value in self.main.tempLccObj.values.keys():
            if not value in excludedList:
                includedList.append(value)
        
        idList = list(includedList)
        idList.sort()
        
        self.valueAddedToClassSelectionField.addItems(map(str,idList))
        self.valueAddedToClassSelectionField.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)

        self.layout.addWidget(self.targetClassMessage, 0, 0)
        self.layout.addWidget(self.valueAddedToClassLabel, 2, 0)      # add class Id name label widget to layout
        self.layout.addWidget(self.valueAddedToClassSelectionField, 2, 1)    # add class Idd name field widget to layout

        # -- create ok and cancel buttons widget
        self.okButton = QPushButton('OK')
        self.cancelButton = QPushButton('Cancel')

        # -- connect ok and cancel buttons to their event handlers
        self.okButton.clicked.connect(self.okButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

        #self.okButton.clicked.connect(self.wakeup)
        # -- create a new layout view for buttons
        self.buttonBox = QHBoxLayout()                  # create a QHBoxLayout object
        self.buttonBox.addStretch(1)                    # set stretch requirements
        self.buttonBox.addWidget(self.okButton)         # add ok Button to interface
        self.buttonBox.addWidget(self.cancelButton)     # add cancel button to interface

        # add ok and cancel buttons to UI layout
        self.layout.addLayout(self.buttonBox, 6, 1)
        self.setLayout(self.layout)

        #set the window size and title. Then display the UI window (left, top, width, height)
        self.setGeometry(500, 300, 350, 150)
        self.setWindowTitle(self.main.dialogTitle)      # set title of popup window
        
        self.logProgress("**** addValueToClassTreePopUpWindow ****")

    def okButtonClicked(self):
#        convertList = []
        self.logProgress(stack()[0][3])
 
        for selItem in self.valueAddedToClassSelectionField.selectedItems():
            self.main.dialogVariable.append(int(selItem.text()))
        
        self.accept()

        self.logProgress(stack()[0][3] + " END")
    
    def cancelButtonClicked(self):
        self.logProgress(stack()[0][3])

        self.close()

        self.logProgress(stack()[0][3] + " END")
   
    def logProgress(self, message):
        logFile = open("log.lfn",'a')
        logFile.write(message + "\n")
        logFile.close()
      