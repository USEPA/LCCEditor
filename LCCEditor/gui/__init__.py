

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
        self.ActionOpen.triggered.connect(self.fileOpen)
        self.ActionHelp.triggered.connect(self.help)

    #start here !!!!!!!
    def about(self):
        """Popup a box with the About message."""
 
        QMessageBox.about(self, TITLE, ABOUT_MESSAGE)

    def help(self):
        """Opens LLCEditor Help file"""
        
        pathname = os.path.dirname(_sys.argv[0]) + "\TEMP.chm"      # a file relative to running file
        os.startfile(pathname)
        
    def fileOpen(self):
        """Opens a file for viewing"""

        fileName = QFileDialog.getOpenFileName(self, "Open File", "D:\ATtILA2\src\ATtILA2\ToolboxSource\LandCoverClassifications", "LCC files (*.lcc)")
#         print fileName[0]                    # prints the name of the opened file
        
        