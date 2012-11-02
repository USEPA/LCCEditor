
""" Graphical User Interface (GUI) for the Land Cover Classification Editor (LCCEditor)

    The main() function launches the LCCEditor MainWindow

"""

from PySide.QtGui import QMainWindow as _QMainWindow
from PySide.QtGui import QPushButton as _QPushButton
from PySide.QtGui import QApplication as _QApplication
from PySide.QtGui import QMessageBox        # needed for about 
from PySide.QtGui import QFileDialog        # needed for open

from main_ui import Ui_MainWindow
import sys as _sys
import platform                             # needed for platform details
import PySide                               # needed for version
import os
import pylet
from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *
from xml.dom.minidom import parse
from xml.dom.minidom import Document
from pprint import pprint
from Tkinter import Toplevel

VERSION = '0.0.1'
TITLE = "About Land Cover Classification Editor (LCCEditor)"

ABOUT_MESSAGE = """<b>Platform Details</b> v %s
                <p>Copyright(c) 2012 EPA LEB.
                <p> This is the EPA LEB LCCEditor.</p>
                <p>Python %s - PySide version %s - Qt version %s on %s""" % (VERSION,
                platform.python_version(), PySide.__version__, PySide.QtCore.__version__,
                platform.system())
                
def main():
    """ Launch the MainWindow for the LCCEditor"""
    
    app = _QApplication(_sys.argv)
    frame = MainWindow()
    frame.show()  
    app.exec_()  

   
class MainWindow(_QMainWindow, Ui_MainWindow):
    """ MainWindow for the LCCEditor"""
    
    fileName = ""
    tempFileName = ""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ActionAbout.triggered.connect(self.about)
        self.ActionHelp.triggered.connect(self.helpMenu)
        self.ActionOpen.triggered.connect(self.fileOpen)
        self.ActionSave.triggered.connect(self.fileSave)
        self.ActionSaveAs.triggered.connect(self.fileSave)
        self.ActionNew.triggered.connect(self.new)
        self.ValuesAddButton.clicked.connect(self.valuesAddButton)
        self.ValuesRemoveButton.clicked.connect(self.valuesDeleteButton)
        self.ClassesInsertValuesButton.clicked.connect(self.classesInsertValuesButton)
        self.ClassesAddSiblingButton.clicked.connect(self.classesAddSiblingClassButton)
        self.ClassesAddChildButton.clicked.connect(self.classesAddChildClassButton)
        self.ClassesEditButton.clicked.connect(self.classesEditClassButton)
        self.ClassesRemoveButton.clicked.connect(self.classesRemoveClassButton)
        self.tempLccObj = pylet.lcc.LandCoverClassification()
        
    #start here !!!!!!!
    def about(self):
        """Popup a box with the About message."""
 
        QMessageBox.about(self, TITLE, ABOUT_MESSAGE)

    def helpMenu(self):
        """Opens LLCEditor Help file"""
        
        pathname = os.path.dirname(_sys.argv[0]) + "\TEMP.chm"      # a file relative to running file
        os.startfile(pathname)
    
    def clearLccItems(self):
        """ Clear all the LCC items in dialog loaded from file"""
        
        self.ValuesTree.clear()
        self.ClassesTree.clear()
        self.MetadataNameLineEdit.setText('')                
        self.MetadataDescriptionTextEdit.setPlainText('') 
