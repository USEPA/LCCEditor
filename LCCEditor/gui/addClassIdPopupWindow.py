"""

    Last Modified 12/15/13

"""

from PySide import QtCore, QtGui
#from PySide.QtGui import *
from inspect import stack
import os
from PySide.QtCore import QRegExp



class AddClassIdPopupWindow(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self,main):
        '''
        Constructor
        '''
        # initialize the class from the super class
        super(AddClassIdPopupWindow,self).__init__()
        self.main = main
        
        #self.main.notify.notify.emit('In emit')
        # create layout
        self.layout=QtGui.QGridLayout()                   # create a grid widget
        self.layout.setSpacing(10)                  # set the spacing between widgets
        
        self.addClassTableWidget = QtGui.QTableWidget()
        self.addClassTableWidget.setEnabled(True)
        self.addClassTableWidget.setShowGrid(True)
        self.addClassTableWidget.setObjectName("ClassTableWidgetDialog")
        
        self.columnCount = 2
        headerLabels = ["Class", "Description"]
        headerLabels.extend(self.main.tempLccObj.overwriteFieldsNames)
        self.columnCount = self.columnCount + len(self.main.tempLccObj.overwriteFieldsNames)
        
        self.addClassTableWidget.setRowCount(1)
        self.addClassTableWidget.setColumnCount(self.columnCount)
        
#        self.addClassTableWidget.setHorizontalHeaderLabels(headerLabels)
        for index, iterator in enumerate(headerLabels):
            if index < 2:
#                 tempMap = QPixmap()
#                 asteriskPath = os.path.join(main.originalFileDirectoryPointer, "img\\asterisk.png")
#                 tempMap.load(asteriskPath)
#                 tempMap = tempMap.scaled(QtCore.QSize(8,8))
#                 tempIcon = QIcon()
#                 tempIcon.addPixmap(tempMap)
#                 temp = QTableWidgetItem(tempIcon, iterator)
                temp = QtGui.QTableWidgetItem("* " + iterator)
                temp.setTextAlignment(QtCore.Qt.AlignLeft)
            else:
                temp = QtGui.QTableWidgetItem(iterator)
                
            self.addClassTableWidget.setHorizontalHeaderItem(index, temp)
            


        self.addClassTableWidget.setColumnWidth(0,50)
        self.addClassTableWidget.setColumnWidth(1, 150)
        
        index = 2
        dynamicDialogWidth = 300
        
        while index < self.columnCount:
            self.addClassTableWidget.setColumnWidth(index, 100)
            dynamicDialogWidth +=100
            index += 1
        
        self.layout.addWidget(self.addClassTableWidget, 1, 1, 1, 1)

        self.errorMessage = QtGui.QLabel()
        self.layout.addWidget(self.errorMessage, 3, 1 , 2 , 1)
                       
        # -- create label and button widgets
