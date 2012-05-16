

""" Graphical User Interface (GUI) for the Land Cover Classification Editor (LCCEditor)

    The main() function launches the LCCEditor MainWindow

"""

from PySide.QtGui import QMainWindow as _QMainWindow
from PySide.QtGui import QPushButton as _QPushButton
from PySide.QtGui import QApplication as _QApplication
from PySide.QtGui import QMessageBox        # needed for about 
#from PySide.QtGui import QTextEdit
from PySide.QtGui import QFileDialog        # needed for open
#from PySide.QtCore import QIODevice


from main_ui import Ui_MainWindow
import sys as _sys
import platform                             # needed for platform details
import PySide                               # needed for version
import os
import pylet
from PySide import QtCore, QtGui


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
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ActionAbout.triggered.connect(self.about)
        self.ActionHelp.triggered.connect(self.help)
        self.ActionOpen.triggered.connect(self.fileOpen)
 #           self.lccFileDir for relative/absolute path
        
    #start here !!!!!!!
    def about(self):
        """Popup a box with the About message."""
 
        QMessageBox.about(self, TITLE, ABOUT_MESSAGE)

    def help(self):
        """Opens LLCEditor Help file"""
        
        pathname = os.path.dirname(_sys.argv[0]) + "\TEMP.chm"      # a file relative to running file
        os.startfile(pathname)
    
    def clearLccItems(self):
        """ Clear all the LCC items in dialog loaded from file"""
        
        self.ValuesTree.clear()
        self.ClassesTree.clear()
        self.MetadataNameLineEdit.setText('')                
        self.MetadataDescriptionTextEdit.setPlainText('') 
        
    def fileOpen(self):
        """Opens a file for viewing"""
        



        # path will eventually be gotten from a config file through _init__
        fileName = QFileDialog.getOpenFileName(self, "Open File", 
                                "D:\ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications", "LCC files (*.lcc)")[0] # might have to use '/home'
        
        # Exit if user selected cancel in the dialog
        if not fileName:
            return
        
        # Clear the dialog of loaded/created items
        self.clearLccItems()

        # Load the input file
        lccObj = pylet.lcc.LandCoverClassification(fileName)         # create a LandCoverClassification object


        self.ValuesTree.setSortingEnabled(False)
        
        # Load values 
        for value in lccObj.values.values():                       # prints value for the Value Tree
            assert isinstance(value, pylet.lcc.LandCoverValue)      # activates auto-completion      
#            print value.valueId, value.name, value.excluded
            try:

                item_0 = QtGui.QTreeWidgetItem(self.ValuesTree)
                
                if(value.excluded):
                    item_0.setCheckState(2, QtCore.Qt.Checked)
                else:
                    item_0.setCheckState(2, QtCore.Qt.Unchecked)

                item_0.setText(0, str(value.valueId))
                item_0.setText(1, str(value.name))
                

           
            except:
                pass
            

        # Load classes
        for count, classes in enumerate(lccObj.classes.values()):                     # prints value for the Class Tree
            assert isinstance(classes, pylet.lcc.LandCoverClass)    # activates auto-completion 
        
#            print classes.classId, classes.name, classes.uniqueValueIds

 #           try:
 #               print "in try"
  #              self.ClassesTree.setSortingEnabled(False)
#                item_0 = QtGui.QTreeWidgetItem(self.ClassesTree)
                
#                self.ClassesTree.topLevelItem(count).setText(0, QtGui.QApplication.translate("MainWindow", 
#                                str(classes.classId), None, QtGui.QApplication.UnicodeUTF8))
#                self.ClassesTree.topLevelItem(count).setText(1, QtGui.QApplication.translate("MainWindow", 
#                                str(classes.name), None, QtGui.QApplication.UnicodeUTF8))
                
#                self.ClassesTree.topLevelItem(count).child(0).setText(0, QtGui.QApplication.translate("MainWindow", 
#                               str(classes.uniqueValueIds), None, QtGui.QApplication.UnicodeUTF8))
#                self.ClassesTree.topLevelItem(count).child(0).setText(1, QtGui.QApplication.translate("MainWindow",
#                               str(classes.name), None, QtGui.QApplication.UnicodeUTF8))
                
#                self.ClassesTree.topLevelItem(count).child(0).child(0).setText(0, QtGui.QApplication.translate("MainWindow", 
 #                               "3", None, QtGui.QApplication.UnicodeUTF8))
 #               self.ClassesTree.topLevelItem(count).child(0).child(0).setText(1, QtGui.QApplication.translate("MainWindow", 
 #                               "test", None, QtGui.QApplication.UnicodeUTF8))
                
 #           except:
 #               pass
            
        # Load Metadata Name
        metadataName = lccObj.metadata.name
        self.MetadataNameLineEdit.setText(metadataName)                     # prints the metadata name
        
        #Load Metadata Description
        metadataDescription = lccObj.metadata.description
        self.MetadataDescriptionTextEdit.setPlainText(metadataDescription)  # prints the metadata description