#        self.tempLccObj = pylet.lcc.LandCoverClassification()

    def new(self):
        """ Clear all the LCC items in dialog loaded from file"""
        
        self.ValuesTree.clear()
        self.ClassesTree.clear()
        self.MetadataNameLineEdit.setText('')                
        self.MetadataDescriptionTextEdit.setPlainText('') 
        self.tempLccObj = pylet.lcc.LandCoverClassification()
        
        
    def getFileName(self):
        """Gets the file name and creates a temporary file name """
        
        global fileName, tempFileName
        
        # path will eventually be gotten from a config file through _init__
        self.fileName = QFileDialog.getOpenFileName(self,"Open File", 
            "D:\ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications", 
            "LCC files (*.lcc)")[0] # might have to use '/home')
            
    def fileOpen(self):
        """Opens a file for viewing"""
        
        global fileName, tempFileName, tempLccObj
        
        # gets the file name
        self.getFileName()

        # Exit if user selected cancel in the dialog
        if not self.fileName:
            return

        print "filename is ", self.fileName
        
        # Clear the dialog of loaded/created items
        self.clearLccItems()

        # Load the input file
        self.lccObj = pylet.lcc.LandCoverClassification(self.fileName)         # create a LandCoverClassification object

        self.tempLccObj = self.lccObj
        
        self.displayFile()
        
    def displayFile(self):
        """Displays the file in the GUI"""
        
        ten = "10"
        indent = "    "
        
        self.clearLccItems()
        

        self.ValuesTree.setSortingEnabled(True)
        self.ValuesTree.sortByColumn(0,Qt.AscendingOrder)
      
        # Load values 
        for value in self.tempLccObj.values.values():                       # prints value for the Value Tree
            assert isinstance(value, pylet.lcc.LandCoverValue)      # activates auto-completion      
#            print value.valueId, value.name, value.excluded
            try:

                item_0 = QtGui.QTreeWidgetItem(self.ValuesTree)
                
                item_0.setText(0, str(value.valueId))
                item_0.setText(1, str(value.name))
                
                if(value.excluded):
                    item_0.setCheckState(2, QtCore.Qt.Checked)
                else:
                    item_0.setCheckState(2, QtCore.Qt.Unchecked)
           
            except:
                pass
            
        # Load classes
        def printDescendentClasses(landCoverClass, item_0, indentUnit, indentLevel):
            i = 1
            for childClass in landCoverClass.childClasses:
                assert isinstance(childClass, pylet.lcc.LandCoverClass)
                
                # childClass
                item_1 = QtGui.QTreeWidgetItem(item_0)
                item_1.setText(0, childClass.classId) #set id
                item_1.setText(1, childClass.name)   #set name
                print (i*indent), childClass.classId, childClass.name
#                print indentUnit*indentLevel, childClass.classId, childClass.name
                j = 2
                for childValueId in childClass.childValueIds:
                    
                    childItem = QtGui.QTreeWidgetItem(item_1)
                    childItem.setText(0, str(childValueId))
                    print (j * indent), childValueId
 
                printDescendentClasses(childClass,item_1, indentUnit, indentLevel + 1)
                j = j + 1
            i = i + 1
        self.ClassesTree.setSortingEnabled(False)
   
        for topLevelClass in self.tempLccObj.classes.topLevelClasses:
            assert isinstance(topLevelClass, pylet.lcc.LandCoverClass)
            
            try:
                item_0 = QtGui.QTreeWidgetItem(self.ClassesTree)

                item_0.setText(0, str(topLevelClass.classId))
                item_0.setText(1, str(topLevelClass.name))
                print topLevelClass.classId, topLevelClass.name
#                item_1 = QTreeWidgetItem(item_0.setText(0, str(topLevelClass.classId)))
            except:
                pass
            
            printDescendentClasses(topLevelClass, item_0, indent, 2)
        print
                
        # Load Metadata Name
        metadataName = self.tempLccObj.metadata.name
        self.MetadataNameLineEdit.setText(metadataName)
        
        # Load Metadata Description
        metadataDescription = self.lccObj.metadata.description
        self.MetadataDescriptionTextEdit.setPlainText(metadataDescription)
                
    def fileSave(self):
        """ Saves the file in the required format"""
        
        global tempLccObj
        indent = "    "
        
        root_dir = os.path.join(".",'\ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications')
        outFileName = QFileDialog.getSaveFileName(self,'Save File',root_dir,"LCC files (*.lcc)")[0]
#        print 'out file name is', outFileName
        if not outFileName:
            return
        outFileName = open(outFileName,'w')
#        print "This is the in file name", fileName
#        print 'This is tempFileName', self.tempFileName
#        print 'This is lccObj', lccObj
        container = 'ATtILA2{0}ToolboxSource'.format(os.sep)
