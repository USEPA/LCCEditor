''' Build compiled version of Graphical User Interface

'''

from glob import glob
import os
from subprocess import call


MATCH_QRC = "*.qrc"
MATCH_UI = "*.ui"
EXE_COMPILE_UI = "pyside-uic" # Add C:\Python26\ArcGIS10.0\Scripts to PythonPath
EXE_COMPILE_QRC = "pyside-rcc" # Add C:\Python26\ArcGIS10.0\Lib\site-packages\PySide to PythonPath
EXE_COMPILE_ARG = "-o"
GUI_MODULE_NAME = "gui"
MSG_CONVERT_DELIMITER = " --> "
MSG_CONVERT = "\nCompiling gui files..."
INDENT = "  "
QRC_SUFFIX = "_rc.py"
UI_SUFFIX = "_ui.py"

def main():
    buildGui()


def buildGui():
    """ Build compiled Python files from Qt Creator project files.
    
        To edit project files, open LCCEditor.pro with Qt Creator (Included with Qt SDK, http://qt.nokia.com/)
        
        Initial files:
          main_rc.qrc is compiled to main_rc.py
          main_ui.ui is compiled to main_ui.py
          
        Anticipating future files:
          Any .qrc or .ui file will be comipiled to a .py file with the same name
        
    """
    print MSG_CONVERT
    
    # Get original working directory for reset at end
    startDir = os.curdir
    
    # Change working directory to Qt Creator project directory 
    splitPath = __file__.split(os.sep)[0:-2]
    rootDir = splitPath[0] + os.sep + os.path.join(*splitPath[1:])
    projectDir = os.path.join(rootDir, splitPath[-1], GUI_MODULE_NAME)
    os.chdir(projectDir)
    
    # convert all .qrc files to .py files with same name
    compileFiles(MATCH_QRC, EXE_COMPILE_QRC, QRC_SUFFIX)

    #convert all .ui files to .py files with same name
    compileFiles(MATCH_UI, EXE_COMPILE_UI, UI_SUFFIX)
    
    # Reset original working directory
    os.chdir(startDir)
    
def compileFiles(matchString, exeName, suffix):
    """ Compile GUI files 
    
        convertMsg:  initial message to display
        matchString:  glob for files matching this pattern
        exeName: name of executeable (expected to be in PATH variable)
        
    """
    filePaths = glob(matchString)
    for filePath in filePaths:
        outName = filePath.split(".")[0] + suffix
        print "    ", filePath, MSG_CONVERT_DELIMITER, outName
        args = [exeName, filePath, EXE_COMPILE_ARG, outName]
        call(args)
    

if __name__ == "__main__":
    buildGui()