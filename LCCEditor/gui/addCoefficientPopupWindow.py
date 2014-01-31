'''
    Created on Aug 26, 2013
   
    Last Modified 9/30/13

'''

import PySide
from PySide import QtCore, QtGui
#from PySide.QtGui import *
from inspect import stack
import os
from PySide.QtCore import QRegExp
import pylet

class AddCoefficientPopupWindow(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self,main):
        '''
        Constructor
        '''
        # initialize the class from the super class

        super(AddCoefficientPopupWindow,self).__init__()

        self.main = main
        
        #self.main.notify.notify.emit('In emit')
        # create layout
        self.layout=QtGui.QGridLayout()                   # create a grid widget
        self.layout.setSpacing(10)                  # set the spacing between widgets

        self.coefficientTableWidgetDialog = QtGui.QTableWidget()
        self.coefficientTableWidgetDialog.setEnabled(True)
        self.coefficientTableWidgetDialog.setShowGrid(True)
        self.coefficientTableWidgetDialog.setObjectName("coefficientTableWidgetDialog")
        
        columncount = 4
        headerLabels = ["Id", "Description", "Field Name","Method" ]
                   
        self.coefficientTableWidgetDialog.setSortingEnabled(True)
        self.coefficientTableWidgetDialog.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.coefficientTableWidgetDialog.setRowCount(1)
        self.coefficientTableWidgetDialog.setColumnCount(columncount)
        self.coefficientTableWidgetDialog.setColumnWidth(0,200)
        self.coefficientTableWidgetDialog.setColumnWidth(1,425)
        self.coefficientTableWidgetDialog.setColumnWidth(2,150)
        self.coefficientTableWidgetDialog.setColumnWidth(3,100)
        
        tempBox = QtGui.QComboBox()
        tempBox.addItem("A")
        tempBox.addItem("P")
        tempBox.currentIndex()
        self.coefficientTableWidgetDialog.setCellWidget(0, 3, tempBox)

        for index, iterator in enumerate(headerLabels):
            tempMap = QtGui.QPixmap()
            asteriskPath = os.path.join(main.originalFileDirectoryPointer, "img\\asterisk.png")
            tempMap.load(asteriskPath)
            tempMap = tempMap.scaled(QtCore.QSize(8,8))
            tempIcon = QtGui.QIcon()
            tempIcon.addPixmap(tempMap)
            temp = QtGui.QTableWidgetItem(tempIcon, iterator)
            temp.setTextAlignment(QtCore.Qt.AlignLeft)
                
            self.coefficientTableWidgetDialog.setHorizontalHeaderItem(index, temp)
            
        self.coefficientTableWidgetDialog.verticalHeader().setVisible(False)
            
        self.layout.addWidget(self.coefficientTableWidgetDialog, 1,1,1,1)

        self.errorMessage = QtGui.QLabel()
        self.layout.addWidget(self.errorMessage, 3, 1, 2, 1)

        # -- create label and button widgets
        self.requiredLabel = QtGui.QLabel('<img src="' + asteriskPath + '" width="8" height="8">This is a required field.')
        self.okButton = QtGui.QPushButton('OK')
        self.cancelButton = QtGui.QPushButton('Cancel')
        self.addRowButton = QtGui.QPushButton("Add Row")
        self.removeSelectedRowButton = QtGui.QPushButton("Remove Selected Row")
        
        # -- connect buttons to their event handlers
        self.okButton.clicked.connect(self.okButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.addRowButton.clicked.connect(self.addRowButtonClicked)
        self.removeSelectedRowButton.clicked.connect(self.removeSelectedRowClicked)
        
        #self.okButton.clicked.connect(self.wakeup)
        # -- create a new layout view for buttons
        self.buttonBox = QtGui.QHBoxLayout()                  # create a QHBoxLayout object
        self.buttonBox.addWidget(self.requiredLabel)
        self.buttonBox.addStretch(1)                    # set stretch requirements
        self.buttonBox.addWidget(self.addRowButton)
        self.buttonBox.addWidget(self.removeSelectedRowButton)
        self.buttonBox.addWidget(self.okButton)         # add ok Button to interface
        self.buttonBox.addWidget(self.cancelButton)     # add cancel button to interface
        

        # add ok and cancel buttons to UI layout
        self.layout.addLayout(self.buttonBox, 5, 1)
        self.setLayout(self.layout)

        #set the window size and title. Then display the UI window (left, top, width, height)
        self.setGeometry(500, 300, 900, 250)
        self.setWindowTitle(self.main.dialogTitle)      # set title of popup window


        self.logProgress("**** coefficientTablePopupWindow ****")

    def evaluateInput(self):
        ## evaluate for valueId in value tree
        ## compare if ValueId is in key references of main lcc object
        ## by comparing keys of landCoverValues dictionary 
        ## if found, we change error message and change flag to recall new dialog
        self.logProgress(stack()[0][3])

        def focusOnError(row, column):
            self.logProgress(stack()[0][3])
            
            if not self.coefficientTableWidgetDialog.item(row,0):
                newTableItem = QtGui.QTableWidgetItem()
                self.coefficientTableWidgetDialog.setItem(row, 0, newTableItem)
            if not self.coefficientTableWidgetDialog.item(row, 1):
                newTableItem = QtGui.QTableWidgetItem()
                self.coefficientTableWidgetDialog.setItem(row, 1, newTableItem)
            if not self.coefficientTableWidgetDialog.item(row, 2):
                newTableItem = QtGui.QTableWidgetItem()
                self.coefficientTableWidgetDialog.setItem(row, 2, newTableItem)
            
            self.coefficientTableWidgetDialog.item(row, column).setSelected(True)
            self.coefficientTableWidgetDialog.setCurrentItem(self.coefficientTableWidgetDialog.item(row, column))
            self.coefficientTableWidgetDialog.editItem(self.coefficientTableWidgetDialog.item(row, column))
      
        rowIndex =  0
        while rowIndex < self.coefficientTableWidgetDialog.rowCount():        

            # The following conditions need to be checked for:
            # 1. The table item hasn't been selected which mean no object has been created in the table grid which means
            #    calling the table grid item will return a Nonetype because there is no  object.
            # 2. The table position was selected but no item was entered which means that calling the object.text will
            #    return a Nonetype.
            # 3. The table item is reselected and the information is deleted which means that calling the object.text
            #    will return an empty string.
            # 4. Whether the Id is an INT.
            # 5. Whether the value exists in the Value Table .
            # 6. Whether the value exists in the current Add Value Dialog.
            # 7. Whether the description already exists in the Add Value Dialog.
            # 8. Whether the description already exists in the Value Table.
            
            if not self.coefficientTableWidgetDialog.item(rowIndex,0) or  \
                self.coefficientTableWidgetDialog.item(rowIndex,0).text().strip() == "":
                
                self.errorMessage.setText("Please enter an <font color=red>Id</font>")

                focusOnError(rowIndex, 0)
                return False
            
            if not self.coefficientTableWidgetDialog.item(rowIndex,1) or  \
                self.coefficientTableWidgetDialog.item(rowIndex,1).text().strip() == "":
                
                self.errorMessage.setText("Please enter a <font color=red>Name</font> or delete a row")
                focusOnError(rowIndex, 1)
                return False

            if not self.coefficientTableWidgetDialog.item(rowIndex,2) or  \
                self.coefficientTableWidgetDialog.item(rowIndex,2).text().strip() == "":
                
                self.errorMessage.setText("Please enter a <font color=red>Field Name</font> or delete a row")
                focusOnError(rowIndex, 2)
                return False
            
            # This evaluates whether Id is letters
            rx = QRegExp("[A-Za-z]{,}")
            validator = QtGui.QRegExpValidator(rx ,self)
            coefIdValid =  validator.validate(self.coefficientTableWidgetDialog.item(0,0).text(), 0)
            
            if coefIdValid[0] != QtGui.QValidator.State.Acceptable:
                self.errorMessage.setText("Id must consist only of characters.")
                focusOnError(rowIndex, 0)
                return False
            
            # Convert lower case to upper case
            self.coefficientTableWidgetDialog.item(rowIndex, 0).setText(
                        self.coefficientTableWidgetDialog.item(rowIndex, 0).text().strip().upper())
  
            if self.coefficientTableWidgetDialog.item(rowIndex,0).text() in self.main.tempLccObj.coefficients.keys():
                self.errorMessage.setText("<font color=red>Id</font> already exists in Coefficient Table")       
                focusOnError(rowIndex, 0)
                return False
                       
            rowPointer = rowIndex + 1
            while rowPointer < self.coefficientTableWidgetDialog.rowCount():
                if self.coefficientTableWidgetDialog.item(rowIndex, 0).text() == \
                                                        self.coefficientTableWidgetDialog.item(rowPointer,0).text():
                    self.errorMessage.setText("<font color=red>ID</font> already exists in Add Coefficient Dialog")       
                    focusOnError(rowPointer, 0)
                    return False
                rowPointer += 1
            rowIndex += 1

        self.logProgress(stack()[0][3] + " END")
        return True
                        
    def extractCoefficientTableInfo(self, row):
        self.logProgress(stack()[0][3])
        
        newLandCoverCoefficient = pylet.lcc.LandCoverCoefficient()
        
        newLandCoverCoefficient.coefId = self.coefficientTableWidgetDialog.item(row,0).text()
        newLandCoverCoefficient.name = self.coefficientTableWidgetDialog.item(row,1).text()
        newLandCoverCoefficient.fieldName = self.coefficientTableWidgetDialog.item(row,2).text()
        newLandCoverCoefficient.calcMethod = self.coefficientTableWidgetDialog.cellWidget(row,3).currentText()

        self.logProgress(stack()[0][3] + " END")

        return newLandCoverCoefficient

    def addRowButtonClicked(self):
        self.logProgress(stack()[0][3])
        
        def deselect(row):
            self.logProgress(stack()[0][3])
            
            if not self.coefficientTableWidgetDialog.item(row,0):
                newTableItem = QtGui.QTableWidgetItem()
                self.coefficientTableWidgetDialog.setItem(row, 0, newTableItem)
            if not self.coefficientTableWidgetDialog.item(row,1):
                newTableItem = QtGui.QTableWidgetItem()
                self.coefficientTableWidgetDialog.setItem(row, 1, newTableItem)

            if not self.coefficientTableWidgetDialog.item(row,2):
                newTableItem = QtGui.QTableWidgetItem()
                self.coefficientTableWidgetDialog.setItem(row, 2, newTableItem)
            if not self.coefficientTableWidgetDialog.item(row,3):
                tempBox = QtGui.QComboBox()
                tempBox.addItem("A")
                tempBox.addItem("P")
                tempBox.currentIndex()
                self.coefficientTableWidgetDialog.setCellWidget(row, 3, tempBox)
                    
        currentRow = self.coefficientTableWidgetDialog.rowCount()
        self.coefficientTableWidgetDialog.insertRow(currentRow)
              
        rowIndex = 0
        while rowIndex <= currentRow:
            deselect(rowIndex)
            rowIndex += 1
        
        self.coefficientTableWidgetDialog.item(currentRow,0).setSelected(True)
        self.coefficientTableWidgetDialog.setCurrentItem(self.coefficientTableWidgetDialog.item(currentRow, 0))
        self.coefficientTableWidgetDialog.editItem(self.coefficientTableWidgetDialog.item(currentRow, 0))

        self.logProgress(stack()[0][3] + " END")

    def removeSelectedRowClicked(self):
        self.logProgress(stack()[0][3])
        
        if not self.coefficientTableWidgetDialog.selectedItems():
            self.errorMessage.setText("No row selected")
            return
        self.coefficientTableWidgetDialog.removeRow(self.coefficientTableWidgetDialog.currentRow())
        self.errorMessage.setText("")

        self.logProgress(stack()[0][3] + " END")
    
    def okButtonClicked(self):
        self.logProgress(stack()[0][3])
        
        if self.evaluateInput():
            rowIndex = 0
            while rowIndex < self.coefficientTableWidgetDialog.rowCount():
                self.main.tempCoefObjList.append(self.extractCoefficientTableInfo(rowIndex))
                rowIndex += 1
            
            self.logProgress(stack()[0][3] + " END")
    
            self.accept()

    def cancelButtonClicked(self):
        self.logProgress(stack()[0][3])

        self.main.cancelFlag = True
        self.close()

        self.logProgress(stack()[0][3] + " END")
   
    def logProgress(self, message):
        logFile = open("log.lfn",'a')
        logFile.write(message + "\n")
        logFile.close()