#        print "container is ", container
        dirName = pylet.lcc.constants.PredefinedFileDirName
#        print "dirName is ", dirName

        self.tempLccObj.metadata.name = self.MetadataNameLineEdit.text()
        self.tempLccObj.metadata.description = self.MetadataDescriptionTextEdit.toPlainText()

        # File Output starts here        
        outFileName.write('<root>')
        outFileName.write("\n")
        outFileName.write("\n")
        outFileName.write(indent)
        outFileName.write('<metadata>')
        outFileName.write("\n")
        outFileName.write(indent)
        outFileName.write(indent)
        outFileName.write('<name>')
        try:
            outFileName.write(str(self.tempLccObj.metadata.name))
        except:
            pass

        outFileName.write('</name>')
        outFileName.write("\n")
        outFileName.write(indent)
        outFileName.write(indent)
        outFileName.write('<description>')

        try:
            outFileName.write(str(self.tempLccObj.metadata.description))
        except:
            pass

        outFileName.write('</description>')
        outFileName.write("\n")
        outFileName.write(indent)
        outFileName.write('</metadata>')
        outFileName.write("\n")
        outFileName.write("\n")

        coefficientPhrase = """    <!-- 
        * The "Coefficients" node contains coefficients to be assigned to values.
        * 
        * id - text, unique identifier
        * name - text, name describing coefficient
        * fieldName - text, name of field to be created for output
    -->
"""
        outFileName.write(coefficientPhrase)
#        outFileName.write("\n")
        outFileName.write(indent)
        outFileName.write('<coefficient>')
        outFileName.write("\n")
        outFileName.write(indent)
        outFileName.write('</coefficient>')
        outFileName.write("\n")
        outFileName.write("\n")
        outFileName.write("\n")
        outFileName.write("\n")
        
        valuesPhrase = """    <!--  
        * The "values" node defines the full set of values that can exist in a landcover raster
        * The "excluded" attribute is used to exclude values from the total, excluded=false is the default
        * Actual excluded values are always treated as excluded=true, cannot be used in classes, and should not be listed here. 
    -->
"""
        
        outFileName.write(valuesPhrase)
        outFileName.write(indent)
        outFileName.write('<values>')
        outFileName.write("\n")
        
        try:
            for value in self.tempLccObj.values.values():                       # prints value for the Value Tree
                assert isinstance(value, pylet.lcc.LandCoverValue)      # activates auto-completion      
    
                try:
                    outFileName.write(indent)
                    outFileName.write(indent)
                    outFileName.write('<value id="')
                    outFileName.write(str(value.valueId))
                    outFileName.write('" name="')
                    outFileName.write(str(value.name))
    #                
                    if(value.excluded):
                        outFileName.write('" excluded="true" >')
                        outFileName.write("\n")
                    else:
                        outFileName.write('" >')
                        outFileName.write("\n")
                        
                    outFileName.write(indent)
                    outFileName.write(indent)
                    outFileName.write('</value>')
                    outFileName.write("\n")
                except:
                    pass
        except:
            pass
        
        outFileName.write(indent)
        outFileName.write('</values>')
        
        classesPhrase = """    <!-- 
        * The "classes" node contains values grouped into classes.
        * A class can contain either values or classes but not both types
        * Values contain only an id which refers to a value in values node.
        * The id attribute is used for the root of the field name in the output(for example %forest would be P + for = Pfor)
        * Two classes with the same id are not allowed.
        * Special class attributes:
            - onSlopeVisible: Make available in "On Slope" metric category, default is false
            - lcpField:  if present, it overides default "Land Cover Proportions" field name with the supplied value    
    -->
"""

        outFileName.write("\n")
        outFileName.write("\n")
        outFileName.write("\n")
        outFileName.write("\n")
        outFileName.write(classesPhrase)
        outFileName.write(indent)
        outFileName.write('<classes>')
        outFileName.write("\n")
        
        def printDescendentClasses(landCoverClass, item_0, indentUnit, indentLevel):
            
            for childClass in landCoverClass.childClasses:
                assert isinstance(childClass, pylet.lcc.LandCoverClass)
                
                # childClass
                item_1 = QtGui.QTreeWidgetItem()
                outFileName.write(indentUnit*indentLevel)
                outFileName.write('<class id="')
                outFileName.write(str(childClass.classId))    #set id
                outFileName.write('" name="')
                outFileName.write(str(childClass.name))       #set name
                outFileName.write('" filter="')
