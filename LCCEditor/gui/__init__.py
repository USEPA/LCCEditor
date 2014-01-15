
""" 
    Graphical User Interface (GUI) for the Land Cover Classification Editor (LCCEditor)

    The main() function launches the LCCEditor MainWindow

' Last Modified 12/15/13'

"""

import PySide
#from PySide import QtCore
#from PySide import QtGui

#from PySide.QtCore import *
from PySide.QtCore import Signal
from PySide.QtCore import Slot
from PySide.QtCore import QTimer
from PySide.QtCore import Qt

#from PySide.QtGui import *
from PySide.QtGui import QDialog
from PySide.QtGui import QMessageBox
from PySide.QtGui import QFileDialog
from PySide.QtGui import QFont

from PySide.QtGui import QMainWindow as _QMainWindow
from PySide.QtGui import QPushButton as _QPushButton
from PySide.QtGui import QApplication as _QApplication
from addClassIdPopupWindow import AddClassIdPopupWindow
from addValueTableIdPopupWindow import AddValueTableIdPopupWindow
from addValueToClassTreePopUpWindow import AddValueToClassTreePopUpWindow
from editClassInfoPopUpWindow import EditClassInfoPopUpWindow
from main_ui import Ui_MainWindow
from removeValuePopupWindow import RemoveValuePopupWindow
from xml.dom.minidom import Document, parse
from xml.etree.ElementTree import Comment, Element, ElementTree
import os, stat
from stat import *
import platform  # needed for platform details
import pylet
from pylet.lcc import constants
import sys as _sys
import xml.etree.ElementTree as etree
import operator
from inspect import stack
from addCoefficientPopupWindow import AddCoefficientPopupWindow
import pdb


VERSION = '0.0.1'
TITLE = "About Land Cover Classification Editor (LCCEditor)"

ABOUT_MESSAGE = """<b>Platform Details</b> v %s
                <p>Copyright(c) 2012 EPA LEB.
                <p> This is the EPA LEB LCCEditor.</p>
                <p>Python %s - PySide version %s - Qt version %s on %s""" % (VERSION,
                platform.python_version(), PySide.__version__, PySide.QtCore.__version__,
                platform.system())

class MainWindow(_QMainWindow, Ui_MainWindow, QDialog):
    """ MainWindow 
        for the LCCEditor"""
    
    @Slot(PySide.QtGui.QTableWidgetItem)
    def onValueTableDrag(self, item):
        self.itemWanted = item
    
    @Slot(PySide.QtGui.QTreeWidgetItem)
    def onClassTreeDrag(self, item):
        self.itemWanted = item
   
    global tempLccObj
    fileName = None
    itemWanted = None
    valueItemWanted = Signal(PySide.QtGui.QTableWidgetItem)
    classItemWanted = Signal(PySide.QtGui.QTreeWidgetItem)
    recentOpenFileList = None
    originalFileDirectoryPointer = None
        
    def __init__(self, parent=None):
           
        super(MainWindow, self).__init__(parent)  # Call the constructor of the Parent/inherited classes
        self.setupUi(self)
        self.changeTargetFileDirectory()
#        self.ValuesDock.setGeometry(QtCore.QRect(0, 55, 509, 368))
        self.ActionAbout.triggered.connect(self.about)
        self.ActionHelp.triggered.connect(self.helpMenu)
        self.ActionOpen.triggered.connect(self.fileOpen)
        self.ActionRestore_AutoSave.triggered.connect(self.restoreAutoSave)
        self.ActionSave.triggered.connect(self.fileSave)
        self.ActionSaveAs.triggered.connect(self.fileSaveAs)
        self.ActionNew.triggered.connect(self.new)
        self.ActionQuit.triggered.connect(self.close)
        self.ValuesAddButton.clicked.connect(self.valuesAddButton)
        self.ValuesRemoveButton.clicked.connect(self.valuesDeleteButton)
        self.ValuesIncludeAllButton.clicked.connect(self.valuesIncludeAll)
        self.CoefficientAddButton.clicked.connect(self.coefficientAddButton)
        self.ClassesInsertValuesButton.clicked.connect(self.classesInsertValuesButton)
        self.ClassesAddSiblingButton.clicked.connect(self.classesAddSiblingClassButton)
        self.ClassesAddChildButton.clicked.connect(self.classesAddChildClassButton)
        self.ClassesEditButton.clicked.connect(self.classesEditClassButton)
        self.ClassesRemoveButton.clicked.connect(self.classesRemoveClassButton)
        self.ClassesExpandCollapseButton.clicked.connect(self.classesToggleClassTreeButton)
        self.ValueTableWidget.itemPressed.connect(self.valueTableCellClicked)
        self.ValueTableWidget.itemChanged.connect(self.valueTableCellChanged)
        self.ClassesTree.itemPressed.connect(self.classesTreeCellClicked)
        self.tempLccObj = pylet.lcc.EditorLandCoverClassification()
        self.ClassesTree.itemChanged.connect(self.dropItemToClassTree)
        self.valueItemWanted.connect(self.onValueTableDrag)
        self.classItemWanted.connect(self.onClassTreeDrag)
        self.ClassesTree.setContextMenuPolicy(PySide.QtCore.Qt.CustomContextMenu)
        self.ClassesTree.customContextMenuRequested.connect(self.classTreeContextMenu)
        self.newCursor = PySide.QtGui.QCursor()
        self.ClassesTree.setCursor(self.newCursor)
        self.createActions()
        self.saveTime = QTimer(self)
        self.connect(self.saveTime, PySide.QtCore.SIGNAL("timeout(bool)"), self.autoSave)
        self.saveTime.start(constants.TimeInterval)
        self.recentOpenFileList = self.openRecentRestores()
        self.createRestoreRecentFile()
        self.CoefficientAddButton.setEnabled(False)
        self.CoefficientRemoveButton.setEnabled(False)
        self.new()
        self.initLog()
        self.logProgress("initialization")

