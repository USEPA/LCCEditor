'''
Created on Aug 31, 2013

' Last Modified 12/15/13'

'''

from PySide import QtCore, QtGui
from PySide.QtGui import *
import pylet
from inspect import stack
import os

class EditClassInfoPopUpWindow(QDialog):
    '''
    classdocs
    '''


    def __init__(self,main):
        '''
        Constructor
        '''
        # initialize the class from the super class
        super(EditClassInfoPopUpWindow,self).__init__()
        self.main = main
        
        #self.main.notify.notify.emit('In emit')
        # create layout
        self.layout=QtGui.QGridLayout()                   # create a grid widget
        self.layout.setSpacing(10)                  # set the spacing between widgets
        
        self.editClassTableWidget = QtGui.QTableWidget()
        self.editClassTableWidget.setEnabled(True)
        self.editClassTableWidget.setShowGrid(True)
        self.editClassTableWidget.setObjectName("ClassTableWidgetDialog")
        
        self.columnCount = 2
        headerLabels = ["Class", "Description"]
        headerLabels.extend(self.main.tempLccObj.overwriteFieldsNames)
        self.columnCount = self.columnCount + len(self.main.tempLccObj.overwriteFieldsNames)
        
        self.editClassTableWidget.setRowCount(1)
        self.editClassTableWidget.setColumnCount(self.columnCount)
        
        for index, iterator in enumerate(headerLabels):
            if index < 2:
#                 tempMap = QPixmap()
#                 asteriskPath = os.path.join(main.originalFileDirectoryPointer, "img\\asterisk.png")
#                 tempMap.load(asteriskPath)
#                 tempMap = tempMap.scaled(QtCore.QSize(8,8))
#                 tempIcon = QIcon()
#                 tempIcon.addPixmap(tempMap)
#                 temp = QTableWidgetItem(tempIcon, iterator)
                temp = QTableWidgetItem("* " + iterator)
                temp.setTextAlignment(QtCore.Qt.AlignLeft)
            else:
                temp = QTableWidgetItem(iterator)
                
            self.editClassTableWidget.setHorizontalHeaderItem(index, temp)
            
        self.editClassTableWidget.verticalHeader().setVisible(False)

        self.editClassTableWidget.setColumnWidth(0,50)
        self.editClassTableWidget.setColumnWidth(1, 150)
        
        index = 2
        dynamicDialogWidth = 300
        
        while index < self.columnCount:
            self.editClassTableWidget.setColumnWidth(index, 100)
            dynamicDialogWidth +=100
            index += 1
        
        self.layout.addWidget(self.editClassTableWidget, 1, 1, 1, 1)

        self.errorMessage = QtGui.QLabel()
        self.layout.addWidget(self.errorMessage, 3, 1 , 2 , 1)
               
        # -- create ok and cancel buttons widget