#                outFileName.write('" lcosp"')
                outFileName.write('" >')
                outFileName.write("\n")

                for childValueId in childClass.childValueIds:
                    outFileName.write(indentUnit*(indentLevel+1))
                    outFileName.write('<value id="')
                    outFileName.write(str(childValueId))
                    outFileName.write('"/>')
                    outFileName.write("\n")
                
                printDescendentClasses(childClass,item_1, indentUnit, indentLevel + 1)
                outFileName.write(indentUnit*indentLevel)
                outFileName.write("</class>")
                outFileName.write("\n")
        
        try:
            for topLevelClass in self.tempLccObj.classes.topLevelClasses:
                assert isinstance(topLevelClass, pylet.lcc.LandCoverClass)
                
                item_0 = QtGui.QTreeWidgetItem(self.ClassesTree)
    
                try:
                    outFileName.write(indent)
                    outFileName.write(indent)
                    outFileName.write('<class id="')
                    outFileName.write(str(topLevelClass.classId))
                    outFileName.write('" name="')
                    outFileName.write(str(topLevelClass.name))
                    outFileName.write('" lcpField="')
                    outFileName.write('" filter="')
                    outFileName.write('" >')
                    outFileName.write("\n")
    
                    printDescendentClasses(topLevelClass, item_0, indent, 3)
                    
                    outFileName.write(indent)
                    outFileName.write(indent)
                    outFileName.write('</class>')
                    outFileName.write("\n")
                except:
                    pass
                
        except:
            pass
            
        outFileName.write(indent)
        outFileName.write('</classes>')
        

        outFileName.write("\n")
        outFileName.write('</root>')
        
        outFileName.close()
        
    def valuesAddButton(self):
        """ Add value button allows the user to enter in new IDs, Values and Excluded values""" 
        global tempLccObj
        
        # prompts user to input ID from a Input Dialog Box
        text1, ok = QtGui.QInputDialog.getInt(self, 'Values id Dialog', 'Enter Id of the Value', minValue=0)
        
        # checks to see if value was entered
        if text1:
#            self.tempLccObj.values.valueId = text1                  # set key value to entered value **useless line?
            print self.tempLccObj.values.items()
            # checks if value exists in dictionary
            for key in self.tempLccObj.values.keys():
                if key == text1:
                    QMessageBox.warning(self, "ALERT - Value ID", "Id has already been used. Please enter another id "
                    + "or delete id then reenter")
                    return

            # prompts user to input value
            text2, ok = QtGui.QInputDialog.getText(self, 'Values name Dialog', 'Enter name of the Value')
            if not text2:                   # checks to see if value was entered
                return
            text2 = text2.title()           # capitalizes first letter of each word

            # prompts user to input Excluded value
            text3, ok = QtGui.QInputDialog.getText(self, 'Values excluded Dialog', 'Excluded (Enter yes or no)')
            text3 = text3.lower()           # changes string to lower characters

            if not text3:                   # checks to see if excluded value was entered
                return
            while text3:                    # checks to see if excluded value was 'yes' or 'no'
#                print "in while"
                if text3 == "yes":
                    break
                elif text3 == "no":
                    break
                else:                       # if users didn't enter yes/no, reprompts
                    text3, ok = QtGui.QInputDialog.getText(self, 'Values excluded Dialog', "Please enter Excluded value"
                                                           + " as 'yes' or 'no'")
                    text3 = text3.lower()           # changes string to lower characters
                    if not text3:
                        return

            self.tempValueLCV = pylet.lcc.LandCoverValue()               # create a new LandCoverValue object
           
            self.tempValueLCV.addValues(text1, text2, text3)             # populate the object
            
            self.tempLccObj.values[text1] = (self.tempValueLCV)          # populate the keys with the objects
            