####################
#                  #
####################

    def autoSave(self):
        """ 
            Auto-save feature   
            
        **Description:**
                
            At a predetermined amount of time, this method writes to an Xml file, 'autoSave.xml', saving the
            current work allowing the user to copy the auto-saved back to a working copy.
            
        **Arguments:**
                
            * None
            
        **Returns:**
                
            * None
                
        """
        self.logProgress(stack()[0][3])
        self.saveTime.stop()
        if not self.tempLccObj.classes.topLevelClasses and not self.tempLccObj.values:
            return
        
        outFileName = os.path.join('AutoSave', constants.AutoSaveFileName)
                   
        openFileName = open(outFileName, 'w')
        self.buildXMLTree().write(openFileName)
        openFileName.close()
        self.saveTime.start()
        self.logProgress(stack()[0][3] + " END")
    
    def restoreAutoSave(self):
        """ 
            If editor shuts down, allows the user to restore work before the shutdown
        
        **Description:**
            DETAILED_DESCRIPTION
        
        **Arguments:**
            * *INPUT_ARGUMENT_1* - ONE_LINE_DESCRIPTION_OF_TYPE_AND_PURPOSE 
            * *INPUT_ARGUMENT_2* - ONE_LINE_DESCRIPTION_OF_TYPE_AND_PURPOSE
        
        **Returns:**
            * RETURNED_OBJECT_TYPE
"""
        self.logProgress(stack()[0][3])
        
        self.saveTime.stop()
        autoSaveFileName = os.path.join('AutoSave', constants.AutoSaveFileName)

        if not os.path.isfile(autoSaveFileName):
            QMessageBox.warning(self, "No Restore File", 'No Autosaved file exists')
            return

        # Clear the dialog of loaded/created items
        self.clearLccItems()

        # Load the input file
        self.tempLccObj = pylet.lcc.EditorLandCoverClassification(autoSaveFileName)  # create a LandCoverClassification object
        self.setWindowTitle("Land Cover Classification Editor - " + os.path.basename(autoSaveFileName))
        self.displayFile()
        self.saveTime.start(constants.TimeInterval)
        self.logProgress(stack()[0][3] + " END")
                       
    def createActions(self):
        """ These are the actions for the context menu 
    
        **Description:**
            
            This method allows the user to 'right click' and bring up a context menu of the buttons for the Class
            Tree Window.  The context menu allows for another option for the user and/or faster processing  
    
        **Arguments:**
            
            * None
    
        **Returns:**
            
            * None
                
        """
        self.logProgress(stack()[0][3])
        
        self.addSiblingClassTreeClass = PySide.QtGui.QAction("Add &Sibiling", self,
                                                shortcut="alt+S",
                                                statusTip="Add Sibling Class",
                                                triggered=self.classesAddSiblingClassButton)
        self.addChildClassTreeClass = PySide.QtGui.QAction("Add &Child", self,
                                                shortcut="alt+C",
                                                statusTip="Add Child Class",
                                                triggered=self.classesAddChildClassButton)
        self.insertValueIntoTreeClass = PySide.QtGui.QAction("&Insert Value", self,
                                                shortcut="alt+I",
                                                statusTip="Insert value into tree",
                                                triggered=self.classesInsertValuesButton)
        self.editClassTreeClass = PySide.QtGui.QAction("&Edit", self,
                                                shortcut="alt+E",
                                                statusTip="Exit target class",
                                                triggered=self.classesEditClassButton)
        self.removeClassTreeClass = PySide.QtGui.QAction("&Remove", self,
                                                  shortcut="alt+D",
                                                  statusTip="Remove target class",
                                                  triggered=self.classesRemoveClassButton)
        self.logProgress(stack()[0][3] + " END")
        
    def createRestoreRecentFile(self):
        self.logProgress(stack()[0][3])
        
        if self.recentOpenFileList is None:
            return
        
        self.menOpen_Recent.clear()
        for targetFile in reversed(self.recentOpenFileList):
            menuItemRecentFile = self.menOpen_Recent.addAction(targetFile)
            menuItemRecentFile.setText(os.path.basename(targetFile))
            recentFile = lambda targetFile = targetFile: self.openRestore(targetFile)
            self.connect(menuItemRecentFile, PySide.QtCore.SIGNAL("triggered()"), recentFile)
            self.menOpen_Recent.addAction(menuItemRecentFile)
        self.logProgress(stack()[0][3] + " END")
    
    def openRestore(self, targetFile):
        self.logProgress(stack()[0][3])
        
        self.saveTime.stop()
        # Clear the dialog of loaded/created items
        self.clearLccItems()
        self.fileName = targetFile
        # Load the input file
        self.tempLccObj = pylet.lcc.EditorLandCoverClassification(self.fileName)  # create a LandCoverClassification object
        self.setWindowTitle("Land Cover Classification Editor - " + os.path.basename(self.fileName))
        self.updateRecentOpenFileList(self.fileName)
        self.displayFile()
        self.saveTime.start(constants.TimeInterval)
        self.ClassesExpandCollapseButton.setChecked(False)          
        self.logProgress(stack()[0][3] + " END")
              
    def openRecentRestores(self):
        self.logProgress(stack()[0][3])
        
        try:
            workspace = os.path.join('AutoSave', 'LCC.wsp')
            workspace = open(workspace, "r")
        except:
            print "no file openRecentRestores"
            return []
        
        bufferRecentFiles = []
            
        while(1):
            tempBuffer = workspace.readline()
            if not tempBuffer.strip():
                break
            bufferRecentFiles.append(tempBuffer.strip())
        workspace.close()        
        self.logProgress(stack()[0][3] + " END")
        return bufferRecentFiles
        
    def saveRecentRestores(self):
        self.logProgress(stack()[0][3])
        
        workspace = os.path.join('AutoSave', 'LCC.wsp')
        workspace = open(workspace, "w")
        
        for targetFile in self.recentOpenFileList:
            workspace.writelines(targetFile + '\n')
        workspace.truncate()
        workspace.close()
        self.logProgress(stack()[0][3] + " END")
        
    def updateRecentOpenFileList(self, targetFilePath):
        self.logProgress(stack()[0][3])
        
        if targetFilePath in self.recentOpenFileList:
            self.recentOpenFileList.remove(targetFilePath)
            self.recentOpenFileList.append(targetFilePath)
        elif len(self.recentOpenFileList) < 5:
            self.recentOpenFileList.append(targetFilePath)
        else:
            del self.recentOpenFileList[0]
            self.recentOpenFileList.append(targetFilePath)
            
        self.saveRecentRestores()
        self.createRestoreRecentFile()
        self.logProgress(stack()[0][3] + " END")
        
    def classTreeContextMenu(self):
        """ 
            This creates the context/right click menu for the class Tree 
            
            **Description:**
                Implementation of a context menu that allows right-click functionality.  The right-click will bring
                up quick actions for more efficient data entry.  Additional actions can be, in the future, quick added
                to context menu by following the same formats. 
            
            **Arguments:**
                
                * None
            
            **Returns:**
                
                * None
        """
        self.logProgress(stack()[0][3])
                
        contextClassTreeMenu = PySide.QtGui.QMenu(self)
        contextClassTreeMenu.addAction(self.addSiblingClassTreeClass)
        if self.tempLccObj.classes.topLevelClasses:
            contextClassTreeMenu.addAction(self.addChildClassTreeClass)        
            contextClassTreeMenu.addAction(self.editClassTreeClass)
            contextClassTreeMenu.addAction(self.insertValueIntoTreeClass)
            contextClassTreeMenu.addAction(self.removeClassTreeClass)
        contextClassTreeMenu.exec_(self.newCursor.pos())
        self.logProgress(stack()[0][3] + " END")
    
    def activateClassButtons(self):
        """ Activates Class Tree button
        
        ** Description:**

            For clarification of which buttons are active for the user, this method deactivates the Class button at 
            startup.  This method activates the buttons once a topLevelClass item is entered.
    
        **Arguments**
    
            No input arguments directly accesses buttons             
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
         
        self.ClassesAddChildButton.setEnabled(True)
        self.ClassesEditButton.setEnabled(True)
        self.ClassesInsertValuesButton.setEnabled(True)
        self.ClassesRemoveButton.setEnabled(True)
        self.ClassesExpandCollapseButton.setEnabled(True)
        self.logProgress(stack()[0][3] + " END")

    def deactivateClassButtons(self):
        """ Deactivates Class Tree Buttons
        
        ** Description:**

            For clarification of which buttons are active for the user, this method deactivates the Class button at 
            startup.  This method deactivates the buttons until a topLevelClass item is entered.
    
        **Arguments**
    
            No input arguments directly accesses buttons             
   
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])
        
        self.ClassesAddChildButton.setEnabled(False)
        self.ClassesEditButton.setEnabled(False)
        self.ClassesInsertValuesButton.setEnabled(False)
        self.ClassesRemoveButton.setEnabled(False)
        self.ClassesExpandCollapseButton.setEnabled(False)
        self.logProgress(stack()[0][3] + " END")
          
    def valueTableCellChanged(self, event):
        """ Function called by event when mainWindow value table is changed
        
        ** Description:**

            Value table signal is triggered when the mainWindow value table is altered.  The signal is connected to the 
            QTableWidgetItem and is called when it is altered.  The method calls evaluateValueOnChangeInput() to 
            determine if data changed is correct.  If not, error is triggered which results in a messageBox and undoing 
            of the information (based on information collected from valueTableCellClicked()). If valid, updates control 
            class with new data and calls the displayFile to display new data in control class.     
        
        **Arguments**
    
            * parameter:event - The event is a QTableWidgetItem
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
         
        self.message = ""
        # This is what activates the event that removes excluded from class tree
        self.evaluateValueOnChangeInput(event.row(), event.column())
        # disconnects signal so event isn't called again during item alteration
        self.ValueTableWidget.itemChanged.disconnect(self.valueTableCellChanged)
        if not self.message == "":
            QMessageBox.warning(self, "Error changed data", self.message)
            self.ValueTableWidget.item(event.row(), event.column()).setText(self.undoContainer)
            self.ValueTableWidget.setCurrentCell(event.row(), event.column())
            self.ValueTableWidget.itemChanged.connect(self.valueTableCellChanged)
            return
       
        # If changed value is name and accepted, remove leading and trailing whitespace from input name
        if event.column() == 1:
            self.ValueTableWidget.item(event.row(), 1).setText(self.ValueTableWidget.item(event.row(), 1).text().strip())

        # Reconnect signal
        self.ValueTableWidget.itemChanged.connect(self.valueTableCellChanged)
        newLandCoverValue = pylet.lcc.LandCoverValue()
        self.extractValueTableInfo(event.row(), newLandCoverValue)
        self.updateValueTableInClassObject(newLandCoverValue)
        self.displayFile()
        self.logProgress(stack()[0][3] + " END")
        
    def valueTableCellClicked(self, event):
        """ Method called when user clicks in value table dock
        
        ** Description:**

            In order to save the data that is clicked on to edit, this method stores any clicked on data so that it 
            might be restored if an error is discovered.  The original data is stored in self.undoContainer for access 
            by other methods.
    
        **Arguments**
    
            * parameter:event  - The event is a QTableWidgetItem
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
         
        self.undoContainer = self.ValueTableWidget.item(event.row(), event.column()).text()
        self.itemWanted = event
        self.logProgress(stack()[0][3] + " END")
    
    def classesTreeCellClicked(self, event):
        """ Method called when user clicks in value table dock
        
        ** Description:**

            In order to save the data that is clicked on to edit, this method stores any clicked on data so that it 
            might be restored if an error is discovered.  The original data is stored in self.undoContainer for access 
            by other methods.
    
        **Arguments**
    
            * parameter:event  - The event is a QTableWidgetItem
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
        self.itemWanted = event
        self.logProgress(stack()[0][3] + " END")
    
    def resetClassTree(self):
        """ Resets the Class Tree
        
        ** Description:**

            This method is created because PySide does not like when you delete the last item in a QTreeWidget and 
            crashes. Therefore, in order to alleviate this problem this method was created to generate a new 
            classTreeWidget object to replace the old one.  Therefore, solving the dangling pointer problem for this 
            object.  This method also sets our new object to the original parameters that we initialized it to.  
    
        **Arguments**
    
            * None             
    
        **Returns:**

            * None
            
        """
        self.logProgress(stack()[0][3])
        
        self.ClassesTree.itemChanged.disconnect(self.dropItemToClassTree)
        self.ClassesTree = None
        self.ClassesTree = PySide.QtGui.QTreeWidget(self.ClassesWidget)
        self.ClassesTree.setAcceptDrops(True)
        self.ClassesTree.setDragEnabled(False)
        self.ClassesTree.setDragDropMode(PySide.QtGui.QAbstractItemView.DragDrop)
        self.ClassesTree.setDefaultDropAction(PySide.QtCore.Qt.CopyAction)
        self.ClassesTree.setRootIsDecorated(True)
        self.ClassesTree.setHeaderHidden(False)
        self.ClassesTree.setObjectName("ClassesTree")
        self.ClassesTree.header().setDefaultSectionSize(100)
        self.ClassesTree.header().setMinimumSectionSize(20)
        self.gridLayout_4.addWidget(self.ClassesTree, 2, 0, 1, 1)
        self.ClassesTree.headerItem().setText(0, PySide.QtGui.QApplication.translate("MainWindow", "Class", None, PySide.QtGui.QApplication.UnicodeUTF8))
        self.ClassesTree.headerItem().setText(1, PySide.QtGui.QApplication.translate("MainWindow", "Description", None, PySide.QtGui.QApplication.UnicodeUTF8))
        self.ClassesTree.itemPressed.connect(self.classesTreeCellClicked)
        self.ClassesTree.itemChanged.connect(self.dropItemToClassTree)
        self.ClassesTree.setContextMenuPolicy(PySide.QtCore.Qt.CustomContextMenu)
        self.ClassesTree.customContextMenuRequested.connect(self.classTreeContextMenu)
        self.ClassesTree.setCursor(self.newCursor)
        self.logProgress(stack()[0][3] + " END")

    def dropItemToClassTree(self, event):
        """ Evaluates and identifies when data is dropped on class tree
        
        ** Description:**

            This method identifies the type of item that is dropped onto the class tree and calls the appropriate 
            function for the data type.  After the control class is properly modified this redisplays the model.
    
        **Arguments**
    
            * parameter:Event - QTreeWidgetItem        
    
        **Returns:**

            * None
            
        """
        self.logProgress(stack()[0][3])
        # disconnects signal so event isn't called again during item alteration 
        self.ClassesTree.itemChanged.disconnect(self.dropItemToClassTree)
        if isinstance(self.itemWanted, PySide.QtGui.QTableWidgetItem):
            self.dropValueToClassTree(event)
        if isinstance(self.itemWanted, PySide.QtGui.QTreeWidgetItem):
            self.dropClassToClassTree(event)

        # reconnect signal
        self.ClassesTree.itemChanged.connect(self.dropItemToClassTree)
        self.displayFile()
        self.logProgress(stack()[0][3] + " END")
    
    def dropClassToClassTree(self, event):
        """ Function that allows drag and drop of classes with the class tree.
        
        ** Description:**

            This method is called by the dropItemToClassTree function when a dropped item is a QTreeWidgetItem.  The 
            first step is to evaluate whether the dropped data is correct and in the correct location.  If incorrect
            the appropriate message box is displayed. If correct, the pointers of the root class and it's new parent
            class is changed and the former parent class pointers are removed.  The function then updates all the 
            frozensets.   
    
        **Arguments**
    
            * parameter:Event - QTreeWidgetItem        
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
        print "hi" 
        def removeValueOfParentClasses(targetClass, valueList):
            self.logProgress(stack()[0][3])
            
            for removedValue in valueList:
                targetClass.removeValueId(removedValue)
            if targetClass.parentClass:
                removeValueOfParentClasses(targetClass.parentClass, valueList)
                
        def removeClassOfParentClasses(targetClass, classList):
            self.logProgress(stack()[0][3])
            
            for removedClass in classList:
                targetClass.removeUniqueId(removedClass)
            if targetClass.parentClass:
                removeClassOfParentClasses(targetClass.parentClass, classList)
                
        def addValueOfParentClasses(targetClass, valueList):
            self.logProgress(stack()[0][3])
            
            for addValue in valueList:
                targetClass.addNewValueToUniqueValueIdsNodeList(addValue)
            if targetClass.parentClass:
                addValueOfParentClasses(targetClass.parentClass, valueList)
            
        def addClassOfParentClasses(targetClass, classList):
            self.logProgress(stack()[0][3])
            
            for addClass in classList:
                targetClass.addNewUniqueId(addClass)
            if targetClass.parentClass:
                addClassOfParentClasses(targetClass.parentClass, classList)
    
        def modifyClassValueToClassTree(event):
            self.logProgress(stack()[0][3])
            
            self.removeValueIdFromClassNode(int(self.itemWanted.text(0)), self.tempLccObj.classes[self.itemWanted.parent().text(0)])
            self.addValueToClassTree(self.tempLccObj.classes[event.parent().text(0)], event.text(0))
   
        # If event is an in hat means it is a value therefore we treat it like a value
        if self.isInt(event.text(0)):
            if not event.parent():
                self.ClassesTree.invisibleRootItem().removeChild(event)
                QMessageBox.warning(self, "Incorrect Value Placement","Must place a value in a class.")
            elif self.isInt(event.parent().text(0)):
                QMessageBox.warning(self, "Incorrect Value Placement",
                                 "Value can not have attributes.")                
            elif self.tempLccObj.classes[event.parent().text(0)].canAddValuesToClassNode():
                modifyClassValueToClassTree(event)
            else:
                QMessageBox.warning(self, "Incorrect Value Placement",
                                 "Classes can either have a class or a value as an attribute.")
        elif not event.parent():
            if not self.tempLccObj.classes[event.text(0)].parentClass:  # moving toplevel class to top level position
                storeOpenNodes = self.storeExpandedBranches(self.itemWanted)
                self.cloneNode(event, self.itemWanted)
                self.removeInvalidObjectsFromClassTree(self.itemWanted)
                tempTopLevelClassList = []
                for item in self.tempLccObj.classes.topLevelClasses:
                    tempTopLevelClassList.append(item)
                del self.tempLccObj.classes.topLevelClasses [:]
                for itemIndex in range(self.ClassesTree.topLevelItemCount()):
                    self.tempLccObj.classes.topLevelClasses.append(tempTopLevelClassList[tempTopLevelClassList.index(self.tempLccObj.classes[self.ClassesTree.topLevelItem(itemIndex).text(0)])])
                self.restoreExpansion(event, storeOpenNodes)
            else:
                uniqueValueIdList = []
                uniqueClassIdList = []
                movedClass = self.tempLccObj.classes[event.text(0)]
                originalParentClass = self.tempLccObj.classes[self.itemWanted.parent().text(0)]
                movedClass.parentClass = None
                self.tempLccObj.classes.topLevelClasses.append(movedClass)
                originalParentClass.childClasses.remove(movedClass)
                uniqueValueIdList.extend(movedClass.uniqueValueIds)
                uniqueClassIdList.extend(movedClass.uniqueClassIds)
                uniqueClassIdList.extend([movedClass.classId])
                removeValueOfParentClasses(originalParentClass, uniqueValueIdList)
                removeClassOfParentClasses(originalParentClass, uniqueClassIdList)
        else:
            if self.isInt(event.parent().text(0)):
                QMessageBox.warning(self, "Incorrect Value Placement",
                                 "Value can not have class as attributes.")                
            elif self.tempLccObj.classes[event.parent().text(0)].hasValues():
                QMessageBox.warning(self, "Incorrect Value Placement",
                                 "Classes can either have a class or a value as an attribute.")
            elif not self.tempLccObj.classes[event.text(0)].parentClass: # Moved object from top level
                newParentClass = self.tempLccObj.classes[event.parent().text(0)]
                uniqueValueIdList = []
                uniqueClassIdList = []
                movedClass = self.tempLccObj.classes[event.text(0)]
                movedClass.parentClass = newParentClass
                newParentClass.childClasses.append(movedClass)
                self.tempLccObj.classes.topLevelClasses.remove(movedClass)
                uniqueValueIdList.extend(movedClass.uniqueValueIds)
                uniqueClassIdList.extend(movedClass.uniqueClassIds)
                uniqueClassIdList.extend([movedClass.classId])
                addValueOfParentClasses(newParentClass, uniqueValueIdList)
                addClassOfParentClasses(newParentClass, uniqueClassIdList)   
            else:
                parentClass = self.tempLccObj.classes[event.parent().text(0)]
                uniqueValueIdList = []
                uniqueClassIdList = []
                movedClass = self.tempLccObj.classes[event.text(0)]
                originalParentClass = self.tempLccObj.classes[self.itemWanted.parent().text(0)]
                movedClass.parentClass = parentClass
                parentClass.childClasses.append(movedClass)
                originalParentClass.childClasses.remove(movedClass)
                uniqueValueIdList.extend(movedClass.uniqueValueIds)
                uniqueClassIdList.extend(movedClass.uniqueClassIds)
                uniqueClassIdList.extend([movedClass.classId])
                removeValueOfParentClasses(originalParentClass, uniqueValueIdList)
                removeClassOfParentClasses(originalParentClass, uniqueClassIdList)
                addValueOfParentClasses(parentClass, uniqueValueIdList)
                addClassOfParentClasses(parentClass, uniqueClassIdList)

        self.logProgress(stack()[0][3] + " END")

    def dropValueToClassTree(self, event):
        """ Evaluation method for the drop value on classTree.
        
        ** Description:**

         This method is called when itemChanged signal on classTree is triggered.  If there is nothing in classTree
         except for the dropValue it is an error and a potential PySide crash situation.  This is when we call 
         resetClassTree() to alleviate problem (see method).  This data is error checked for valid structural 
         consistency.  If data is valid, then we determine the correlated information of value and update in control 
         class.  The method then displays the new control class.
    
        **Arguments**
    
            * parameter:event - The event is a QTreeWidgetItem
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])
        
        if not self.tempLccObj.classes.topLevelClasses:
            self.resetClassTree()
            return
        if not event.parent():
            QMessageBox.warning(self, "Incorrect Value Placement",
                                 "Values can only be applied as attributes to classes.")   
        elif self.isInt(event.parent().text(0)):
            QMessageBox.warning(self, "Incorrect Value Placement", "Class values should not have attributes.")
        elif not self.tempLccObj.classes[event.parent().text(0)].canAddValuesToClassNode():
            QMessageBox.warning(self, "Incorrect Value Placement",
                                 "Classes can either have a class or a value as an attribute.")
        else:
            if self.isInt(event.text(0)):
                tempId = int(event.text(0))
            else:
                for valueIdFromEvent in self.tempLccObj.values.keys():
                    if self.tempLccObj.values[valueIdFromEvent].name == event.text(0):
                        tempId = valueIdFromEvent
                        break 
            if self.tempLccObj.classes[str(event.parent().text(0))].isValueInSet(tempId):
                QMessageBox.warning(self, "Value already in class.", "Value already exists in the class.")
            else:
                self.addValueToClassTree(self.tempLccObj.classes[str(event.parent().text(0))], tempId)
        self.logProgress(stack()[0][3] + " END")

        return
    
    def closeEvent(self, event):
        """ Function the prompts user when quitting the editor.  
        
        ** Description:**

            This method is an overloaded function.  It is called when the close command is triggered, regardless of 
            the source of the close command.    It initiates a QMessagebox that asks the user if they want to quit or 
            not to insure that the user doesn't quit accidentally. 
            
        **Arguments**
    
            * None        
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])
        
        reply = QMessageBox.question(self, "Save File", "Are you sure you want to quit the editor?", \
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            event.ignore()
        else:
            self.clearLccItems()
            event.accept()

        self.logProgress(stack()[0][3] + " END")
                      
    def about(self):
        """
            A message popup box appears with the About message.
            
        **Description:**
            Once the About menu item is selected from the LCCEditor, the About message, provided above, pops up on the
            screen in a message box
                    
        **Arguments**
            
            * None
                        
        **Returns:**
        
            * None
            
        """ 
        self.logProgress(stack()[0][3])
               
        # The QMessageBox generates a pop up box.  Provided are the Title and message arguments
        QMessageBox.about(self, TITLE, ABOUT_MESSAGE)

        self.logProgress(stack()[0][3] + " END")
    
    def helpMenu(self):
        """ 
            Opens LLCEditor Help file
                
        ** Description:**
        
            Once the Help menu item is selected, the Help file is opened and allows the users to search for help in
            the documentation.
                        
        **Arguments**
            
            * None
                        
        **Returns:**
        
            * None
        """
        self.logProgress(stack()[0][3])
        
        # Provides the directory name of the path of the running file + the name of the help file.
        pathname = os.path.dirname(_sys.argv[0]) + "\help.chm"
        # Starts the file at the specified path
#        os.startfile(pathname)

        self.logProgress(stack()[0][3] + " END")
    
    def clearLccItems(self):
        """ 
            Clears the display/GUI in preparation of receiving new information to display.
                
        ** Description:**
        
            All of the trees, Values and Classes, and Metatdata information are cleared out of the display in 
            preparation of receiving the new display data when a new file is opened or data is changed in the LCCEditor
            GUI 
            
        **Arguments**
            
            * None             
            
        **Returns:**
        
            * None
                    
        """
        self.logProgress(stack()[0][3])
                
        self.ValueTableWidget.clear()
        self.setValueParametersTable()
        self.CoefficientTableWidget.clear()
#        self.ClassesTree.clear()
        self.resetClassTree()
        self.MetadataNameLineEdit.clear()                
        self.MetadataDescriptionTextEdit.clear() 

        self.logProgress(stack()[0][3] + " END")
    
    def new(self):
        """ 
            Clears the display in preparation of receiving new information to display 
                
        ** Description:**
        
             Once the New menu item is selected the trees, Values and Classes, and the Metadata, description and name,
             are cleared.  A new Land Cover Classification object is created and the filename is set to None.  
             Currently, coefficients are directly hard coded due to dynamic coefficients not being implemented yet.  
             
        **Arguments**
            
            * None
                        
        **Returns:**
        
            * None
                    
        """
        self.logProgress(stack()[0][3])
        
        self.saveTime.stop()
        self.clearLccItems()
        self.tempLccObj = pylet.lcc.EditorLandCoverClassification()
        tempCoefficient = pylet.lcc.LandCoverCoefficient()
        tempCoefficient.populateCoefficient("IMPERVIOUS", "Percent Cover Total Impervious Area", "PCTIA", "P")
        self.tempLccObj.coefficients["IMPERVIOUS"] = tempCoefficient
        tempCoefficient = pylet.lcc.LandCoverCoefficient()
        tempCoefficient.populateCoefficient("NITROGEN", "Estimated Nitrogen Loading Based on Land Cover", "N_Load", "A")
        self.tempLccObj.coefficients["NITROGEN"] = tempCoefficient
        tempCoefficient = pylet.lcc.LandCoverCoefficient()
        tempCoefficient.populateCoefficient("PHOSPHORUS", "Estimated Phosphorus Loading Based on Land Cover", "P_Load", "A")
        self.tempLccObj.coefficients["PHOSPHORUS"] = tempCoefficient
        self.deactivateClassButtons()
        self.fileName = None
        self.setWindowTitle("Land Cover Classification Editor")        
        self.displayFile()
        self.saveTime.start(constants.TimeInterval)
        self.ClassesExpandCollapseButton.setChecked(False)

        self.logProgress(stack()[0][3] + " END")
        
    def changeTargetFileDirectory(self):
        """
        """
        self.originalFileDirectoryPointer = os.path.dirname(os.path.abspath(_sys.argv[0]))
        dirPath = self.originalFileDirectoryPointer.split('\\')
        if dirPath[1] == "Projects":
            newWorkingPath = os.path.join(dirPath[0], '\\', dirPath[1], 'ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications/')
        elif "ToolboxSource" in dirPath:
            rootLocation = dirPath.index('ToolboxSource')
            buildString = ""
            for index, iterator in enumerate(dirPath):
                buildString = buildString + iterator
                if index == rootLocation:
                    break
                buildString = buildString + '\\'
            newWorkingPath = os.path.join(buildString,'LandCoverClassifications/')
        else:
            #This cannot find the path that we need
            print "no correct file path found"
        
        os.chdir(newWorkingPath)
        if not os.path.isdir('AutoSave'):
            os.mkdir('AutoSave')
                    
    def fileOpen(self):
        """ Opens an xml file for viewing in the display.
                
        ** Description:**
        
             Once the Open menu item is selected, and the file is selected,  the filename is returned.  All tree and
             meta items are cleared.  A new Land Cover Classification is opened  and the file is displayed in the GUI 
            
        **Arguments**
            
            * None
                        
        **Returns:**
        
            * None
                    
        """ 
        self.logProgress(stack()[0][3])
        
        self.saveTime.stop()
                
        # gets the file name
        self.fileName = QFileDialog.getOpenFileName(self, "Open File",
            os.getcwd(), "XML files (*.xml)")[0]  # might have to use '/home')

        # Exit if user selected cancel in the dialog
        if not self.fileName:
            return
        # Clear the dialog of loaded/created items
        self.clearLccItems()

        # Load the input file
        self.tempLccObj = pylet.lcc.EditorLandCoverClassification(self.fileName)  # create a LandCoverClassification object
        self.setWindowTitle("Land Cover Classification Editor - " + os.path.basename(self.fileName))
        self.updateRecentOpenFileList(self.fileName)
        self.displayFile()
        self.saveTime.start(constants.TimeInterval)
        self.ClassesExpandCollapseButton.setChecked(False)        

        self.logProgress(stack()[0][3] + " END")
        
    def findCorespondingLabel(self, idValue):
        """ 
            Finds the value id in the valueTree and returns the corresponding Label
                
        ** Description:**
        
             Given a value id this method returns the corresponding label for use in the displayFile method. 
            
        **Arguments**
            
            * parameter:idValue - Numerical value used to match valueId.
            
        **Returns:**
        
            * value.name - The name associated with the valueId.
            * Returns error message if not found.
                    
        """         
#        self.logProgress(stack()[0][3])
               
        for value in self.tempLccObj.values.values():  # creates value for iterator
            assert isinstance(value, pylet.lcc.LandCoverValue)  # activates auto-completion   
            try:
                         
                if value.valueId == idValue:
                    return value.name 
                           
            except:
                pass

#        self.logProgress(stack()[0][3] + " END")
            
        return "No Description"
   
    def displayFile(self):
        """ 
            Displays the contents of the newly opened file or redraws the changed display to the GUI 
                
        ** Description:**
        
             This method clears the GUI by calling the clearLccItems().  Then displays to the GUI the values from the
             valueTree, the classes from the classTree and the metadata name and description.  For the classes, we 
             cycle through each topLevelClasses checking the descendants and displaying before moving on to the next 
             topLevelclass.
            
        **Arguments**
            
            * None
                        
        **Returns:**
        
            * None
                    
        """         
        self.logProgress(stack()[0][3])

        def displayValuesTable():
            # set parameters for ValueTableWidget becuase qml file from QT creator dows no allow
            self.setValueParametersTable()
            self.ValueTableWidget.itemChanged.disconnect(self.valueTableCellChanged)
            
            # Load values
            idList = list(self.tempLccObj.values.keys())
            idList.sort()
            
            # Sorting the valud ids when displaying to allow for correct insertion in to the display
            for index, idValue in enumerate(idList):
                populateId = PySide.QtGui.QTableWidgetItem(str(idValue))
                populateId.setFlags(Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable)
                self.ValueTableWidget.setItem(index, 0, populateId)
            
            loopInteger = 0
            tempLCV = pylet.lcc.LandCoverValue()
            
            while loopInteger < len(self.tempLccObj.values.keys()):
                tempLCV = self.tempLccObj.values[int(self.ValueTableWidget.item(loopInteger, 0).text())]
                populateName = PySide.QtGui.QTableWidgetItem(str(tempLCV.name))
                populateExclusion = PySide.QtGui.QTableWidgetItem()
                populateExclusion.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                if(tempLCV.excluded):
                    populateExclusion.setCheckState(PySide.QtCore.Qt.Checked)
                else:
                    populateExclusion.setCheckState(PySide.QtCore.Qt.Unchecked)
                    
                self.ValueTableWidget.setItem(loopInteger, 1, populateName)
                self.ValueTableWidget.setItem(loopInteger, 2, populateExclusion)
    
                column = 3
                while column < len(self.tempLccObj.coefficients.keys()) + 3:
                    coffTableItem = PySide.QtGui.QTableWidgetItem(str(
                        tempLCV._coefficients[self.ValueTableWidget.horizontalHeaderItem(column).text()].value))
                    coffTableItem.setTextAlignment(Qt.AlignRight)
                    coffTableItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
                    self.ValueTableWidget.setItem(loopInteger, column, coffTableItem)
                    column = column + 1
                loopInteger = loopInteger + 1
                
            # Auto adjust Value table based on contents
            self.ValueTableWidget.resizeColumnsToContents()
    
            self.ValueTableWidget.itemChanged.connect(self.valueTableCellChanged)

        def displayCoefficientsTable():
            self.logProgress(stack()[0][3])

            self.setCoefficientParametersTable()
            
            for index, coefficientObj in enumerate(self.tempLccObj.coefficients.values()):
                populateCoeffId = PySide.QtGui.QTableWidgetItem()
                populateCoeffName = PySide.QtGui.QTableWidgetItem()
                populateCoeffFieldName = PySide.QtGui.QTableWidgetItem()
                populateCoeffAPMethod = PySide.QtGui.QTableWidgetItem()
                populateCoeffId.setText(coefficientObj.coefId)
                populateCoeffName.setText(coefficientObj.name)
                populateCoeffFieldName.setText(coefficientObj.fieldName)
                populateCoeffAPMethod.setText(coefficientObj.apMethod)
                
                # Locks column contents from being modified
                populateCoeffId.setFlags(Qt.NoItemFlags)
                populateCoeffName.setFlags(Qt.NoItemFlags)
                populateCoeffFieldName.setFlags(Qt.NoItemFlags)
                populateCoeffAPMethod.setFlags(Qt.NoItemFlags)
                
                self.CoefficientTableWidget.setItem(index, 1, populateCoeffName)
                self.CoefficientTableWidget.setItem(index, 2, populateCoeffFieldName)
                self.CoefficientTableWidget.setItem(index, 3, populateCoeffAPMethod)
                self.CoefficientTableWidget.setItem(index, 0, populateCoeffId)
            
            # Auto adjust Coefficient table based on contents
            self.CoefficientTableWidget.resizeColumnsToContents()
                
        def displayMetaData():
            self.logProgress(stack()[0][3])

            # Load Metadata Name
            metadataName = self.tempLccObj.metadata.name
            self.MetadataNameLineEdit.setText(metadataName)
            
            # Load Metadata Description
            metadataDescription = self.tempLccObj.metadata.description
            self.MetadataDescriptionTextEdit.setPlainText(metadataDescription)
            
        def displayClassesTree():
            self.logProgress(stack()[0][3])

            indent = "    "

            # Load classes
            def printDescendentClasses(landCoverClass, item_0, indentUnit, indentLevel):
                """ Searches and displays the descendants of the current class
            
                ** Description:**
                
                    Once the current class is selected this method recursively transverses the class tree checking for
                    child to display.
                    
                **Arguments** 
                    
                    * topLevelClass - the root or lowest class item
                    * QTreeWidgetItem
                    * Indent - the indent spacing unit amount
                    * IndentLevel - starting at the second level and incrementing
                                    
                **Returns:**
                
                    * None
                            
                """
#                self.logProgress(stack()[0][3])
 
                try:
                    for childClass in landCoverClass.childClasses:
                        assert isinstance(childClass, pylet.lcc.EditorLandCoverClass)
                        
                        # childClass
                        item_1 = PySide.QtGui.QTreeWidgetItem(item_0)
                        item_1.setFont(0, boldFont)
                        item_1.setText(0, childClass.classId)  # set id
                        item_1.setFont(1, boldFont)
                        item_1.setText(1, childClass.name)  # set name
                             
                        childValueList = []
                        childValueList.extend(childClass.childValueIds)
                        childValueList.sort()
                                  
                        for childValueId in childValueList:
                            if self.tempLccObj.values[childValueId].excluded:  # delete#
                                continue  # delete#
                            childItem = PySide.QtGui.QTreeWidgetItem(item_1)
                            childItem.setFont(0, smallFont)
                            childItem.setText(0, str(childValueId))
                            childItem.setFont(1, smallFont)
                            childItem.setText(1, self.findCorespondingLabel(childValueId))
                        printDescendentClasses(childClass, item_1, indentUnit, indentLevel + 1)
                except:
                    print "big time error"
            self.ClassesTree.itemChanged.disconnect(self.dropItemToClassTree)
            self.ClassesTree.setSortingEnabled(False)
       
            boldFont = QFont("Ariel", 10, QFont.Bold)
            smallFont = QFont("Ariel", 10)
            
            if not self.tempLccObj.classes.topLevelClasses == None:
                self.activateClassButtons()
                for topLevelClass in self.tempLccObj.classes.topLevelClasses:
                    assert isinstance(topLevelClass, pylet.lcc.EditorLandCoverClass)
                    
                    try:
                        item_0 = PySide.QtGui.QTreeWidgetItem(self.ClassesTree)

                        item_0.setFont(0, boldFont)
                        item_0.setText(0, str(topLevelClass.classId))
                        item_0.setFont(1, boldFont)
                        item_0.setText(1, str(topLevelClass.name))
                        if topLevelClass.childValueIds:
                            childValueList = []
                            childValueList.extend(topLevelClass.childValueIds)
                            childValueList.sort()
                                      
                            for childValueId in childValueList:
                                if self.tempLccObj.values[childValueId].excluded:  # delete#
                                    continue  # delete#
                                childItem = PySide.QtGui.QTreeWidgetItem(item_0)
                                childItem.setText(0, str(childValueId))
                                childItem.setText(1, self.findCorespondingLabel(childValueId))
                    except:
                        pass
                    
                    printDescendentClasses(topLevelClass, item_0, indent, 2)
            
            self.ClassesTree.itemChanged.connect(self.dropItemToClassTree)

        # Main controls display file    
        
            
        # store all the expanded nodes for later re-expansion
        storeOpenNodes = self.storeExpandedBranches(None)


        # Clears out Model view
        self.clearLccItems()
        
        if self.tempLccObj.values:
            displayValuesTable()
            
        if self.tempLccObj.coefficients:
            displayCoefficientsTable()
        
        if self.tempLccObj.metadata.doesMetaDataExist():
            displayMetaData()
            
        if self.tempLccObj.classes:
            displayClassesTree()

            self.restoreExpansion(None, storeOpenNodes)
        
        self.logProgress(stack()[0][3] + " END")
    
    def getLccSize(self):
        self.logProgress(stack()[0][3])

        sumLcc = self.tempLccObj.classes.__sizeof__()
        for classIterator in self.tempLccObj.classes.iteritems():
            sumLcc += classIterator[1].getSize()

        self.logProgress(stack()[0][3] + " END")
        
        return sumLcc
                      
    def fileSave(self):
        """ Save the file if predefined file path is selected, otherwise determine new file path.
        
        ** Description:**
        
             This method evaluates where a current file path is selected by evaluating fileName.  If there is a current
             file path, the file is open and the current control class data is converted to XML format via 
             buildXMLTree().  If no path is selected, then dialog is called to determine new path. 
            
        **Arguments**
            
            * None
                        
        **Returns:**
        
            * None
                    
        """
        self.logProgress(stack()[0][3])
 
        if not self.fileName:
            outFileName = QFileDialog.getSaveFileName(self, 'Save File', os.getcwd(), "XML files (*.xml)")[0]
            if not outFileName:
                return
            self.fileName = outFileName
        else:
            outFileName = unicode(self.fileName)
            if S_IMODE(os.stat(outFileName).st_mode) == 292:
                QMessageBox.about(self, "Read-Only File", "File is Read-Only, can not save file!")
                return
            reply = QMessageBox.question(self, "Save File", "Are you sure you want to save file?", \
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
             
        openFileName = open(outFileName, 'w')
        self.buildXMLTree().write(openFileName, encoding="UTF-8")
        openFileName.close()
        self.setWindowTitle("Land Cover Classification Editor - " + os.path.basename(self.fileName))
        self.updateRecentOpenFileList(self.fileName)

        self.logProgress(stack()[0][3] + " END")

    def fileSaveAs(self):
        """ 
            Save the file to new file path.
        
        ** Description:**

             This method determines new file path, converts control class to XML format and saves XML format in file
             path.  This method also updates fileName with new file path.  
    
        **Arguments**
    
            * None            
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        if not self.fileName:
            fileName = "temp.xml"
        else:
            fileName = self.fileName
        outFileName = QFileDialog.getSaveFileName(self, 'Save As File', fileName, "XML files (*.xml)")[0]
        if not outFileName:
            return
        if os.path.isfile(outFileName) and S_IMODE(os.stat(str(outFileName)).st_mode) == 292:
            QMessageBox.about(self, "Read-Only File", "File is Read-Only, can not save file!")
            return
        self.fileName = outFileName
        outFileName = open(outFileName, 'w')        
        self.buildXMLTree().write(outFileName, encoding="UTF-8")
        outFileName.close()
        self.setWindowTitle("Land Cover Classification Editor - " + os.path.basename(self.fileName))  
        self.updateRecentOpenFileList(self.fileName)      

        self.logProgress(stack()[0][3] + " END")
        
    def buildXMLTree(self):
        """ 
            Builds XML tree from control class.
        
        ** Description:**

             This method utilizes the functionality of ElementTree.  It builds elements based on control class and
             builds xml structure based on the information of the control class. The constants are imported from 
             pylet/pylet/lcc/constants.py and their use allows for cross platform compatibility.   
    
        **Arguments**
    
            * None
            
        **Returns:**

            * Built XML tree
            
        """  
        self.logProgress(stack()[0][3])

        def indent(elem, level=0):
#            self.logProgress(stack()[0][3])

            i = "\n" + level * "    "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "    "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    indent(elem, level + 1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i
        # create the root element
        root = Element('lccSchema')
        tree = ElementTree(root)
        
        # create metadata nodes
        meta = Element(constants.XmlElementMetadata)
        root.append(meta)
        metaName = Element(constants.XmlElementMetaname)
        metaName.text = str(self.MetadataNameLineEdit.text())
        meta.append(metaName)
        metaDesc = Element(constants.XmlElementMetadescription)
        metaDesc.text = str(self.MetadataDescriptionTextEdit.toPlainText())
        meta.append(metaDesc)

        # add the coefficients text and coefficients
#         coeffText = etree.Comment("""    
#         * The Coefficients node contains coefficients to be assigned to values.
#         * 
#         * Id - text, unique identifier
#         * Name - text, name describing coefficient
#         * fieldName - text, name of field to be created for output
#         * apMethod - text, Percentage or Area Percentage
#     """)
        coeffText = etree.Comment(""" 
        * The coefficients node contains coefficients to be assigned to values.
           
        * REQUIRED ATTRIBUTES
        * Id - text, unique identifier
        * Name - text, word or phrase describing coefficient
        * fieldName - text, name of field to be created for output
        * apMethod - text, "P" or "A", designates "P"ercentage or per unit "A"rea calculation routine
    """)
        root.append(coeffText)
        coeffs = Element(constants.XmlElementCoefficients)
        
        for coef in self.tempLccObj.coefficients:
            tempid = self.tempLccObj.coefficients[str(coef)].coefId
            tempname = self.tempLccObj.coefficients[str(coef)].name
            tempfieldname = self.tempLccObj.coefficients[str(coef)].fieldName
            tempAPMethod = self.tempLccObj.coefficients[str(coef)].apMethod
            coeff = Element(constants.XmlElementCoefficient, Id=tempid, Name=tempname, fieldName=tempfieldname, apMethod=tempAPMethod)
            coeffs.append(coeff)
        root.append(coeffs)

        # add the value text and values
#         valText = etree.Comment("""
#         * The "values" node defines the full set of values that can exist in a landcover raster
#         * The "excluded" attribute is used to exclude values from the total, excluded=false is the default
#         * Actual excluded values are always treated as excluded=true, cannot be used in classes, and should not be listed here. 
#     """)
        valText = etree.Comment(""" 
        * The values node defines the full set of values that can exist in a land cover raster.
        
        * REQUIRED ATTRIBUTES
        * Id - integer, raster code
        *
        * OPTIONAL ATTRIBUTES
        * Name - text, word or phrase describing value
        * excluded - boolean, "true" or "false" or "1" or "0"
        *          - used to exclude values from effective area calculations
        *          - excluded=false is the default 
        
        * A value element can optionally contain one or more coefficient elements

        * REQUIRED COEFFICIENT ATTRIBUTES
        * Id - text, must match an Id attribute from a coefficients node element
        * value - decimal, weighting/calculation factor
    """)
        root.append(valText)
        values = Element(constants.XmlElementValues)
        # get the values
        for key in sorted(self.tempLccObj.values.iteritems(), key=operator.itemgetter(0)):
            valDict = {}
            valDict[constants.XmlAttributeId] = str(key[1].valueId)
            valDict[constants.XmlAttributeName] = str(key[1].name)
            if (key[1].excluded):
                valDict[constants.XmlAttributeNodata] = 'true'
            val = Element(constants.XmlAttributeValue, attrib=valDict)
            values.append(val)
        # get the coefficients for each value
            for coef in key[1]._coefficients:
                coefDict = {}
                coefDict[constants.XmlAttributeId] = key[1]._coefficients[str(coef)].coefId
                if key[1]._coefficients[str(coef)].value == 0.0:
                    coefDict[constants.XmlAttributeValue] = "0.0"
                else:
                    coefDict[constants.XmlAttributeValue] = str(key[1]._coefficients[str(coef)].value)
                if coefDict["value"] == "":
                    pass
                coefe = Element(constants.XmlElementCoefficient, attrib=coefDict)
                val.append(coefe)
        root.append(values)
        if self.tempLccObj.classes.topLevelClasses == None:
            indent(tree.getroot())
            return tree
        # add the class text and the class nodes
#         classText = etree.Comment("""
#         * The "classes" node contains values grouped into classes.
#         * A class can contain either values or classes but not both types
#         * Values contain only an id which refers to a value in values node.
#         * The id attribute is used for the root of the field name in the output(for example %forest would be P + for = Pfor)
#         * Two classes with the same id are not allowed.
#         * Special class attributes:
#             - onSlopeVisible: Make available in "On Slope" metric category, default is false
#             - overwriteField:  if present, it overides default "Land Cover Proportions" field name with the supplied value
#     """)
        classText = etree.Comment("""
        * The classes node contains values from a land cover raster grouped into one or more classes.
    
        * REQUIRED ATTRIBUTES
        * Id - text, unique identifier, also used for automated generation of output field name
        
        * OPTIONAL ATTRIBUTES
        * Name - text, word or phrase describing class
        * filter - text, a string of one or more tool name abbreviations separated by a ";"
        *        - possible abbreviations are: lcp, rlcp, lcosp, splcp, and caeam
        *        - used to exclude the class from the selectable classes in the tool's GUI
        * xxxxField - text, overrides ATtILA-generated field name for output
        *           - where xxxx equals a tool name abbreviation
        *           - possible abbreviations are: lcp, rlcp, lcosp, splcp, and caeam
        *           - a separate xxxxField attribute can exist for each tool

        * A class can contain either values or classes but not both types.
        * Value elements contain only an Id attribute which refers to a value in a raster.
        * Values tagged as excluded="true" in the values node should not be included in any class.
    """)
        root.append(classText)
        classes = Element('classes')
        root.append(classes)
        # function to find child classes of the parent classes
        def printDescendentClasses(landCoverClass, classE):
#            self.logProgress(stack()[0][3])

            if landCoverClass.childClasses:
                for childClass in landCoverClass.childClasses:
                    assert isinstance(childClass, pylet.lcc.EditorLandCoverClass)
                    # childClass
                    clasDict = {}
                    clasDict[constants.XmlAttributeId] = str(childClass.classId)
                    clasDict[constants.XmlAttributeName] = str(childClass.name)
                    for field in self.tempLccObj.overwriteFieldsNames:
                        if childClass.classoverwriteFields[field]:
                            clasDict[field] = childClass.classoverwriteFields[field]
                    clasDict[constants.XmlAttributeFilter] = "" 
                    childClas = Element(constants.XmlElementClass, attrib=clasDict)
                    classE.append(childClas)
                    for childValueId in sorted(childClass.childValueIds):
                        if self.tempLccObj.values[childValueId].excluded:
                            continue
                        childVal = Element(constants.XmlElementValue, Id=str(childValueId))
                        childClas.append(childVal)
                    printDescendentClasses(childClass, childClas)
            else:
                return
        for clas in self.tempLccObj.classes.topLevelClasses:
            clasDict = {}
            clasDict[constants.XmlAttributeId] = str(clas.classId)
            clasDict[constants.XmlAttributeName] = str(clas.name)
            for field in self.tempLccObj.overwriteFieldsNames:
                if clas.classoverwriteFields[field]:
                    clasDict[field] = clas.classoverwriteFields[field]
            clasDict[constants.XmlAttributeFilter] = ""
            classE = Element(constants.XmlElementClass, attrib=clasDict)
            classes.append(classE)
            for childValueId in clas.childValueIds:
                if self.tempLccObj.values[childValueId].excluded:
                    continue
                childVal = Element(constants.XmlElementValue, Id=str(childValueId))
                classE.append(childVal)
            printDescendentClasses(clas, classE)                

        # indent the output correctly and the write to file
        indent(tree.getroot())
        

        self.logProgress(stack()[0][3] + " END")

        return tree
     
    def valuesAddButton(self):             
        """ 
            Add value button allows the user to enter in new IDs, Values and Excluded values
        
        ** Description:**

            This method is triggered by clicking valueAdd button.  It calls addValueTableIdPopupWindow() to facilitate 
            the entering of data.  The input data is directly stored in tempLCVObjectList by the dialog and the 
            dialog does the error checking. The data is updated to the control class and the control class is 
            redisplayed if the dialog was valid.  
    
        **Arguments**
    
            * None
                
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        self.dialogTitle = "Add Value Dialog"  # Variable that dialog accesses for title.
        self.tempLCVObjectList = []  # Variable that dialog accesses to store valid data
        self.addValueDialog = AddValueTableIdPopupWindow(self).exec_()  # Calls dialog: errors are evaluated in dialog 
        if self.addValueDialog == 0:
            return
        for newValueIdObject in self.tempLCVObjectList:
            self.tempLccObj.values[newValueIdObject.valueId] = newValueIdObject  # populate the keys with the objects
        self.displayFile()  # updates GUI to display correct values

        self.logProgress(stack()[0][3] + " END")
                                            
    def valuesDeleteButton(self):
        """
            The delete value button deletes value entries from the valueTable model
        
        ** Description:**

             This method has two different directions depending on whether a value is selected in a value tree or not.
             If nothing is selected, then removeValuePoppWindow dialog is called.  Where multiple values may be 
             selected for removal, and selected values are removed from control class.  If something in the valueTable
             is selected, this method appends the selected value to a list that is removed from the valueTable, then 
             removes the value from the control class. This method, after selected values are removed from the value
             control class, removes all the values from the control class classTree.  When finished redisplays 
             updated control class.
             
        **Arguments**
    
            * None             
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        self.dialogTitle = "Remove Value(s) Dialog"
        self.removalSelection = []
        if not self.tempLccObj.values.keys():
            QMessageBox.warning(self, "Values IDs", "Currently there are no Value id's") 
            return 
        # checks to see if item in value tree is selected
        if self.ValueTableWidget.currentItem():
            self.removalSelection.append(int(self.ValueTableWidget.item(self.ValueTableWidget.currentRow(), 0).text()))
            del self.tempLccObj.values[int(self.ValueTableWidget.item(self.ValueTableWidget.currentRow(), 0).text())]   
        else:
            self.callDialog = RemoveValuePopupWindow(self)
            dialogValid = self.callDialog.exec_()
            if dialogValid == 0:
                return
            for key in self.removalSelection:
                del self.tempLccObj.values[key]
        for removedId in self.removalSelection:
            self.removeValueIdFromClassTree(removedId, self.tempLccObj.classes.topLevelClasses)
        self.displayFile()

        self.logProgress(stack()[0][3] + " END")

    def valuesIncludeAll(self):
        """ 
            This button unchecks all the excluded (X) boxes
        
        ** Description:**

             The method unchecks all the excluded box to all the values to be seen in the classTree. 
    
        **Arguments**
    
            * None            
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        for valueObj in self.tempLccObj.values.values():
            valueObj.excluded = False
        self.displayFile()

        self.logProgress(stack()[0][3] + " END")
 
    def setValueParametersTable(self):
        """ 
            Sets the valueTable parameters for display in the model
        
        ** Description:**
            This method provides the parameters for the valueTable model.  It assigns the column heading for the first
            three columns and then dynamically assigns the remaining columns based on the coefficients table.   
             
        **Arguments**
        
            * None            
    
        **Returns:**
        
            * None
            
        """ 
        self.logProgress(stack()[0][3])
 
        # creation of parameters...therefore must be implemented outside build file ....   :(
        columncount = 3
        headerLabels = ["Value", "Description", "X"]
        if not self.tempLccObj.coefficients == None:
            headerLabels.extend(self.tempLccObj.coefficients.keys())
            columncount = columncount + len(self.tempLccObj.coefficients.keys())
        self.ValueTableWidget.setSortingEnabled(False)
        self.ValueTableWidget.setRowCount(len(self.tempLccObj.values.keys()))
        self.ValueTableWidget.setColumnCount(columncount)
        self.ValueTableWidget.setSelectionMode(PySide.QtGui.QAbstractItemView.SingleSelection)
        self.ValueTableWidget.setColumnWidth(0, 50)
        self.ValueTableWidget.setColumnWidth(1, 225)
        self.ValueTableWidget.setColumnWidth(2, 15)
        self.ValueTableWidget.resizeColumnToContents(2)
        index = len(self.tempLccObj.coefficients.keys()) + 3
        col = 3
        while col < index:
            self.ValueTableWidget.setColumnWidth(col, 150)
            col = col + 1    
        self.ValueTableWidget.setHorizontalHeaderLabels(headerLabels)
        self.ValueTableWidget.verticalHeader().setVisible(False)

        self.logProgress(stack()[0][3] + " END")
     
    def extractValueTableInfo(self, row, newLandCoverValue):
        """ 
            Accesses the valueTable model and extracts data into new valueLccObject 
        
        ** Description:**

             This method is called by valueTableCellChanged whenever an item is changed in the valueTableWidget.  It 
             also extracts the data from the valueTable model and puts it into the passed LLCValueObject
    
        **Arguments**
    
            * parameter:row - int (Current value of selected row in value table)
            * parameter:newLandCoverValue - LCC value object (To hold extracted data)             
    
        **Returns:**

            * Returns a LandCoverValue object 
            
        """
        self.logProgress(stack()[0][3])
  
        newLandCoverValue.valueId = int(self.ValueTableWidget.item(row, 0).text())
        newLandCoverValue.name = self.ValueTableWidget.item(row, 1).text() 
        if self.ValueTableWidget.item(row, 2).checkState() == Qt.Checked:
            newLandCoverValue.excluded = True
        else:
            newLandCoverValue.excluded = False       
        column = 3
        while column < len(self.tempLccObj.coefficients.keys()) + 3:
            tempholder = self.ValueTableWidget.horizontalHeaderItem(column).text()
            newCoefficientObj = pylet.lcc.LandCoverCoefficient()
            newCoefficientObj.deepCopyCoefficient(self.tempLccObj.coefficients[tempholder])
            newCoefficientObj.populateCoefficientValue(self.ValueTableWidget.item(row, column).text())
            newLandCoverValue._coefficients[tempholder] = newCoefficientObj
            column += 1         

        self.logProgress(stack()[0][3] + " END")
 
        return newLandCoverValue
    
    def updateValueTableInClassObject(self, newLandCoverValue):
        """ 
            Adds new LandCoverValue Object to control values class 
            
        ** Description:**

             This method is called by valueTableCellChanged whenever an item is changed in the valueTableWidget.  It 
             adds extracted data to control values class.
    
        **Arguments**
    
            * parameter:newLandCoverValue - LCC LandCoverValue object (To populate the control value class)
    
        **Returns:**

            * None
            
        """
        self.logProgress(stack()[0][3])
  
        self.tempLccObj.values[newLandCoverValue.valueId] = newLandCoverValue      

        self.logProgress(stack()[0][3] + " END")

    def evaluateValueOnChangeInput(self, row, column):
        """ 
            Evaluates new data when valueTable model is changed in mainWindow
        
        ** Description:**

            This method is called by valueTableCellChanged whenever an item is changed in the valueTableWidget.  This 
            evaluates the valueTableWidgetItem that is pointed at by passed row and passed column.  If data is found
            to be not valid self.message is upddated which will spawn a warning messageBox in parent class.
    
        **Arguments**
    
        * parameter:row - int (To point to row of changed data)
        * parameter:column - int (To point to column of changed data)
    
        **Returns:**

            * None - But directly accesses self.message
            
        """  
        self.logProgress(stack()[0][3])

        # # evaluate for valueId in value tree
        # # compare if ValueId is in key references of main lcc object
        # # by comparing keys of landCoverValues dictionary 
        # # if found, we change error message and change flag to recall new dialog
        if column == 1:
            if not self.ValueTableWidget.item(row, 1).text() or \
                self.ValueTableWidget.item(row, 1).text().strip() == "":
                self.message = "Please enter a <font color=red>VALUE NAME.</font>"
                return
            for checkNameObject in self.tempLccObj.values.values():
                if self.ValueTableWidget.item(row, 1).text().lower() == checkNameObject.name.lower():
                    valName = checkNameObject.name.lower()
                    self.message = valName.title() + " already exists as a <font color=red>VALUE NAME</font>, \
                                    please choose a different name."
                    return
        elif column >= 3:
            if not self.isFloat(self.ValueTableWidget.item(row, column).text()):
                colName = self.ValueTableWidget.horizontalHeaderItem(column).text()
                self.message = "The Coefficient <font color=red>" + colName.title() + " </font>value must be a decimal."
                return

        self.logProgress(stack()[0][3] + " END")
                
    def coefficientAddButton(self):
        pass
#         self.logProgress(stack()[0][3])
#         
#         self.dialogTitle = "Add Coefficients Dialog Window"
#         self.tempCoefObjList = []
#         self.addCoefDialog = AddCoefficientPopupWindow(self).exec_()
#         if self.addCoefDialog == 0:
#             return
#         
#         for newCoefIdObj in self.tempCoefObjList:
#             self.tempLccObj.coefficients[newCoefIdObj.coefId] = newCoefIdObj
#         
#         self.displayFile()
# 
#         self.logProgress(stack()[0][3] + " END")
    
    def coefficientDeleteButton(self):
#         self.logProgress(stack()[0][3])

        pass

    def setCoefficientParametersTable(self):
        """ 
            Sets the coefficientTable parameters for display in the model

        
        ** Description:**

            This method provides the parameters for the coefficientTable model and assigns the column headings.   
    
        **Arguments**
    
            * None             
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
 
        # creation of parameters...therefore must be implemented outside build file ....   :(
        columncount = 4
        headerLabels = ["Id", "Name", "Fieldname", "A/P"]
               
        self.CoefficientTableWidget.setSortingEnabled(True)
        self.CoefficientTableWidget.sortByColumn(0, Qt.AscendingOrder)
        self.CoefficientTableWidget.setRowCount(len(self.tempLccObj.coefficients.keys()))
        self.CoefficientTableWidget.setColumnCount(columncount)
        self.CoefficientTableWidget.setColumnWidth(0, 150)
        self.CoefficientTableWidget.setColumnWidth(1, 225)
        self.CoefficientTableWidget.setColumnWidth(2, 125)
        self.CoefficientTableWidget.setColumnWidth(3, 25)
        self.CoefficientTableWidget.setHorizontalHeaderLabels(headerLabels)
        lastHeader = self.CoefficientTableWidget.horizontalHeader()
        lastHeader.setStretchLastSection(True)
        self.CoefficientTableWidget.verticalHeader().setVisible(False)

        self.logProgress(stack()[0][3] + " END")
    
    def classesInsertValuesButton(self):
        """ 
            Inserts the value into the control classTree class 
        
        ** Description:**

             This method is triggered by clicking the classesInsertValues button.  On valid selection, it calls
             AddValueToClassTreePopUpWindow().  The error checking for value is done in the dialog.  The input
             retrieved by the dialog is then import to the control class classTree and addValueToClassTree is used to 
             update the frozen sets in the control class classTree.  Displays updated control class.
    
        **Arguments**
    
            * None            
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        self.dialogTitle = "Add Value to Class Tree Dialog"
        self.dialogVariable = []
        self.selectedClass = self.ClassesTree.currentItem()
        if not self.tempLccObj.values.keys():
            QMessageBox.warning(self, "Values IDs", "Currently there are no Value id's")  # prints warning 
            return  # message concerning empty Values table 
        if not self.selectedClass:
            QMessageBox.warning(self, "Class Selection", "Target Class must be selected before Value added")  # prints warning 
            return  # message concerning empty Values table 
        if self.isInt(self.ClassesTree.indexFromItem(self.ClassesTree.currentItem()).data(0)):
            QMessageBox.warning(self, "ALERT - Value Selected  ",
                                " Can not add a value to a value")
            return
        if not self.tempLccObj.classes[self.selectedClass.text(0)].canAddValuesToClassNode():
            QMessageBox.warning(self, "Incorrect Value Placement",
                                 "Classes can either have a class or a value as an attribute.")  
            return
        # checks to see if item in value tree is selected
        if self.ValueTableWidget.currentItem():
            pass
        else:
            dialogValid = AddValueToClassTreePopUpWindow(self).exec_()
            if dialogValid == 0:
                return   
        targetedControlerClass = self.tempLccObj.classes[self.selectedClass.text(0)]
        for selectedValues in self.dialogVariable:
            self.addValueToClassTree(targetedControlerClass, selectedValues)
        self.displayFile()

        self.logProgress(stack()[0][3] + " END")
    
    def addValueToClassTree(self, classItem, valueAdded):
        """ 
            Appends the values to the control classTree class and updates tree search
        
        ** Description:**

             This method is used to update the individual frozenSets of the classTree nodes in the control 
             classTree class.  The frozenSets are used to search for values in the classTree.  
    
        **Arguments**
    
            * parameter:classItem - The target classTree Object in classTree
            * parameter:valueAdded* - The value added to the classTree Ojbect in the classTree             
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
 
        def addValueToClassTreeFrozenSet(classItem, valueAdded):
            self.logProgress(stack()[0][3])

            classItem.addNewValueToUniqueValueIdsNodeList(valueAdded)
            if not classItem.parentClass == None:  # This is not the root
                addValueToClassTreeFrozenSet(classItem.parentClass, valueAdded)
        classItem.addNewValueId(valueAdded)
        if classItem.parentClass:
            addValueToClassTreeFrozenSet(classItem.parentClass, valueAdded)

        self.logProgress(stack()[0][3] + " END")
         
    def updateUniqueIds(self, index, idValue):
        """ 
            Updates the frozenset of the classes up the classTree.
            
        ** Description:**

             This method targets a specific classTree node and updates the frozenset that indicates children
             classTree nodes.  It recursively travels up the tree until there are no further parents updating each
             node. 
    
        **Arguments**
    
            * parameter:index - pointer to current classTree node
            * parameter:idValue - classId identifier that we are adding to the classTree control class.            
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        # create a new LandCoverClass object
        self.tempClassLCC = pylet.lcc.EditorLandCoverClass()  
        while not index.data() is None:
            self.tempClassLCC = self.tempLccObj.classes[index.data()]               
            self.tempClassLCC.addNewUniqueId(idValue)              
            # Resets the currentItemParentIndex
            index = index.parent()

        self.logProgress(stack()[0][3] + " END")

    def editUniqueIds(self, index, addClassId, removeClassId):
        """ 
            Updates the frozenset of the classes up the classTree by adding and removing classId.
            
        ** Description:**

             This method targets a specific classTree node and updates the frozenset that indicates children
             classTree nodes, both by adding and removing classId identifier.  It recursively travels up the tree 
             until there are no further parents updating each node. 
    
        **Arguments**
    
            * parameter:index - pointer to current classTree node
            * parameter:addClassId - classId identifier that we are adding to the classTree control class.  
            * parameter: removeClassId - classId identifier that we are removing from the classTree control class.          
    
        **Returns:**

            * None
            
        """
        self.logProgress(stack()[0][3])

        self.tempClassLCC = pylet.lcc.EditorLandCoverClass()  
        while not index.data() is None:
            self.tempClassLCC = self.tempLccObj.classes[index.data()]               
            self.tempClassLCC.addNewUniqueId(addClassId) 
            self.tempClassLCC.removeUniqueId(removeClassId)              
            # Resets the currentItemParentIndex
            index = index.parent()

        self.logProgress(stack()[0][3] + " END")

    def removeUniqueIds(self, index, removeClassId):
        """ 
            Updates the frozenset of the classes up the classTree by removing classId.
            
        ** Description:**

             This method targets a specific classTree node and updates the frozenset that indicates children
             classTree nodes, by removing classId identifier.  It recursively travels up the tree 
             until there are no further parents updating each node. 
    
        **Arguments**
    
            * parameter:index - pointer to current classTree node
            * parameter: removeClassId - classId identifier that we are removing from the classTree control class.          
    
        **Returns:**

            * None
            
        """
        self.logProgress(stack()[0][3])

        self.tempClassLCC = pylet.lcc.EditorLandCoverClass()  
        while not index.data() is None:
            self.tempClassLCC = self.tempLccObj.classes[index.data()]               
            self.tempClassLCC.removeUniqueId(removeClassId)              
            # Resets the currentItemParentIndex
            index = index.parent()

        self.logProgress(stack()[0][3] + " END")
             
    def storeExpandedBranches(self, topNode):
        """ 
            Stores which branches are open for later redisplaying.
        
        ** Description:**

             This method transverses that model classTree view,  evaluating which items are expanded or not.  Those
             items which are evaluated to be expanded are stored in a list which will be used to redisplay the tree.  
    
        **Arguments**
    
            * parameter:passedList - topLevelObjectItems of classTree control class 
            * parameter:storeOpenNodes - container to store pointers to expanded nodes             
    
        **Returns:**

            * storeOpenNodes
            
        """  
        self.logProgress(stack()[0][3])

        def createListOfWidgetItems(widgetAddress, storeOpenNodes):
            temp = PySide.QtGui.QTreeWidgetItem()
            for index in range(widgetAddress.childCount()):
                temp = widgetAddress.child(index)
                if self.isInt(temp.text(0)):
                    continue
                if temp.isExpanded():
                    storeOpenNodes.append(temp.text(0))
                    if(temp.childCount() != 0):
                        createListOfWidgetItems(temp,storeOpenNodes)

        storeOpenNodes = []

        # list to hold which nodes are expanded                            
        passedList = []
        if not topNode:
            for itemIndex in range(self.ClassesTree.topLevelItemCount()):
                passedList.append(self.ClassesTree.topLevelItem(itemIndex))
        else:
            passedList.append(topNode)
        # Establish initial List from QtWidget model
        for item in passedList:
            if self.isInt(item.text(0)):
                continue
            if item.isExpanded():
                storeOpenNodes.append(item.text(0))
                if(item.childCount() != 0):
                    createListOfWidgetItems(item, storeOpenNodes)
                   
        self.logProgress(stack()[0][3] + " END")
        return storeOpenNodes
    
    def restoreExpansion(self, topNode,openNodes):
        """ 
            Restore a new classTree to previously saved expansion state.
        
        ** Description:**

            This method transverses that model classTree view in reverse,  evaluating which items are expanded or not.
            Those items which are evaluated to be expanded are stored in a list which will be used to redisplay the
            tree.  
    
        **Arguments**
    
            * parameter:passedList - topLevelObjectItems of classTree control class 
            * parameter:OpenNodes - container to store pointers to expanded nodes             
    
        **Returns:**

            * None
            
        """
        self.logProgress(stack()[0][3])
  
        def expandListOfWidgetItems(widgetAddress, openNodes):
#            self.logProgress(stack()[0][3])
            temp = PySide.QtGui.QTreeWidgetItem()
            for index in range(widgetAddress.childCount()):
                temp = widgetAddress.child(index)
                if self.isInt(temp.text(0)):
                    continue
                if temp.text(0) in openNodes:
                    temp.setExpanded(True)
                    expandListOfWidgetItems(temp, openNodes)

        # list to hold which nodes are expanded                            
        passedList = []
        if not topNode:
            for itemIndex in range(self.ClassesTree.topLevelItemCount()):
                passedList.append(self.ClassesTree.topLevelItem(itemIndex))
        else:
            passedList.append(topNode)
        # Establish initial List from QTwidget model    
        for item in passedList:
            if self.isInt(item.text(0)):
                continue
            if item.text(0) in openNodes:
                item.setExpanded(True)
                if(item.childCount() != 0):
                    expandListOfWidgetItems(item, openNodes)
                
        self.logProgress(stack()[0][3] + " END")

    def classesAddSiblingClassButton(self):
        """ 
            Adds a node sibling class to the existing control classTree class or creates a top level node class.
        
        ** Description:**

            This function is triggered when the addSiblingsClass button is clicked.  First, it evaluates where there is
            an existing classTree and starts a new one if not.  Secondly, if item in classTree model is selected,
            method triggers addClassIdIdPopupWindow dialog to retrieve data of new sibling node class.  Lastly, this
            data is appended to the classTree node that corresponds with the selected classTree model item, and updates
            the control classTree class with relevant methods.  Finally, it displays a the new updated model.  
    
        **Arguments**
    
            * None 
            
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        self.dialogVariable = pylet.lcc.EditorLandCoverClass()
        currentItemIndex = self.ClassesTree.indexFromItem(self.ClassesTree.currentItem())
        self.dialogTitle = "Add Sibling Dialog" 
        # Checks to see if a ClassTree is empty or if any class is selected
        # True
        if self.tempLccObj.classes.topLevelClasses and not self.ClassesTree.selectedItems():
            QMessageBox.warning(self, "ALERT - Nothing Selected", "No class has been selected.  "
                    + " Please select a class and try again ")
            return
        if self.isInt(currentItemIndex.data(0)):
            QMessageBox.warning(self, "ALERT - Value Selected  ",
                                " Can not add a class to a value")
            return
        # Prompt the user for a class
        # create instance of dialog box addClassIdPopupWindow
        validDialog = AddClassIdPopupWindow(self).exec_()
        if validDialog == 0:
            return
        # If no class is selected and there is no class we need to start a new class tree
        currentItemParentIndex = currentItemIndex.parent()
        if self.ClassesTree.itemFromIndex(currentItemParentIndex) is None:
            self.dialogVariable.setParentClass(None)
            self.tempLccObj.classes.addTopLevelClass(self.dialogVariable)
        else:
            # Gets the index of the parent
            self.dialogVariable.setParentClass(self.tempLccObj.classes[currentItemParentIndex.data()])
            # add the new class to the parents' childClassesList
            self.tempLccObj.classes[currentItemParentIndex.data()].childClasses.append(self.dialogVariable)
            # add the new object to the global control structure
            self.tempLccObj.classes[self.dialogVariable.classId] = self.dialogVariable
            # update all uniqueIds up the branches
            self.updateUniqueIds(currentItemParentIndex, self.dialogVariable.classId)
        for overwriteFieldKeys in self.dialogVariable.classoverwriteFields.keys():
            if self.dialogVariable.classoverwriteFields[overwriteFieldKeys]:
                self.tempLccObj.overwriteFieldDataList.append(self.dialogVariable.classoverwriteFields[overwriteFieldKeys])
        self.dialogVariable = None
        self.displayFile()                 

        self.logProgress(stack()[0][3] + " END")
         
    def classesAddChildClassButton(self):
        """ 
            Adds a node child class to the existing control classTree class.  
        
        ** Description:**

             This function is triggered when the addChildClass button is clicked. The method triggers 
             addClassIdIdPopupWindow dialog to retrieve data of new child node class.  This data populates a new 
             classTree node and is appended to the classTree node that corresponds with the selected classTree model
             item, and updates the control classTree class with relevant methods.  Finally, it displays a the new
            updated model.  
             
        **Arguments**
    
            * None           
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        self.dialogTitle = "Add Child Class Dialog"
        # #Initialization area
        self.dialogVariable = pylet.lcc.EditorLandCoverClass()
        #     prompt if no file open
        if self.tempLccObj.classes.topLevelClasses == None:
            QMessageBox.warning(self, "ALERT - No File open", "Can not use 'Add Child Class' button. \n"
                    + " Please use 'Add Sibling Class' button to enter a parent class.")
            return
        #    prompt if nothing selected
        elif not self.ClassesTree.selectedItems():
            QMessageBox.warning(self, "ALERT - Nothing Selected", "No class has been selected.  "
                    + " Please select and try again ")
            return
        currentItemIndex = self.ClassesTree.indexFromItem(self.ClassesTree.currentItem())                
        if self.isInt(currentItemIndex.data(0)):
            QMessageBox.warning(self, "ALERT - Value Selected  ",
                                " Can not add a class to a value")
            return
        if not self.tempLccObj.classes[currentItemIndex.data()].canAddChildToClassNode():
            QMessageBox.warning(self, "ALERT - Illegal Action",
                                " Can not add a child to a class with values")
            return
        # Prompt the user for a class
        # create instance of dialog box addClassIdPopupWindow
        validDialog = AddClassIdPopupWindow(self).exec_()
        if validDialog == 0:
            return
        # Gets the name of the currentItem => selected item
        self.dialogVariable.setParentClass(self.tempLccObj.classes[currentItemIndex.data()])       
        # Adds the new class as a TopLevelClass => ie global tree
        self.tempLccObj.classes[currentItemIndex.data()].childClasses.append(self.dialogVariable)
        # add new object to global object
        self.tempLccObj.classes[self.dialogVariable.classId] = self.dialogVariable        
        # update all uniqueids up branches
        self.updateUniqueIds(currentItemIndex, self.dialogVariable.classId)
        for overwriteFieldKeys in self.dialogVariable.classoverwriteFields.keys():
            if self.dialogVariable.classoverwriteFields[overwriteFieldKeys]:
                self.tempLccObj.overwriteFieldDataList.append(self.dialogVariable.classoverwriteFields[overwriteFieldKeys])
        self.ClassesTree.itemFromIndex(currentItemIndex).setExpanded(True)
        # updates GUI to display correct values    
        self.displayFile()

        self.logProgress(stack()[0][3] + " END")

            
    def classesEditClassButton(self):
        """ 
            Allows for the editing of the control classTree class node. 
        
        ** Description:**

             This method is triggered by the classesEditClass button being clicked.  The selected classTree item is 
             retrieved from the control classTree class and sent to editClassInfoPopUpWindow dialog for editing.  After
             dialog evaluates and validates data, this method compares the original data to the retrieved data and
             updates the control classTree class correspondingly, by adding new data and removing old data.  
             Finally, it displays a the new updated model.  
                 
        **Arguments**
    
            * None      
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        self.dialogTitle = "Edit Class Dialog"
        #     prompt if no file open
        if self.tempLccObj.classes.topLevelClasses == None:
            QMessageBox.warning(self, "ALERT - No File open", "Can not use 'Edit Class' button. \n"
                    + " Please use 'Add Sibling Class' button to enter a parent class.")
            return
        #    prompt if nothing selected
        elif not self.ClassesTree.selectedItems():
            QMessageBox.warning(self, "ALERT - Nothing Selected", "No class has been selected.  "
                    + " Please select and try again ")
            return
        elif self.isInt(self.ClassesTree.currentItem().text(0)):
            QMessageBox.warning(self, "ALERT - Editting Value", "Values can not be edited from class tree.")
            return
        #Initialization area
        currentItemIndex = self.ClassesTree.indexFromItem(self.ClassesTree.currentItem())
        self.dialogVariable = self.tempLccObj.classes[currentItemIndex.data()]
        self.originalLccObject = pylet.lcc.EditorLandCoverClass()
        self.originalLccObject.classId = self.tempLccObj.classes[currentItemIndex.data()].classId
        # copy into storage container for comparison
        for overwriteFieldKeys in self.dialogVariable.classoverwriteFields.keys():
            self.originalLccObject.classoverwriteFields[overwriteFieldKeys] = self.dialogVariable.classoverwriteFields[overwriteFieldKeys]
        # Prompt the user for a class
        # create instance of dialog box EditClassInfoPopUpWindow            
        validDialog = EditClassInfoPopUpWindow(self).exec_()
        if validDialog == 0:
            return
        # Update control class if class id has changed
        if not self.dialogVariable.classId == self.originalLccObject.classId:
            # Update frozen sets with our new class id
            self.editUniqueIds(currentItemIndex.parent(), [self.dialogVariable.classId], self.originalLccObject.classId)
            # Update classes with new key
            self.tempLccObj.classes[self.dialogVariable.classId] = \
                                                self.tempLccObj.classes[self.originalLccObject.classId]
            # Delete original class key
            del self.tempLccObj.classes[self.originalLccObject.classId]
        # Check to see if any Lcp fields have been modified
        for overwriteFieldKeys in self.dialogVariable.classoverwriteFields.keys():
            if not self.originalLccObject.classoverwriteFields[overwriteFieldKeys] == \
                                                             self.dialogVariable.classoverwriteFields[overwriteFieldKeys]:
                if self.dialogVariable.classoverwriteFields[overwriteFieldKeys]:
                    self.tempLccObj.overwriteFieldDataList.append(self.dialogVariable.classoverwriteFields[overwriteFieldKeys])
                    if self.originalLccObject.classoverwriteFields[overwriteFieldKeys]:
                        self.tempLccObj.overwriteFieldDataList.remove(self.originalLccObject.classoverwriteFields[overwriteFieldKeys])
        self.ClassesTree.itemFromIndex(currentItemIndex).setExpanded(True)
        # updates GUI to display correct values    
        self.displayFile()

        self.logProgress(stack()[0][3] + " END")
         
    def removeValueIdFromClassTree(self, valueId, passedList):
        """
            Helper method that removes values from control classTree class and related frozensets.
        
        ** Description:**

             This method is a helper function of classesRemoveClassButton, it recursively removes passed values from
             forzensets of all classTree nodes and removes the value itself. 
    
        **Arguments**
    
            * parameter:valueId - int
            * parameter:passedList -  A list of classTree objects which are the children of the recursive parent.
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        if passedList == None:
            return
        for classObject in passedList:
            if classObject.isLeaf():  # check to see if it can have values
                if classObject.isValueInSet(valueId):  # check to see if it has the specific value
                    classObject.removeValueId(valueId)  # removes the value
            else:  # not a leaf (on the wind)
                if classObject.isValueInSet(valueId):  # check to see if it has the specific value - frozenset
                    classObject.removeValueId(valueId)  # removes the value
                    self.removeValueIdFromClassTree(valueId, classObject.childClasses)  # recursively feeding the children of the object

        self.logProgress(stack()[0][3] + " END")

    def removeValueIdFromClassNode(self, valueId, targetNode):
        """ """
        self.logProgress(stack()[0][3])

        def removeValueIdFromNodePath(valueId, targetNode):
            self.logProgress(stack()[0][3])

            self.tempLccObj.classes[targetNode.classId].uniqueValueIds.remove(valueId)
            if self.tempLccObj.classes[targetNode.classId].parentClass == None:
                return
            removeValueIdFromNodePath(valueId, self.tempLccObj.classes[targetNode.classId].parentClass)
        self.tempLccObj.classes[targetNode.classId].childValueIds.remove(valueId)
        removeValueIdFromNodePath(valueId, self.tempLccObj.classes[targetNode.classId])

        self.logProgress(stack()[0][3] + " END")
  
    def removeClassIdFromClassTree(self, valueId, passedList):
        """
            Helper method that removes classTree node from control classTree class and related frozensets.
        
        ** Description:**

             This method is a helper function of classesRemoveClassButton, it recursively removes passed classTree node
             from forzensets of all classTree nodes and removes the classTree node itself.  It should be noted that it
             also recursively removes any children or values underneath it.   
    
        **Arguments**
    
            * parameter:valueId - int
            * parameter:passedList -  A list of classTree objects which are the children of the recursive parent.
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        for classObject in passedList:
            # First thing need to do it check to see if classObject is target class
            if classObject.classId == valueId:
                # create iterator that removes target children as well
                for childClasses in classObject.getChildrenClasses():
                    self.removeClassIdFromClassTree(childClasses, self.tempLccObj.classes.topLevelClasses)
                # check to see if leaf
                for childValue in classObject.childValueIds:
                    self.removeValueIdFromClassNode(childValue, self.tempLccObj.classes[classObject.classId])
                if self.tempLccObj.classes[classObject.classId].parentClass:
                    for lcpKey in self.tempLccObj.classes[classObject.classId].classoverwriteFields.keys():
                        if self.tempLccObj.classes[classObject.classId].classoverwriteFields[lcpKey]:
                            self.tempLccObj.overwriteFieldDataList.remove(self.tempLccObj.classes[\
                                                                    classObject.classId].classoverwriteFields[lcpKey])
                    self.tempLccObj.classes[classObject.classId].parentClass.childClasses.remove(
                            self.tempLccObj.classes[classObject.classId])
                elif classObject in self.tempLccObj.classes.topLevelClasses:
                    for lcpKey in self.tempLccObj.classes[classObject.classId].classoverwriteFields.keys():
                        if self.tempLccObj.classes[classObject.classId].classoverwriteFields[lcpKey]:
                            self.tempLccObj.overwriteFieldDataList.remove(self.tempLccObj.classes[\
                                                                    classObject.classId].classoverwriteFields[lcpKey])
                if classObject.parentClass == None:
                    self.tempLccObj.classes.topLevelClasses.remove(self.tempLccObj.classes[classObject.classId])
                del self.tempLccObj.classes[classObject.classId]
            elif valueId in classObject.getChildrenClasses():
                classObject.removeUniqueId(valueId)
                self.removeClassIdFromClassTree(valueId, classObject.childClasses)
            else:
                continue

        self.logProgress(stack()[0][3] + " END")
          
    def classesRemoveClassButton(self):
        """ 
            This removes a class item from the classTree control class. 
        
        ** Description:**

             This method is triggered by signal when classesRemoveClass button is clicked.  First, it checks to see 
             if what is being deleted is a value or a class.  If it is a value it calls the appropriate method to 
             remove it from the control classTree class and pertinent frozensets.  If it is a class it calls the 
             appropriate method to remove it from the control classTree class and pertinent frozensets.  It should 
             be noted that the called methods remove not only the targeted value or class from the control classTree 
             class but also any children.  The method then evulates whether the buttons should be active or not.  
             Finally, it redisplays the updated control class.
             
        **Arguments**
    
            * None             
    
        **Returns:**

            * None
            
        """  
        self.logProgress(stack()[0][3])

        targetNodeIndex = self.ClassesTree.indexFromItem(self.ClassesTree.currentItem())
        # evaluate if selection has been clicked
        if not targetNodeIndex.data():
            QMessageBox.warning(self, "ALERT - No Class Selected", "Can not use 'Remove Class/Value' button. \n" 
                                 + "Please select target class/value to utilize 'Remove Class/Value' button.")
            return         
        if self.isInt(str(targetNodeIndex.data())):
            self.removeValueIdFromClassNode(int(targetNodeIndex.data()), self.tempLccObj.classes[targetNodeIndex.parent().data()])
        else:
            self.removeClassIdFromClassTree(str(targetNodeIndex.data()), self.tempLccObj.classes.topLevelClasses)
        if not self.tempLccObj.classes.topLevelClasses:
            self.deactivateClassButtons()
        self.displayFile()

        self.logProgress(stack()[0][3] + " END")

    def classesToggleClassTreeButton(self):
        """ Function that expands/collapses class tree.  
        
        ** Description:**

            This method is called when the toggle tree button is triggered.   It either expands every node or collapses
            every node of the class tree.
            
    
        **Arguments**
    
            * None        
    
        **Returns:**

            * None
            
        """ 
        self.logProgress(stack()[0][3])
 
        if self.ClassesExpandCollapseButton.isChecked():
            self.ClassesTree.expandAll()
        else:
            self.ClassesTree.collapseAll()

        self.logProgress(stack()[0][3] + " END")
                    
    def isInt(self, passedString):
        """ 
            Boolean method that determines if a variable is an integer
        
        ** Description:**

             This method is passed a single variable and returns true if it is an integer and false if anything else.
    
        **Arguments**
    
            * parameter:passesString - variable (Returns true if integer.)
    
        **Returns:**

            * Boolean
            
        """
        self.logProgress(stack()[0][3])
        return unicode(passedString).isnumeric()
    
    def isFloat(self, passedString):
        """ 
            Float method that determines if a variable is a float
        
        ** Description:**

             This method is passed a single variable and returns true if it is a float and false if anything else.
    
        **Arguments**
    
            * parameter:passesString - variable (Returns true if float.)
    
        **Returns:**

            * Boolean
            
        """
        self.logProgress(stack()[0][3])
        try:
            return float(passedString)
        except ValueError:
            return False
          
    def initLog(self):
        logFile = os.path.join('AutoSave','log.lfn')
        os.remove(logFile)
        
    def logProgress(self, message):
        testStackSize = str(stack().__sizeof__())
        logString = "log.lfn"
        logFile = os.path.join('AutoSave',logString)
        logFile = open(logFile,'a')
        logFile.write(message + " Current Stack size " + testStackSize + "\n")
        tempStack = stack()
        tempBuffer = ""
        for iter in reversed(tempStack):
            logFile.write(str(iter[3]) + "\n")
        logFile.write("\n")

        logFile.close()
        
    def removeInvalidObjectsFromClassTree(self, removedObject):
        
        self.logProgress(stack()[0][3])

        def recursiveRemoval(rootObject):
            for index in range(rootObject.childCount()):
                if not rootObject.child(index):
                    continue
                if rootObject.child(index).childCount() != 0:
                    recursiveRemoval(rootObject.child(index))
                rootObject.removeChild(rootObject.child(index))
        if removedObject.childCount() != 0:
            recursiveRemoval(removedObject)
        if not removedObject.parent(): # This is a top level item
            self.ClassesTree.invisibleRootItem().removeChild(removedObject)
        else:
            removedObject.parent().removeChild(removedObject)
        
        self.logProgress(stack()[0][3] + " END")
        
    def cloneNode(self, topNewNode, topOldNode):

        self.logProgress(stack()[0][3])
        
        for index in range(topOldNode.childCount()):
            if not topNewNode:
                return
            topNewNode.addChild(topOldNode.child(index).clone())
            self.cloneNode(topNewNode.child(index), topOldNode.child(index))

        self.logProgress(stack()[0][3] + " END")
       
if __name__ == '__main__':
    """ Launch the MainWindow for the LCCEditor"""
     
    # Every PySide application must create an application object.  The sys.argv parameter is a list of command line args 
    app = _QApplication(_sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
    
    
""" 
    ONE_LINE_SUMMARY 
    
    **Description:**
        DETAILED_DESCRIPTION
    
    **Arguments:**
        * *INPUT_ARGUMENT_1* - ONE_LINE_DESCRIPTION_OF_TYPE_AND_PURPOSE 
        * *INPUT_ARGUMENT_2* - ONE_LINE_DESCRIPTION_OF_TYPE_AND_PURPOSE
    
    **Returns:**
        * RETURNED_OBJECT_TYPE
"""
