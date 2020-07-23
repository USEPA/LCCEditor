"""

    Last Modified 12/15/13
    
"""

import PySide
from PySide import QtCore, QtGui
#from PySide.QtGui import *
from pylet import lcc
from inspect import stack
import os

class AddValueTableIdPopupWindow(QtGui.QDialog):
    def __init__(self, main):

        # initialize the class from the super class

        super(AddValueTableIdPopupWindow,self).__init__()

        self.main = main
        
        #self.main.notify.notify.emit('In emit')
        # create layout
        self.layout= QtGui.QGridLayout()                   # create a grid widget
        self.layout.setSpacing(10)                  # set the spacing between widgets

        self.valueTableWidgetDialog = QtGui.QTableWidget()
        self.valueTableWidgetDialog.setEnabled(True)
        self.valueTableWidgetDialog.setShowGrid(True)
        self.valueTableWidgetDialog.setObjectName("valueTableWidgetDialog")
        
        columncount = 3
        headerLabels = ["Value", "Description", "X"]
            
        if not main.tempLccObj.coefficients == None:
            for iterator in main.tempLccObj.coefficients.keys():
                headerLabels.append(iterator)
            columncount = columncount + len(main.tempLccObj.coefficients.keys())
                   
        self.valueTableWidgetDialog.setSortingEnabled(True)
        self.valueTableWidgetDialog.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.valueTableWidgetDialog.setRowCount(1)
        self.valueTableWidgetDialog.setColumnCount(columncount)
        self.valueTableWidgetDialog.setColumnWidth(0,50)
        self.valueTableWidgetDialog.setColumnWidth(1,225)
        self.valueTableWidgetDialog.setColumnWidth(2,20)
                
        index = len(self.main.tempLccObj.coefficients.keys()) + 3
        self.col = 3
        
        while self.col < index:
            tempItem = QtGui.QTableWidgetItem("0.0")
            tempItem.setTextAlignment(QtCore.Qt.AlignRight)
            self.valueTableWidgetDialog.setItem(0, self.col, tempItem)
            self.valueTableWidgetDialog.setColumnWidth(self.col,150)
            self.col = self.col + 1

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
                
            self.valueTableWidgetDialog.setHorizontalHeaderItem(index, temp)
            
        self.valueTableWidgetDialog.verticalHeader().setVisible(False)
        
        populateExclusion = QtGui.QTableWidgetItem()
        populateExclusion.setCheckState(QtCore.Qt.Unchecked)
        populateExclusion.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        self.valueTableWidgetDialog.setItem(0, 2, populateExclusion)
            
        self.layout.addWidget(self.valueTableWidgetDialog, 1,1,1,1)

        self.errorMessage = QtGui.QLabel()
        self.layout.addWidget(self.errorMessage, 3, 1, 2, 1)

        # -- create label and button widgets
#         self.requiredLabel = QLabel('<img src="' + asteriskPath + '" width="8" height="8">This is a required field.')
        self.requiredLabel = QtGui.QLabel('* This is a required field.')
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
        self.setGeometry(500, 300, 600, 250)
        self.setWindowTitle(self.main.dialogTitle)      # set title of popup window