#        for value in self.tempLccObj.values.values():                       # prints value for the Value Tree
#            try:
#                print value.valueId
#                print value.name
#            except:
#                print "in except"
#                pass

        self.displayFile()                              # updates GUI to display correct values
                                            
    def valuesDeleteButton(self):
        """ The delete value button deletes value entries from the GUI"""
        
        global tempLccObj                   # global object
        
        # checks to see if there are any keys in the dictionary, if it is empty
        if self.tempLccObj.values.keys():
           # prompts the user for id to delete from a dialog box
            text1, ok = QtGui.QInputDialog.getInt(self, 'Input Dialog', 'Enter Id of the Value to delete', minValue=0)
            if text1:                       # checks to see if a value was entered
                # Checks to see if the id entered is in the list/dictionary
                if text1 in self.tempLccObj.values.keys():
                    del self.tempLccObj.values[text1]                           # delete the id from the dictionary
                    self.displayFile()                                          # redisplay values in editor/GUI/screen
                else:                       # if value doesn't exist, prints warning message for invalid id
                    QMessageBox.warning(self, "Invalid id", "The id entered doesn't exist")
        else:                           # prints warning message concerning empty Values table
            QMessageBox.warning(self, "Values IDs", "Currently there are no Value id's")        # prints prints warning 
                                                                        # message concerning empty Values table
    def classesInsertValuesButton(self):
        print "in insert values button"
              
    def classesAddSiblingClassButton(self):
        print "in add sibling class button"
        
        global tempLccObj
        filterList = ["", "lcp", "lcosp", "rlcp", "lccc", "splcp"]
        indent = "    "
        classId = None
#        filter = None
        lcpField = None
        

        print "Class Items:"
        if self.tempLccObj.classes.items():
            print self.tempLccObj.classes.items()
        else:
            print "    No Class Items"
        print
        j = 0
        for key in self.tempLccObj.classes.keys():
            print "j is:", j
            print "key:", key
            print "classId:", self.tempLccObj.classes.values()[j].classId        
            print "name:", self.tempLccObj.classes.values()[j].name        
            print "uniqueValueIds:", self.tempLccObj.classes.values()[j].uniqueValueIds        
            print "uniqueClassIds:", self.tempLccObj.classes.values()[j].uniqueClassIds        
            print "attributes:", self.tempLccObj.classes.values()[j].attributes        
            print "parentClass:",self.tempLccObj.classes.values()[j].parentClass
            j = j + 1
            print 
                 
        
        # Input ClassId
        classId, ok = QtGui.QInputDialog.getText(self, 'Class ID', 'Enter class id:')  # format ( self, dialog title, prompt)
        classId = str(classId)
        classId = classId.lower()
        phrase = "ClassId is"

        if classId:
            print "Input is ", classId
            title = "%s %s" % (phrase, classId)
            
            for key in self.tempLccObj.classes.keys():
                if key == classId.lower():
                    # error message for duplicate Class Id
                    QMessageBox.warning(self, "ALERT - Class ID", "Id has already been used. Please enter another id ")
                    classId = None
                    return
                
            def cancel(self):
                print "Canceled!!!!"
                return

            prompt = "%s %s" %("Enter class name for ", classId)
            name, ok = QtGui.QInputDialog.getText(self, "%s %s" % (phrase, classId), prompt)
            while not name or name == "":
#                 self.cancelButton.clicked.connect(self.cancel)
                print "Name is ", name
                name, ok = QtGui.QInputDialog.getText(self, "%s %s" % (phrase, classId), "Please, enter a class name")
                print "Name is now ", name
                                                      
            filter, ok = QtGui.QInputDialog.getText(self, 'Filter', 'Enter filter to use or leave blank for None') 
                # (self, dialog title, prompt)
