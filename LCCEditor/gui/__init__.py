
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
from pprint import pprint

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
        self.ValuesAddButton.clicked.connect(self.addValueButton)
        self.ValuesRemoveButton.clicked.connect(self.deleteValueButton)
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
        """Displays the file """
        
        ten = "10"
        indent = "    "
        
        self.clearLccItems()
        

        self.ValuesTree.setSortingEnabled(True)
#        self.ValuesTree.sortByColumn(0,Qt.AscendingOrder)
      
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
            
            for childClass in landCoverClass.childClasses:
                assert isinstance(childClass, pylet.lcc.LandCoverClass)
                
                # childClass
                item_1 = QtGui.QTreeWidgetItem(item_0)
                item_1.setText(0, childClass.classId) #set id
                item_1.setText(1, childClass.name)   #set name

#                print indentUnit*indentLevel, childClass.classId, childClass.name

                for childValueId in childClass.childValueIds:
                    
                    childItem = QtGui.QTreeWidgetItem(item_1)
                    childItem.setText(0, str(childValueId))

                
                printDescendentClasses(childClass,item_1, indentUnit, indentLevel + 1)

        self.ClassesTree.setSortingEnabled(False)
   
        for topLevelClass in self.tempLccObj.classes.topLevelClasses:
            assert isinstance(topLevelClass, pylet.lcc.LandCoverClass)
            
            try:
                item_0 = QtGui.QTreeWidgetItem(self.ClassesTree)

                item_0.setText(0, str(topLevelClass.classId))
                item_0.setText(1, str(topLevelClass.name))

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
                outFileName.write('<class  id="')
                outFileName.write(str(childClass.classId))    #set id
                outFileName.write('" name="')
                outFileName.write(str(childClass.name))       #set name
                outFileName.write('" filter="')
                outFileName.write('" <lcosp>')
                outFileName.write('" >')
                outFileName.write("\n")

                for childValueId in childClass.childValueIds:
                    outFileName.write(indentUnit*(indentLevel+1))
                    outFileName.write('<value id="')
                    outFileName.write(str(childValueId))
                    outFileName.write('" />')
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
        
    def addValueButton(self):
        global tempLccObj
        
        # prompts user input from a Input Dialog Box
        text1, ok = QtGui.QInputDialog.getInt(self, 'Input Dialog', 'Enter Id of the Value', minValue=0)
        
        # checks to see if value was entered
        if text1:
            self.tempLccObj.values.valueId = text1                  # set key value to entered value

            # checks if value exists in dictionary
            for key in self.tempLccObj.values.keys():
                if key == text1:
                    QMessageBox.warning(self, "ALERT - Value ID", "Id has already been used. Please enter another id "
                    + "or delete id then reenter")
                    return

            # prompts user for value and whether excluded
            text2, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter name of the Value')
            text2 = text2.title()           # capitalizes first letter of each word

            text3, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Excluded( Enter yes or no')
            text3 = text3.lower()           # changes string to lower characters

#            while text3 != "yes" or text3 != "no":
#                text3, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Excluded( Enter yes or no')
#                text3 = text3.lower()           # changes string to lower characters

                          
            self.tempLCV = pylet.lcc.LandCoverValue()               # create a new LandCoverValue object
           
            self.tempLCV.addValues(text1, text2, text3)             # populate the object
            
            self.tempLccObj.values[text1] = (self.tempLCV)          # populate the keys with the objects
        
#        keys = self.tempLccObj.values.keys()
#        values = self.tempLccObj.values.values()
            
    #        print type(self.tempLccObj.values)
            
            #checks if list is empty
#        if not keys:
#            pass
#        else:
#            print "These are keys:"
#            print keys
#        if not values:
#            pass
#        else:
#            print "Theres are values:"
#            print values
#        if not keys:
#            pass
#        else:    
#            print "These are the items"
#            print self.tempLccObj.values.items()
#        
#        print text3   
#            self.displayFile(self)

#        self.addButton.clicked.connect(self.addValueButtonDialog)
        for value in self.tempLccObj.values.values():                       # prints value for the Value Tree
            try:
                print value.valueId
                print value.name
            except:
                print "in except"
                pass

        print
        self.displayFile()
                                            
    def deleteValueButton(self):
        global tempLccObj                   # global object
        
#        found = None                        # variable assignment, to be used to check if 
        
#        print "In deleteValueButton"
        # checks to see if there are any keys in the dictionary
        if self.tempLccObj.values.keys():
#            tempDVB = pylet.lcc.LandCoverClassification()               # creates an object for 
#            
#            self.tempDVB = self.tempLccObj
#            
#            print self.tempDVB
    #        
            for value in self.tempLccObj.values.values():                       # prints value for the Value Tree
    #            assert isinstance(value, pylet.lcc.LandCoverValue)      # activates auto-completion      
    #            print value.valueId, value.name, value.excluded
                try:
    
                    print value.valueId
                    print value.name
                except:
                    print "in except"
                    pass
            # Gets id to delete
            text1, ok = QtGui.QInputDialog.getInt(self, 'Input Dialog', 'Enter Id of the Value to delete', minValue=0)
            
            if text1:
    #            self.tempLccObj.values.valueId = text1
                text1 = int(text1)
                print "This is keys", self.tempLccObj.values.keys()
                
                if text1 in self.tempLccObj.values.keys():
                    del self.tempLccObj.values[text1]
                    self.displayFile()
                elif not self.tempLccObj.values.keys():
                    QMessageBox.warning(self, "No ids", "no id's exist")
                else:
                    print "error, no id"
                
    #            for key in self.tempLccObj.values.keys():
    #                print "This is key", key
    #                print "THis is text1", text1
    #                print self.tempLccObj.values.keys()
    #                if key == text1:
    #                    print "in del" 
    #                    found = True       
    #                    del self.tempLccObj.values[text1]
    #                    print self.tempLccObj.values.keys()
    #                    self.displayFile()
    #
    #            if not found:
    #                print "in else"
    #                QMessageBox.about(self, "ALERT", "Id doesn't exist.")
    #        else:
    #            print "in pass"
    #            pass
            
    #        found = None
        else:
            QMessageBox.warning(self, "Values IDs", "Currently there are no Value id's")
              
    def addValueButtonDialog(self):
        print "In widget"
        item_0 = QtGui.QTreeWidgetItem(self.ValuesTree)        
        
        item_0.setText(0, self.edit1.text())
        item_0.setText(1, self.edit2.text())