#         self.requiredLabel = QLabel('<img src="' + asteriskPath + '" width="8" height="8"> This is a required field.')
        self.requiredLabel = QtGui.QLabel('* This is a required field.')
        self.okButton = QtGui.QPushButton('OK')
        self.cancelButton = QtGui.QPushButton('Cancel')
        
        # -- connect ok and cancel buttons to their event handlers
        self.okButton.clicked.connect(self.okButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        #self.okButton.clicked.connect(self.wakeup)
         
        # -- create a new layout view for buttons
        self.buttonBox = QtGui.QHBoxLayout()                  # create a QHBoxLayout object
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
            
        self.setGeometry(500, 300, dynamicDialogWidth, 200)
        self.setWindowTitle(self.main.dialogTitle)      # set title of popup window
        self.logProgress("***** addClassIdPopupWindow *****")
    
    def evaluateInput(self):
        self.logProgress(stack()[0][3])
        
        def focusOnError(column):
            if not self.addClassTableWidget.item(0,0):
                newTableItem = QtGui.QTableWidgetItem()
                self.addClassTableWidget.setItem(0, 0, newTableItem)
            if not self.addClassTableWidget.item(0,1):
                newTableItem = QtGui.QTableWidgetItem()
                self.addClassTableWidget.setItem(0, 1, newTableItem)
            
            index = 0
            while index < self.columnCount:
                if self.addClassTableWidget.item(0,index):
                    self.addClassTableWidget.item(0,index).setSelected(False)
                index += 1
            self.addClassTableWidget.item(0,column).setSelected(True)

            self.addClassTableWidget.setCurrentItem(self.addClassTableWidget.item(0,column))
            self.addClassTableWidget.editItem(self.addClassTableWidget.item(0, column))

        self.errorMessage.setText("")                                 # reset error message to empty
                        
        if not self.addClassTableWidget.item(0, 0) or self.addClassTableWidget.item(0,0).text().strip() == "":           
            self.errorMessage.setText("Please enter a <font color=red>CLASS</font>")
            focusOnError(0)
            return False
        
        if not self.addClassTableWidget.item(0, 1) or self.addClassTableWidget.item(0,1).text().strip() == "":
            self.errorMessage.setText("Please enter a <font color=red>DESCRIPTION</font>")
            focusOnError(1)
            return False

#         rx = QRegExp("[A-Za-z]{3,5}")       # {min, max}
#         validator = QRegExpValidator(rx ,self)
#         classValid =  validator.validate(self.addClassTableWidget.item(0,0).text(), 0)
#         if classValid[0] != QtGui.QValidator.State.Acceptable:
#             if classValid[2] < 3 or classValid[2] > 5:
#                 self.errorMessage.setText("Class must be between 3 and 5 character in length.")
#                 focusOnError(0)
#                 return False
#             else:
#                 self.errorMessage.setText("Class must consist only characters.")
#                 focusOnError(0)
#                 return False

        # Strips whitespace from everything
        index = 0
        while(index < self.columnCount):
            if self.addClassTableWidget.item(0, index):
                self.addClassTableWidget.item(0, index).setText(self.addClassTableWidget.item(0, index).text().strip())
            index += 1
            
        ## evaluate for classId in class tree
        ## compare if classId is in key references of main lcc object
        ## by comparing keys of landCoverclasss dictionary 
        ## if found, we change error message and change flag to recall new dialog
        if self.addClassTableWidget.item(0,0).text().lower() in self.main.tempLccObj.classes.keys():
            self.errorMessage.setText("<font color=red>CLASS</font> already exists in Class Tree")
            focusOnError(0)
            return False
    
        ## evaluate for name in class tree
        ##  checkreference is an iterator of LandCoverclass objects
        ## which we iterate over to find if name exists in the class tree 
        ## if isName returns true on match, we change error message and change flag to recall new dialog
#         for checkReference in self.main.tempLccObj.classes.values():
#             if checkReference.isName(self.addClassTableWidget.item(0, 1).text()):           
#                 self.errorMessage.setText("The <font color=red>DESCRIPTION</font> already exists in Class Tree")
#                 focusOnError(1)
#                 return False
        
        index = 2
        
        while index < self.columnCount:
            if self.addClassTableWidget.item(0, index):  
                if not self.addClassTableWidget.item(0, index).text() == "" and \
                                        self.addClassTableWidget.item(0,index).text() in  \
                                        self.main.tempLccObj.overwriteFieldDataList:
                    errorString = "The overwriteField attribute \"<font color=red>" \
                                    + self.addClassTableWidget.item(0,index).text() \
                                    + "</font>\" in \"<font color=red>" \
                                    + (self.addClassTableWidget.horizontalHeaderItem(index).text()).upper() \
                                    +"</font>\" has already been used."                      
                    self.errorMessage.setText(errorString)
                    self.addClassTableWidget.item(0,index).setText("")            # remove field in dialog
                    focusOnError(index)
                    return False
            index += 1
                 
        checkColumnOne = 2
        checkColumnTwo = 2
        
        while checkColumnOne < self.columnCount:
            checkColumnTwo = checkColumnOne
            if not self.addClassTableWidget.item(0, checkColumnOne) \
                                                    or self.addClassTableWidget.item(0, checkColumnOne).text() == "":
                checkColumnOne += 1
                continue
            while checkColumnTwo < self.columnCount:
                if checkColumnOne == checkColumnTwo or not self.addClassTableWidget.item(0, checkColumnTwo) \
                                                or self.addClassTableWidget.item(0, checkColumnTwo).text() == "":
                    checkColumnTwo += 1
                    continue
                
                if self.addClassTableWidget.item(0, checkColumnOne).text() == \
                                                            self.addClassTableWidget.item(0,checkColumnTwo).text():
                    errorString = "The overwriteField attribute for \"<font color=red>" \
                                            + self.addClassTableWidget.horizontalHeaderItem(checkColumnOne).text() \
                                            + "</font>\" is the same as the overwriteField attribute for \"<font color=red>" \
                                            + self.addClassTableWidget.horizontalHeaderItem(checkColumnTwo).text() \
                                            + "</font>\".  Attributes must be distinct."                      
                    self.errorMessage.setText(errorString)
                    self.addClassTableWidget.item(0, checkColumnOne).setText(
                                self.main.dialogVariable.classoverwriteFields[str(
                                self.addClassTableWidget.horizontalHeaderItem(checkColumnOne).text())])
                    self.addClassTableWidget.item(0, checkColumnTwo).setText(
                                self.main.dialogVariable.classoverwriteFields[str(
                               self.addClassTableWidget.horizontalHeaderItem(checkColumnTwo).text())])
                    focusOnError(checkColumnOne)
                    return False
                checkColumnTwo += 1
            checkColumnOne += 1

        self.logProgress(stack()[0][3] + " END")
                            
        return True
    
    def extractData(self):
        self.logProgress(stack()[0][3])
        
        tempoverwriteField = {}
        
        index = 2
        while index <  self.columnCount:
            if self.addClassTableWidget.item(0, index) and not self.addClassTableWidget.item(0, index).text() == "": 
                tempoverwriteField[self.addClassTableWidget.horizontalHeaderItem(index).text()] = \
                        self.addClassTableWidget.item(0, index).text()
            index += 1                           
       
        self.main.dialogVariable.addClass(self.addClassTableWidget.item(0, 0).text(), 
                                         self.addClassTableWidget.item(0, 1).text(), 
                                         tempoverwriteField)     
        self.logProgress(stack()[0][3] + " END")

    def okButtonClicked(self):
        self.logProgress(stack()[0][3])
        
        if not self.evaluateInput():
            return
        self.extractData()
        
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