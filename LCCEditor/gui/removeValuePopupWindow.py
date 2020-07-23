'''
    Created on Aug 19, 2013

    Last Modified 9/30/13

'''
import PySide
from PySide import QtCore, QtGui
#from PySide.QtGui import *
from inspect import stack

class RemoveValuePopupWindow(QtGui.QDialog):
    '''
    classdocs
    '''   

    def __init__(self,main):
        '''
        Constructor
        '''
        # initialize the class from the super class

        super(RemoveValuePopupWindow,self).__init__()

        self.main = main
        # create layout
        self.layout= QtGui.QGridLayout()                   # create a grid widget
        self.layout.setSpacing(10)                  # set the spacing between widgets

        # Create widgets and add them to the layout

        # -- valueId Widget
        # ---- create IntValidator widget
        # -- class filter widget
        self.idRemoveLabel = QtGui.QLabel("Current List of Values")         # create class Id name label widget
        self.idRemoveSelectionField = QtGui.QListWidget()
        #tempcont = []
        #for number in self.main.tempLccObj.values.keys():
        #   tempcont.append(str(number))
        
        idList = list(self.main.tempLccObj.values.keys())
        idList.sort()
        
        self.idRemoveSelectionField.addItems(map(str,idList))
        self.idRemoveSelectionField.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)

        self.layout.addWidget(self.idRemoveLabel, 0, 0)      # add class Id name label widget to layout
        self.layout.addWidget(self.idRemoveSelectionField, 0, 1)      # add class Idd name field widget to layout

        # -- create ok and cancel buttons widget
        self.okButton = QtGui.QPushButton('OK')
        self.cancelButton = QtGui.QPushButton('Cancel')

        # -- connect ok and cancel buttons to their event handlers
        self.okButton.clicked.connect(self.okButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

        #self.okButton.clicked.connect(self.wakeup)
        # -- create a new layout view for buttons
        self.buttonBox = QtGui.QHBoxLayout()                  # create a QHBoxLayout object
        self.buttonBox.addStretch(1)                    # set stretch requirements
        self.buttonBox.addWidget(self.okButton)         # add ok Button to interface
        self.buttonBox.addWidget(self.cancelButton)     # add cancel button to interface

        # add ok and cancel buttons to UI layout
        self.layout.addLayout(self.buttonBox, 6, 1)
        self.setLayout(self.layout)

        #set the window size and title. Then display the UI window (left, top, width, height)
        self.setGeometry(500, 300, 350, 150)
        self.setWindowTitle(self.main.dialogTitle)      # set title of popup window
        
        self.logProgress("**** removeValuePopupWindow ****")
        
    def okButtonClicked(self):
#        convertList = []
        self.logProgress(stack()[0][3])
 
        for selItem in self.idRemoveSelectionField.selectedItems():
            self.main.removalSelection.append(int(selItem.text()))
        
        self.accept()

        self.logProgress(stack()[0][3] + " END")
        
    def cancelButtonClicked(self):
        self.logProgress(stack()[0][3])

        self.close()

        self.logProgress(stack()[0][3] + " END")

    def logProgress(self, message):
        logString = "log.lfn"
        logFile = os.path.join('AutoSave',logString)
        logFile = open(logFile,'a')
        logFile.write(message + "\n")
        logFile.close()