#            if filter in filterList:
#                print "Good Filter"
#            else:
#                filter = None
            while not filter in filterList:
                filter, ok = QtGui.QInputDialog.getText(self, 'Filter', 'Not valid filter.  Please reenter') 
                    # (self, dialog title, prompt)
                
            #####
            # check for filter
            #####
            print "Class id is %s, Class name is %s, Filter is %s" % (classId,name, filter)
#            print  self.tempLccObj.classes.values(classId).classId

            self.tempClassLCC = pylet.lcc.LandCoverClass()               # create a new LandCoverClass object
            self.tempClassLCC.addClass(classId, name, filter, lcpField)
            self.tempLccObj.classes[classId] = self.tempClassLCC
            
#            self.tempLccObj.classes.values()[classId].classId = classId
#            self.tempLccObj.classes.values()[classId].name = name        
#            print "uniqueValueIds:", self.tempLccObj.classes.values()[classId].uniqueValueIds        
#            print "uniqueClassIds:", self.tempLccObj.classes.values()[classId].uniqueClassIds        
#            print "attributes:", self.tempLccObj.classes.values()[classId].attributes        
#            print "parentClass:",self.tempLccObj.classes.values()[classId].parentClass

#            self.tempClassLCC = pylet.lcc.LandCoverClasses()
#            self.tempClassLCC.addClass(text, text2)
#            self.tempLccObj.classes[text] = self.tempClassLCC
            print self.tempLccObj.classes.items()
            
#            print "topclevelclass: ", self.tempLccObj.classes.topLevelClasses.classId, self.tempLccObj.classes.topLevelClasses.name

#        self.btn = QtGui.QPushButton("class id", self)
#        self.btn.move(20,20)
#        self.btn.clicked.connect(self.showClassId)
#        
#        self.classID = QtGui.QLineEdit(self)
#        self.classID.move(130, 22)
#        
#        self.showClassId()
        self.displayFile()                              # updates GUI to display correct values
        
    def showClassId(self):
        print "in showClassId"
#        text, ok = QtGui.QInputDialog.getText(self, 'Class ID', 'Enter class id:')

       
            
#        if ok:
#            self.classID.setText(str(text))
#        def printDescendentClasses(landCoverClass, item_0, indentUnit, indentLevel):
#            
#            for childClass in landCoverClass.childClasses:
#                assert isinstance(childClass, pylet.lcc.LandCoverClass)
#                
#                # childClass
#                item_1 = QtGui.QTreeWidgetItem(item_0)
#                item_1.setText(0, childClass.classId) #set id
#                item_1.setText(1, childClass.name)   #set name
#
#                print indentUnit*indentLevel, childClass.classId, childClass.name
#
#                for childValueId in childClass.childValueIds:
#                    
#                    childItem = QtGui.QTreeWidgetItem(item_1)
#                    childItem.setText(0, str(childValueId))
#
#                
#                printDescendentClasses(childClass,item_1, indentUnit, indentLevel + 1)
#
#        self.ClassesTree.setSortingEnabled(False)
#        
#        print "this is ", self.tempLccObj.classes.topLevelClasses
   
#        if self.tempLccObj.classes.topLevelClasses:                     # could use a try:
#            for topLevelClass in self.tempLccObj.classes.topLevelClasses:
#                assert isinstance(topLevelClass, pylet.lcc.LandCoverClass)
#                
#                try:
#                    item_0 = QtGui.QTreeWidgetItem(self.ClassesTree)
#    
#                    print 'this is toplevelClass', topLevelClass.classId, topLevelClass.name
#    
##                    item_1 = QTreeWidgetItem(item_0.setText(0, str(topLevelClass.classId)))
#                except:
#                    pass
#                printDescendentClasses(topLevelClass, item_0, indent, 2)
#
#        else:                                                           # could use an except:
#            print "in pass"
#            pass
#        print

        self.displayFile()
    def classesAddChildClassButton(self):
        print "in add child class button"
        
    def classesEditClassButton(self):
        print "in edit class button"
        
    def classesRemoveClassButton(self):
        print "in remove class button"