#         self.requiredLabel = QLabel('<img src="' + asteriskPath + '" width="8" height="8"> This is a required field.')
        self.requiredLabel = QLabel('* This is a required field.')
        self.okButton = QPushButton('OK')
        self.cancelButton = QPushButton('Cancel')
        
        # -- connect ok and cancel buttons to their event handlers
        self.okButton.clicked.connect(self.okButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        #self.okButton.clicked.connect(self.wakeup)
         
        # -- create a new layout view for buttons
        self.buttonBox = QHBoxLayout()                  # create a QHBoxLayout object
        self.buttonBox.addWidget(self.requiredLabel)
        self.buttonBox.addStretch(1)                    # set stretch requirements
        self.buttonBox.addWidget(self.okButton)         # add ok Button to interface
        self.buttonBox.addWidget(self.cancelButton)     # add cancel button to interface
        
        # add ok and cancel buttons to UI layout
        self.layout.addLayout(self.buttonBox, 8, 1)
                
        self.setLayout(self.layout)

        #set the window size and title. Then display the UI window (left, top, width, height)
        if dynamicDialogWidth > 800:
            dynamicDialogWidth = 800
        
        #set the window size and title. Then display the UI window (left, top, width, height)
        self.setGeometry(500, 300, dynamicDialogWidth, 200)
        self.setWindowTitle(self.main.dialogTitle)      # set title of popup window
                    
        self.editTableClassId = QtGui.QTableWidgetItem(self.main.dialogVariable.classId)
        self.editClassTableWidget.setItem(0, 0, self.editTableClassId)
        self.editTableClassName = QtGui.QTableWidgetItem(self.main.dialogVariable.name)
        self.editClassTableWidget.setItem(0, 1, self.editTableClassName)
        
        column = 2
        for lcpKeys in self.main.dialogVariable.classoverwriteFields:
            self.editTableClassoverwriteField = QtGui.QTableWidgetItem(
                        self.main.dialogVariable.classoverwriteFields[str(self.editClassTableWidget.horizontalHeaderItem(column).text())])
            self.editClassTableWidget.setItem(0, column, self.editTableClassoverwriteField)
            column += 1
        
        self.logProgress("**** editClassInfoPopUpWindow ****")
                
    def evaluateInput(self):
        self.logProgress(stack()[0][3])
      
        def focusOnError(column):
            self.logProgress(stack()[0][3])
            
            if not self.editClassTableWidget.item(0,0):
                newTableItem = QtGui.QTableWidgetItem()
                self.editClassTableWidget.setItem(0, 0, newTableItem)
            if not self.editClassTableWidget.item(0,1):
                newTableItem = QtGui.QTableWidgetItem()
                self.editClassTableWidget.setItem(0, 1, newTableItem)
            
            index = 0
            while index < self.columnCount:
                if self.editClassTableWidget.item(0,index):
                    self.editClassTableWidget.item(0,index).setSelected(False)
                index += 1
            self.editClassTableWidget.item(0,column).setSelected(True)

            self.editClassTableWidget.setCurrentItem(self.editClassTableWidget.item(0,column))
            self.editClassTableWidget.editItem(self.editClassTableWidget.item(0, column))

        self.errorMessage.setText("")                                 # reset error message to empty
        
        if not self.editClassTableWidget.item(0, 0).text() == self.main.dialogVariable.classId: 
            if not self.editClassTableWidget.item(0, 0).text().strip():           
                self.errorMessage.setText("Please enter a <font color=red>CLASS</font>")
                self.editClassTableWidget.item(0, 0).setText(self.main.dialogVariable.classId)
                focusOnError(0)
                return False

            self.editClassTableWidget.item(0, 0).setText(self.editClassTableWidget.item(0, 0).text().strip())
            ## evaluate for classId in class tree
            ## compare if classId is in key references of main lcc object
            ## by comparing keys of landCoverclasss dictionary 
            ## if found, we change error message and change flag to recall new dialog
            if self.editClassTableWidget.item(0, 0).text() in self.main.tempLccObj.classes.keys():
                self.errorMessage.setText("<font color=red>CLASS ID</font> already exists in class Tree")
                self.editClassTableWidget.item(0, 0).setText(self.main.dialogVariable.classId)
                focusOnError(0)
                return False
        
        if not self.editClassTableWidget.item(0, 1).text() == self.main.dialogVariable.name:
            if not self.editClassTableWidget.item(0, 1).text().strip():
                self.errorMessage.setText("Please enter a <font color=red>CLASS DESCRIPTION</font>")
                self.editClassTableWidget.item(0, 1).setText(self.main.dialogVariable.name)
                focusOnError(1)
                return False
            
            self.editClassTableWidget.item(0, 1).setText(self.editClassTableWidget.item(0,1).text().strip())
            ## evaluate for name in class tree
            ##  checkreference is an iterator of LandCoverclass objects
            ## which we iterate over to find if name exists in the class tree 
            ## if isName returns true on match, we change error message and change flag to recall new dialog
            for checkReference in self.main.tempLccObj.classes.values():
                if checkReference.isName(self.editClassTableWidget.item(0, 1).text()):           
                    self.errorMessage.setText("<font color=red>CLASS DESCRIPTION</font> already exists in class Tree.")
                    self.editClassTableWidget.item(0, 1).setText(self.main.dialogVariable.name)
                    focusOnError(1)
                    return False

        column = 2
        while column < self.columnCount:
            if not self.editClassTableWidget.item(0, column).text() == self.main.dialogVariable.classoverwriteFields[str(
                                                self.editClassTableWidget.horizontalHeaderItem(column).text())]:
                if not self.editClassTableWidget.item(0, column).text() ==  "" \
                                    and self.editClassTableWidget.item(0, column).text() \
                                    in self.main.tempLccObj.overwriteFieldDataList:
                    errorString = "The overwriteField attribute \"<font color=red>" + \
                                            self.editClassTableWidget.item(0, column).text() \
                                            + "</font>\" in <font color=red>" \
                                            + self.editClassTableWidget.horizontalHeaderItem(column).text() \
                                            + "</font> has already been used.</font>"                      
                    self.errorMessage.setText(errorString)
                    self.editClassTableWidget.item(0, column).setText(
                                self.main.dialogVariable.classoverwriteFields[str(
                                self.editClassTableWidget.horizontalHeaderItem(column).text())])
                    focusOnError(column)
                    return False
            column += 1


        checkColumnOne = 2
        checkColumnTwo = 2
        
        while checkColumnOne < self.columnCount:
            checkColumnTwo = checkColumnOne
            if not self.editClassTableWidget.item(0, checkColumnOne) \
                                                    or self.editClassTableWidget.item(0, checkColumnOne).text() == "":
                checkColumnOne += 1
                continue
            
            while checkColumnTwo < self.columnCount:
                if checkColumnOne == checkColumnTwo or not self.editClassTableWidget.item(0, checkColumnTwo) \
                                                or self.editClassTableWidget.item(0, checkColumnTwo).text() == "":
                    checkColumnTwo += 1
                    continue
                if self.editClassTableWidget.item(0, checkColumnOne).text() == \
                                                            self.editClassTableWidget.item(0,checkColumnTwo).text():
                    errorString = "The overwriteField attribute for \"<font color=red>" \
                                            + self.editClassTableWidget.horizontalHeaderItem(checkColumnOne).text() \
                                            + "</font>\" is the same as the overwriteField attribute for \"<font color=red>" \
                                            + self.editClassTableWidget.horizontalHeaderItem(checkColumnTwo).text() \
                                            + "</font>\".  Attributes must be distinct.</font>"                      
                    self.errorMessage.setText(errorString)
                    self.editClassTableWidget.item(0, checkColumnOne).setText(
                                self.main.dialogVariable.classoverwriteFields[str(
                                self.editClassTableWidget.horizontalHeaderItem(checkColumnOne).text())])
                    self.editClassTableWidget.item(0, checkColumnTwo).setText(
                                self.main.dialogVariable.classoverwriteFields[str(
                                self.editClassTableWidget.horizontalHeaderItem(checkColumnTwo).text())])
                    focusOnError(checkColumnOne)
                    return False
                checkColumnTwo += 1
            checkColumnOne += 1

        self.logProgress(stack()[0][3] + " END")
                            
        return True    
       
    def okButtonClicked(self):
        self.logProgress(stack()[0][3])

        if not self.evaluateInput():
            return
 
        self.main.dialogVariable.classId = str(self.editClassTableWidget.item(0, 0).text())
        self.main.dialogVariable.name = str(self.editClassTableWidget.item(0, 1).text())
        
        column = 2
        while column < self.columnCount:
            self.main.dialogVariable.classoverwriteFields[str(self.editClassTableWidget.horizontalHeaderItem(
                                        column).text())] = str(self.editClassTableWidget.item(0, column).text())
            column += 1
       
        self.accept()
        self.close()

        self.logProgress(stack()[0][3] + " END")
          
    def cancelButtonClicked(self):
        self.logProgress(stack()[0][3])

        self.close()

        self.logProgress(stack()[0][3] + " END")
        
    def logProgress(self, message):
        logFile = open("log.lfn",'a')
        logFile.write(message + "\n")
        logFile.close()