#         column = 3
#         while column < self.col:
#             self.valueTableWidgetDialog.item(0,column).setText("0.0")
#             column = column + 1
        self.logProgress("**** addValueTablePopupWindow ****")

    def evaluateInput(self):
        ## evaluate for valueId in value tree
        ## compare if ValueId is in key references of main lcc object
        ## by comparing keys of landCoverValues dictionary 
        ## if found, we change error message and change flag to recall new dialog
        self.logProgress(stack()[0][3])

        def focusOnError(row, column):
            self.logProgress(stack()[0][3])
            
            if not self.valueTableWidgetDialog.item(row,0):
                newTableItem = QtGui.QTableWidgetItem()
                self.valueTableWidgetDialog.setItem(row, 0, newTableItem)
            if not self.valueTableWidgetDialog.item(row, 1):
                newTableItem = QtGui.QTableWidgetItem()
                self.valueTableWidgetDialog.setItem(row, 1, newTableItem)
            
            index = 0
            while index < self.col:
                if self.valueTableWidgetDialog.item(row,index):
                    self.valueTableWidgetDialog.item(row, index).setSelected(False)
                index += 1
            self.valueTableWidgetDialog.item(row, column).setSelected(True)
            self.valueTableWidgetDialog.setCurrentItem(self.valueTableWidgetDialog.item(row, column))
            self.valueTableWidgetDialog.editItem(self.valueTableWidgetDialog.item(row, column))
      
        rowIndex =  0
        while rowIndex < self.valueTableWidgetDialog.rowCount():        

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
            if not self.valueTableWidgetDialog.item(rowIndex,0) or  \
                not self.valueTableWidgetDialog.item(rowIndex,0).text() or  \
                self.valueTableWidgetDialog.item(rowIndex,0).text().strip() == "":
                
                
                self.message = "Please enter a <font color=red>VALUE</font> or delete the row"
                focusOnError(rowIndex, 0)
                return
            
            if not self.valueTableWidgetDialog.item(rowIndex,1) or  \
                not self.valueTableWidgetDialog.item(rowIndex,1).text() or  \
                self.valueTableWidgetDialog.item(rowIndex,1).text().strip() == "":
                
                self.message = "Please enter a <font color=red>DESCRIPTION</font> or delete the row"
                focusOnError(rowIndex, 1)
                return
            
            if not self.main.isInt(self.valueTableWidgetDialog.item(rowIndex,0).text()):
                self.message = "<font color=red>VALUE</font> must be an integer."
                focusOnError(rowIndex, 0)
                return  

            if int(self.valueTableWidgetDialog.item(rowIndex,0).text()) in self.main.tempLccObj.values.keys():
                self.message = "<font color=red>VALUE</font> already exists in Value Table"       
                focusOnError(rowIndex, 0)
                return
            
            # Remove leading and trailing whitespace from input name
            self.valueTableWidgetDialog.item(rowIndex, 1).setText(self.valueTableWidgetDialog.item(rowIndex, 1).text().strip())
            
            for checkNameObject in self.main.tempLccObj.values.values():
                if checkNameObject.isName(self.valueTableWidgetDialog.item(rowIndex, 1).text()):
                    valName = checkNameObject.name.lower()
                    self.message = "<font color=red> " + (valName.title()).upper() \
                        + "</font> already exists as a Value Description in Value Table. Please choose a different \
                        <font color=red>Descritpion.</font>"
                    focusOnError(rowIndex, 1)
                    return
            rowPointer = rowIndex + 1
            while rowPointer < self.valueTableWidgetDialog.rowCount():
                if self.valueTableWidgetDialog.item(rowIndex, 0).text() == \
                                                        self.valueTableWidgetDialog.item(rowPointer,0).text():
                    self.message = "<font color=red>VALUE</font> already exists in Add Value Dialog"       
                    focusOnError(rowPointer, 0)
                    return
                if self.valueTableWidgetDialog.item(rowIndex, 1).text() == \
                                                        self.valueTableWidgetDialog.item(rowPointer,1).text():
                    self.message = "<font color=red>VALUE Description</font> already exists in add Dialog"       
                    focusOnError(rowPointer, 1)
                    return
                rowPointer += 1
            column = 3
            while column < self.col:
                if not self.main.isFloat(self.valueTableWidgetDialog.item(rowIndex,column).text()):
                    colName =  self.valueTableWidgetDialog.horizontalHeaderItem(column).text()
                    self.message = "The Coefficient <font color=red>" + colName.upper() \
                        + "</font> value must be a decimal."
                    focusOnError(rowIndex, column)
                    return
                column = column + 1
            rowIndex += 1

        self.logProgress(stack()[0][3] + " END")
                            
    def extractValueTableInfo(self,row,newLandCoverValue):
        self.logProgress(stack()[0][3])
        
        newLandCoverValue.valueId = int(self.valueTableWidgetDialog.item(row,0).text())
        newLandCoverValue.name = self.valueTableWidgetDialog.item(row,1).text()
        
        if self.valueTableWidgetDialog.item(row, 2).checkState() == QtCore.Qt.Checked:
            newLandCoverValue.excluded = True
        else:
            newLandCoverValue.excluded = False
        column = 3
        for specificKey in self.main.tempLccObj.coefficients.keys():
            tempholder = self.valueTableWidgetDialog.horizontalHeaderItem(column).text()
            newCoefficientObj = lcc.LandCoverCoefficient()
            newCoefficientObj.deepCopyCoefficient(self.main.tempLccObj.coefficients[tempholder])
            newCoefficientObj.populateCoefficientValue(self.valueTableWidgetDialog.item(row,column).text())
            newLandCoverValue._coefficients[tempholder] = newCoefficientObj
            column = column +1

        self.logProgress(stack()[0][3] + " END")

        return newLandCoverValue

    def addRowButtonClicked(self):
        self.logProgress(stack()[0][3])
        
        def deselect(row):
            self.logProgress(stack()[0][3])
            
            if not self.valueTableWidgetDialog.item(row,0):
                newTableItem = QtGui.QTableWidgetItem()
                self.valueTableWidgetDialog.setItem(row, 0, newTableItem)
            if not self.valueTableWidgetDialog.item(row,1):
                newTableItem = QtGui.QTableWidgetItem()
                self.valueTableWidgetDialog.setItem(row, 1, newTableItem)
            
            index = 0
            while index < self.col:
                if self.valueTableWidgetDialog.item(row,index):
                    self.valueTableWidgetDialog.item(row,index).setSelected(False)
                index += 1
        
        currentRow = self.valueTableWidgetDialog.rowCount()
        self.valueTableWidgetDialog.insertRow(currentRow)
        populateExclusion = QtGui.QTableWidgetItem()
        populateExclusion.setCheckState(QtCore.Qt.Unchecked)
        populateExclusion.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        self.valueTableWidgetDialog.setItem(currentRow, 2, populateExclusion)
        
        colIndex = 3
        while colIndex < self.col:
            tempItem = QtGui.QTableWidgetItem("0.0")
            tempItem.setTextAlignment(QtCore.Qt.AlignRight)
            self.valueTableWidgetDialog.setItem(currentRow, colIndex, tempItem)
            self.valueTableWidgetDialog.setColumnWidth(colIndex,150)
            colIndex += 1
        
        rowIndex = 0
        while rowIndex <= currentRow:
            deselect(rowIndex)
            rowIndex += 1
        
        self.valueTableWidgetDialog.item(currentRow,0).setSelected(True)
        self.valueTableWidgetDialog.setCurrentItem(self.valueTableWidgetDialog.item(currentRow, 0))
        self.valueTableWidgetDialog.editItem(self.valueTableWidgetDialog.item(currentRow, 0))

        self.logProgress(stack()[0][3] + " END")

    def removeSelectedRowClicked(self):
        self.logProgress(stack()[0][3])
        
        if not self.valueTableWidgetDialog.selectedItems():
            self.errorMessage.setText("No row selected")
            return
        self.valueTableWidgetDialog.removeRow(self.valueTableWidgetDialog.currentRow())
        self.errorMessage.setText("")

        self.logProgress(stack()[0][3] + " END")
    
    def okButtonClicked(self):
        self.logProgress(stack()[0][3])

        self.message = ""                                  # reset error message to empty
        self.evaluateInput()
        
        if self.message == "":
            rowIndex = 0
            while rowIndex < self.valueTableWidgetDialog.rowCount():
                tempLCVContainerObject = lcc.LandCoverValue()
                self.main.tempLCVObjectList.append(self.extractValueTableInfo(rowIndex, tempLCVContainerObject))
                rowIndex += 1
            self.accept()
        else:
            self.errorMessage.setText(self.message)

        self.logProgress(stack()[0][3] + " END")

    def cancelButtonClicked(self):
        self.logProgress(stack()[0][3])

        self.main.cancelFlag = True
        self.close()

        self.logProgress(stack()[0][3] + " END")
   
    def logProgress(self, message):
        logString = "log.lfn"
        logFile = os.path.join('AutoSave',logString)
        logFile = open(logFile,'a')
        logFile.write(message + "\n")
        logFile.close()
