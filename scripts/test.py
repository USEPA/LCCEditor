# Example of how to make a popup window (second window) with complex layout.
# 
# By Zak Fallows
# 2012-12-21

import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *

class MainWindow(QDialog):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.setWindowTitle("Main Window")
        
        self.top_label = QLabel("Middle of main window")
        
        self.bottom_button = QPushButton("Add Name")
        
        layout = QVBoxLayout()
        layout.addWidget(self.top_label)
        layout.addWidget(self.bottom_button)
        self.setLayout(layout)
        
        self.connect(self.bottom_button, SIGNAL("clicked()"),
                     self.button_clicked)
    
    def button_clicked(self):
        self.popup_window = PopupWindow(self)
        self.popup_window.show()

class PopupWindow(QDialog):
    
    def __init__(self, parent=None):
        super(PopupWindow, self).__init__(parent)
        
        self.setWindowTitle("Popup Window")
        layout = QGridLayout()
        
        line1 = QLabel("What is your first name?")
        layout.addWidget(line1, 0, 0)
        self.line1_edit = QLineEdit()
        layout.addWidget(self.line1_edit, 0, 1)
        
        line2 = QLabel("What is your occupation?")
        layout.addWidget(line2, 1, 0)
        self.line2_edit = QLineEdit()
        layout.addWidget(self.line2_edit, 1, 1)
        
        line3 = QLabel("How many years have you had this job?")
        layout.addWidget(line3, 2, 0)
        self.line3_edit = QLineEdit()
        layout.addWidget(self.line3_edit, 2, 1)
        
        line4 = QLabel("Do you want email?")
        layout.addWidget(line4, 3, 0)
        self.line4_checkbox = QCheckBox()
        layout.addWidget(self.line4_checkbox, 3, 1)
        
        self.setLayout(layout)

app = QApplication(sys.argv)

main_window = MainWindow()
main_window.resize(400, 400)
main_window.show()
# The .raise_() brings the window to the foreground, in front of other windows
main_window.raise_()

app.exec_()
sys.exit()