
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
    lccObj = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ActionAbout.triggered.connect(self.about)
        self.ActionHelp.triggered.connect(self.helpMenu)
        self.ActionOpen.triggered.connect(self.fileOpen)
        self.ActionSave.triggered.connect(self.fileSave)
        self.ActionNew.triggered.connect(self.clearLccItems)
        
        self.ValuesAddButton.clicked.connect(self.addValueButton)
#        self.ValuesAddButton.connect(addValueButton(),QtCore.SIGNAL("triggered()"),self.addValueButton)
#        self.ValuesAddButton.triggered.connect(self.addValue)
#       QtCore.QObject.connect(self.ValuesAddButt on, QtCore.SIGNAL("triggered(bool)"))self.ValuesTree.addTopLevelItem()
#           self.lccFileDir for relative/absolute path
        
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
        
#    def ValueAddButton(self):
#        self.ValuesTree.clear()
        
    def fileOpen(self):
        """Opens a file for viewing"""
        ten = "10"
        indent = "    "
        global fileName, tempFileName, lccObj

        # path will eventually be gotten from a config file through _init__
        self.fileName = QFileDialog.getOpenFileName(self, "Open File", 
                                "D:\ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications", "LCC files (*.lcc)")[0] # might have to use '/home'
        self.tempFileName = self.fileName.split('.')

        self.tempFileName = self.tempFileName[0] + ".tmp"             # building temporary file name
        # Exit if user selected cancel in the dialog
        if not self.fileName:
            return
        
        # Clear the dialog of loaded/created items
        self.clearLccItems()

        # Load the input file
        self.lccObj = pylet.lcc.LandCoverClassification(self.fileName)         # create a LandCoverClassification object

        self.ValuesTree.setSortingEnabled(False)
      
        # Load values 
        for value in self.lccObj.values.values():                       # prints value for the Value Tree
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
   
        for topLevelClass in self.lccObj.classes.topLevelClasses:
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
        metadataName = self.lccObj.metadata.name
        self.MetadataNameLineEdit.setText(metadataName)
        
        # Load Metadata Description
        metadataDescription = self.lccObj.metadata.description
        self.MetadataDescriptionTextEdit.setPlainText(metadataDescription)
        
    def fileSave(self):
        
#        from os.path import isfile
        
        global lccObj
        indent = "    "

        root_dir = os.path.join(".",'\ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications')
        outFileName = QFileDialog.getSaveFileName(self,'Save File',root_dir,"LCC files (*.lcc)")[0]
        print 'out file name is', outFileName
        if not outFileName:
            return
        outFileName = open(outFileName,'w')
#        print "This is the in file name", fileName
        print 'This is tempFileName', self.tempFileName
#        print 'This is lccObj', lccObj
        container = 'ATtILA2{0}ToolboxSource'.format(os.sep)
        print "container is ", container
        dirName = pylet.lcc.constants.PredefinedFileDirName
        print "dirName is ", dirName
        
        # File Output starts here        
        outFileName.write('<root>')
        outFileName.write("\n")
        outFileName.write("\n")
        
        outFileName.write(indent)
        outFileName.write('<metadata>')
        outFileName.write("\n")

        try:
            outFileName.write(indent)
            outFileName.write(indent)
            outFileName.write('<name>')
            outFileName.write(str(self.lccObj.metadata.name))
            outFileName.write('<name>')
            outFileName.write("\n")
            outFileName.write(indent)
            outFileName.write(indent)
            outFileName.write('<description>')
            outFileName.write(str(self.lccObj.metadata.description))
            outFileName.write('</description>')
            outFileName.write("\n")
            
        except:  
            pass  

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
        
        for value in self.lccObj.values.values():                       # prints value for the Value Tree
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

#                print indentUnit*indentLevel, childClass.classId, childClass.name

                for childValueId in childClass.childValueIds:
                    outFileName.write(indentUnit*(indentLevel+1))
                    outFileName.write('<value id="')
                    outFileName.write(str(childValueId))
                    outFileName.write('" />')
                    outFileName.write("\n")
                
                printDescendentClasses(childClass,item_1, indentUnit, indentLevel + 1)
        
        for topLevelClass in self.lccObj.classes.topLevelClasses:
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
#                outFileName.write( <lcpFieldType>)
                outFileName.write('" filter="')
#                outFileName.write( <lcosp>)
                outFileName.write('" >')
                outFileName.write("\n")

                printDescendentClasses(topLevelClass, item_0, indent, 3)
                
                outFileName.write(indent)
                outFileName.write(indent)
                outFileName.write('</class>')
                outFileName.write("\n")
                
            except:
                pass
            
        outFileName.write(indent)
        outFileName.write('</classes>')
        

        outFileName.write("\n")
        outFileName.write('</root>')
        
        outFileName.close()



#        outFileName = open('self.tempFileName', 'w')
        
#        for value in lccObj.values.values():                       # prints value for the Value Tree
#            assert isinstance(value, pylet.lcc.LandCoverValue)      # activates auto-completion      
#            print outFileName.write(str(value.valueId))
#            print outFileName.write('\n')
#            print outFileName.write(str(value.name))
#            print outFileName.write('\n')
#            print outFileName.write(str(value.excluded))
#            print outFileName.write('\n')
            
#        root_dir = os.path.abspath(os.path.dirname(__file__))
#        print 'root_dir ', root_dir
#        root_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
#        print 'root_dir ', root_dir
#        root_dir = os.path.join(".",'\ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications')
#        print 'root_dir ', root_dir
        
        
#        print self.fileOpen().lccObj.values.value
        
#        outFileName = open(QFileDialog.getSaveFileName(self,'Save File',root_dir,"LCC files (*.lcc)")[0],'w')
#        print outFileName.write('This sucks')
#        curfile = "In the Save"
#        item_0 = QtGui.QTreeWidgetItem(self.ClassesTree)
#        dom = parse(outFileName)
#        x = dom.createElement('metadata')       # creates <metadata />
#        dom.childNodes[1].appendChild(x)
#        print "this is dom to xml", dom.toxml()


#        dom = parse(str(outFileName))
#
#        def getChildrenByTitle(node):
#            for child in node.childNodes:
#                if child.localName=='Title':
#                    yield child
#
#        Topic=dom.getElementsByTagName('Topic')
#        for node in Topic:
#            alist=getChildrenByTitle(node)
#            for a in alist:
##                Title= a.firstChild.data
#                Title= a.childNodes[0].nodeValue
#                print Title
        
    def addValueButton(self):
        
        self.edit1 = QLineEdit("Input ID")
        self.edit2 = QLineEdit("Input Value")
        self.addButton = QPushButton("Add")
        
        layout = QVBoxLayout()
        layout.addWidget(self.edit1)
        layout.addWidget(self.edit2)
        layout.addWidget(self.addButton)
        
        self.setLayout(layout)
        
        self.addButton.clicked.connect(self.addValueButtonDialog)
        
        print "In AddValueButton"
        
    def addValueButtonDialog(self):
        print "In widget"
        item_0 = QtGui.QTreeWidgetItem(self.ValuesTree)        
        
        item_0.setText(0, self.edit1.text())
        item_0.setText(1, self.edit2.text())
