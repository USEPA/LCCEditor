# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainBak.ui'
#
# Created: Wed Jan 15 14:25:43 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(940, 787)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.ClassesWidget = QtGui.QWidget(MainWindow)
        self.ClassesWidget.setObjectName("ClassesWidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.ClassesWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ClassesLabel = QtGui.QLabel(self.ClassesWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        font.setBold(True)
        self.ClassesLabel.setFont(font)
        self.ClassesLabel.setObjectName("ClassesLabel")
        self.verticalLayout_4.addWidget(self.ClassesLabel)
        self.ClassesButtonsHorizontalLayout = QtGui.QHBoxLayout()
        self.ClassesButtonsHorizontalLayout.setObjectName("ClassesButtonsHorizontalLayout")
        self.ClassesInsertValuesButton = QtGui.QPushButton(self.ClassesWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(23)
        sizePolicy.setVerticalStretch(22)
        sizePolicy.setHeightForWidth(self.ClassesInsertValuesButton.sizePolicy().hasHeightForWidth())
        self.ClassesInsertValuesButton.setSizePolicy(sizePolicy)
        self.ClassesInsertValuesButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main/images/img/coins_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClassesInsertValuesButton.setIcon(icon)
        self.ClassesInsertValuesButton.setObjectName("ClassesInsertValuesButton")
        self.ClassesButtonsHorizontalLayout.addWidget(self.ClassesInsertValuesButton)
        self.ClassesAddSiblingButton = QtGui.QPushButton(self.ClassesWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ClassesAddSiblingButton.sizePolicy().hasHeightForWidth())
        self.ClassesAddSiblingButton.setSizePolicy(sizePolicy)
        self.ClassesAddSiblingButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/main/images/img/application_side_expand.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClassesAddSiblingButton.setIcon(icon1)
        self.ClassesAddSiblingButton.setObjectName("ClassesAddSiblingButton")
        self.ClassesButtonsHorizontalLayout.addWidget(self.ClassesAddSiblingButton)
        self.ClassesAddChildButton = QtGui.QPushButton(self.ClassesWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ClassesAddChildButton.sizePolicy().hasHeightForWidth())
        self.ClassesAddChildButton.setSizePolicy(sizePolicy)
        self.ClassesAddChildButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/main/images/img/application_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClassesAddChildButton.setIcon(icon2)
        self.ClassesAddChildButton.setObjectName("ClassesAddChildButton")
        self.ClassesButtonsHorizontalLayout.addWidget(self.ClassesAddChildButton)
        self.ClassesEditButton = QtGui.QPushButton(self.ClassesWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ClassesEditButton.sizePolicy().hasHeightForWidth())
        self.ClassesEditButton.setSizePolicy(sizePolicy)
        self.ClassesEditButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/main/images/img/application_edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClassesEditButton.setIcon(icon3)
        self.ClassesEditButton.setObjectName("ClassesEditButton")
        self.ClassesButtonsHorizontalLayout.addWidget(self.ClassesEditButton)
        self.ClassesRemoveButton = QtGui.QToolButton(self.ClassesWidget)
        self.ClassesRemoveButton.setAutoFillBackground(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/main/images/img/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClassesRemoveButton.setIcon(icon4)
        self.ClassesRemoveButton.setArrowType(QtCore.Qt.NoArrow)
        self.ClassesRemoveButton.setObjectName("ClassesRemoveButton")
        self.ClassesButtonsHorizontalLayout.addWidget(self.ClassesRemoveButton)
        self.verticalLayout_4.addLayout(self.ClassesButtonsHorizontalLayout)
        self.ClassesTree = QtGui.QTreeWidget(self.ClassesWidget)
        self.ClassesTree.setRootIsDecorated(True)
        self.ClassesTree.setHeaderHidden(False)
        self.ClassesTree.setObjectName("ClassesTree")
        self.ClassesTree.header().setDefaultSectionSize(100)
        self.ClassesTree.header().setMinimumSectionSize(20)
        self.verticalLayout_4.addWidget(self.ClassesTree)
        MainWindow.setCentralWidget(self.ClassesWidget)
        self.MenuBar = QtGui.QMenuBar(MainWindow)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 940, 21))
        self.MenuBar.setObjectName("MenuBar")
        self.MenuFile = QtGui.QMenu(self.MenuBar)
        self.MenuFile.setObjectName("MenuFile")
        self.MenuHelp = QtGui.QMenu(self.MenuBar)
        self.MenuHelp.setObjectName("MenuHelp")
        self.MenuImport = QtGui.QMenu(self.MenuBar)
        self.MenuImport.setObjectName("MenuImport")
        MainWindow.setMenuBar(self.MenuBar)
        self.ValuesDock = QtGui.QDockWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        font.setBold(True)
        self.ValuesDock.setFont(font)
        self.ValuesDock.setObjectName("ValuesDock")
        self.ValuesDockContents = QtGui.QWidget()
        self.ValuesDockContents.setObjectName("ValuesDockContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.ValuesDockContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ValuesButtonsHorizontalLayout = QtGui.QHBoxLayout()
        self.ValuesButtonsHorizontalLayout.setObjectName("ValuesButtonsHorizontalLayout")
        self.ValuesIncludeAllButton = QtGui.QPushButton(self.ValuesDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ValuesIncludeAllButton.sizePolicy().hasHeightForWidth())
        self.ValuesIncludeAllButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setWeight(50)
        font.setBold(False)
        self.ValuesIncludeAllButton.setFont(font)
        self.ValuesIncludeAllButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/main/images/img/accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ValuesIncludeAllButton.setIcon(icon5)
        self.ValuesIncludeAllButton.setObjectName("ValuesIncludeAllButton")
        self.ValuesButtonsHorizontalLayout.addWidget(self.ValuesIncludeAllButton)
        self.ValuesAddButton = QtGui.QPushButton(self.ValuesDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ValuesAddButton.sizePolicy().hasHeightForWidth())
        self.ValuesAddButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setWeight(50)
        font.setBold(False)
        self.ValuesAddButton.setFont(font)
        self.ValuesAddButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/main/images/img/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ValuesAddButton.setIcon(icon6)
        self.ValuesAddButton.setObjectName("ValuesAddButton")
        self.ValuesButtonsHorizontalLayout.addWidget(self.ValuesAddButton)
        self.ValuesRemoveButton = QtGui.QPushButton(self.ValuesDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ValuesRemoveButton.sizePolicy().hasHeightForWidth())
        self.ValuesRemoveButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setWeight(75)
        font.setBold(True)
        self.ValuesRemoveButton.setFont(font)
        self.ValuesRemoveButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/main/images/img/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ValuesRemoveButton.setIcon(icon7)
        self.ValuesRemoveButton.setObjectName("ValuesRemoveButton")
        self.ValuesButtonsHorizontalLayout.addWidget(self.ValuesRemoveButton)
        self.verticalLayout.addLayout(self.ValuesButtonsHorizontalLayout)
        self.ValuesTree = QtGui.QTreeWidget(self.ValuesDockContents)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.ValuesTree.setFont(font)
        self.ValuesTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ValuesTree.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.ValuesTree.setObjectName("ValuesTree")
        self.ValuesTree.header().setDefaultSectionSize(121)
        self.ValuesTree.header().setMinimumSectionSize(4)
        self.ValuesTree.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.ValuesTree)
        self.ValuesDock.setWidget(self.ValuesDockContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.ValuesDock)
        self.MetadataDock = QtGui.QDockWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        font.setBold(True)
        self.MetadataDock.setFont(font)
        self.MetadataDock.setObjectName("MetadataDock")
        self.MetadataDockContents = QtGui.QWidget()
        self.MetadataDockContents.setObjectName("MetadataDockContents")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.MetadataDockContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.MetadataNameLabel = QtGui.QLabel(self.MetadataDockContents)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.MetadataNameLabel.setFont(font)
        self.MetadataNameLabel.setObjectName("MetadataNameLabel")
        self.verticalLayout_3.addWidget(self.MetadataNameLabel)
        self.MetadataNameLineEdit = QtGui.QLineEdit(self.MetadataDockContents)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.MetadataNameLineEdit.setFont(font)
        self.MetadataNameLineEdit.setObjectName("MetadataNameLineEdit")
        self.verticalLayout_3.addWidget(self.MetadataNameLineEdit)
        self.MetadataDescriptionLabel = QtGui.QLabel(self.MetadataDockContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(50)
        font.setBold(False)
        self.MetadataDescriptionLabel.setFont(font)
        self.MetadataDescriptionLabel.setObjectName("MetadataDescriptionLabel")
        self.verticalLayout_3.addWidget(self.MetadataDescriptionLabel)
        self.MetadataDescriptionTextEdit = QtGui.QPlainTextEdit(self.MetadataDockContents)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.MetadataDescriptionTextEdit.setFont(font)
        self.MetadataDescriptionTextEdit.setObjectName("MetadataDescriptionTextEdit")
        self.verticalLayout_3.addWidget(self.MetadataDescriptionTextEdit)
        self.MetadataDock.setWidget(self.MetadataDockContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.MetadataDock)
        self.ToolBar = QtGui.QToolBar(MainWindow)
        self.ToolBar.setObjectName("ToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.ToolBar)
        self.ActionNew = QtGui.QAction(MainWindow)
        self.ActionNew.setObjectName("ActionNew")
        self.ActionOpen = QtGui.QAction(MainWindow)
        self.ActionOpen.setObjectName("ActionOpen")
        self.ActionSave = QtGui.QAction(MainWindow)
        self.ActionSave.setObjectName("ActionSave")
        self.ActionQuit = QtGui.QAction(MainWindow)
        self.ActionQuit.setObjectName("ActionQuit")
        self.ActionSaveAs = QtGui.QAction(MainWindow)
        self.ActionSaveAs.setObjectName("ActionSaveAs")
        self.ActionImportFromRaster = QtGui.QAction(MainWindow)
        self.ActionImportFromRaster.setObjectName("ActionImportFromRaster")
        self.ActionImportFromLcc = QtGui.QAction(MainWindow)
        self.ActionImportFromLcc.setObjectName("ActionImportFromLcc")
        self.ActionHelp = QtGui.QAction(MainWindow)
        self.ActionHelp.setObjectName("ActionHelp")
        self.ActionAbout = QtGui.QAction(MainWindow)
        self.ActionAbout.setObjectName("ActionAbout")
        self.ActionValuesShowHide = QtGui.QAction(MainWindow)
        self.ActionValuesShowHide.setCheckable(True)
        self.ActionValuesShowHide.setChecked(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/main/images/img/coins.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ActionValuesShowHide.setIcon(icon8)
        self.ActionValuesShowHide.setObjectName("ActionValuesShowHide")
        self.ActionMetadataShowHide = QtGui.QAction(MainWindow)
        self.ActionMetadataShowHide.setCheckable(True)
        self.ActionMetadataShowHide.setChecked(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/main/images/img/database.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ActionMetadataShowHide.setIcon(icon9)
        self.ActionMetadataShowHide.setObjectName("ActionMetadataShowHide")
        self.MenuFile.addAction(self.ActionNew)
        self.MenuFile.addAction(self.ActionOpen)
        self.MenuFile.addSeparator()
        self.MenuFile.addAction(self.ActionSave)
        self.MenuFile.addAction(self.ActionSaveAs)
        self.MenuFile.addSeparator()
        self.MenuFile.addAction(self.ActionQuit)
        self.MenuHelp.addAction(self.ActionHelp)
        self.MenuHelp.addSeparator()
        self.MenuHelp.addAction(self.ActionAbout)
        self.MenuImport.addAction(self.ActionImportFromRaster)
        self.MenuBar.addAction(self.MenuFile.menuAction())
        self.MenuBar.addAction(self.MenuImport.menuAction())
        self.MenuBar.addAction(self.MenuHelp.menuAction())
        self.ToolBar.addAction(self.ActionValuesShowHide)
        self.ToolBar.addAction(self.ActionMetadataShowHide)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.ActionValuesShowHide, QtCore.SIGNAL("triggered(bool)"), self.ValuesDock.setVisible)
        QtCore.QObject.connect(self.ActionMetadataShowHide, QtCore.SIGNAL("triggered(bool)"), self.MetadataDock.setVisible)
        QtCore.QObject.connect(self.ActionQuit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.MetadataNameLineEdit, self.MetadataDescriptionTextEdit)
        MainWindow.setTabOrder(self.MetadataDescriptionTextEdit, self.ClassesAddChildButton)
        MainWindow.setTabOrder(self.ClassesAddChildButton, self.ClassesEditButton)
        MainWindow.setTabOrder(self.ClassesEditButton, self.ClassesRemoveButton)
        MainWindow.setTabOrder(self.ClassesRemoveButton, self.ClassesTree)
        MainWindow.setTabOrder(self.ClassesTree, self.ValuesRemoveButton)
        MainWindow.setTabOrder(self.ValuesRemoveButton, self.ValuesTree)
        MainWindow.setTabOrder(self.ValuesTree, self.ClassesInsertValuesButton)
        MainWindow.setTabOrder(self.ClassesInsertValuesButton, self.ClassesAddSiblingButton)
        MainWindow.setTabOrder(self.ClassesAddSiblingButton, self.ValuesAddButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Land Cover Classification Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesLabel.setText(QtGui.QApplication.translate("MainWindow", "CLASSES", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesInsertValuesButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Insert Values", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesAddSiblingButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Add Sibling Class", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesAddChildButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Add Child Class", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesEditButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Edit Class", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesRemoveButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove Class", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesRemoveButton.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesTree.setSortingEnabled(True)
        self.ClassesTree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "id", None, QtGui.QApplication.UnicodeUTF8))
        self.ClassesTree.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.MenuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.MenuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.MenuImport.setTitle(QtGui.QApplication.translate("MainWindow", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.ValuesDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "VALUES", None, QtGui.QApplication.UnicodeUTF8))
        self.ValuesIncludeAllButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Include All", None, QtGui.QApplication.UnicodeUTF8))
        self.ValuesAddButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Add Value", None, QtGui.QApplication.UnicodeUTF8))
        self.ValuesRemoveButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove Value", None, QtGui.QApplication.UnicodeUTF8))
        self.ValuesTree.setSortingEnabled(True)
        self.ValuesTree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "id", None, QtGui.QApplication.UnicodeUTF8))
        self.ValuesTree.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.ValuesTree.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "excluded", None, QtGui.QApplication.UnicodeUTF8))
        self.MetadataDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "METADATA", None, QtGui.QApplication.UnicodeUTF8))
        self.MetadataNameLabel.setText(QtGui.QApplication.translate("MainWindow", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.MetadataDescriptionLabel.setText(QtGui.QApplication.translate("MainWindow", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolBar.setToolTip(QtGui.QApplication.translate("MainWindow", "Show/Hide Values", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionNew.setText(QtGui.QApplication.translate("MainWindow", "&New...", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionOpen.setText(QtGui.QApplication.translate("MainWindow", "&Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionSave.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionSaveAs.setText(QtGui.QApplication.translate("MainWindow", "Save &As...", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionImportFromRaster.setText(QtGui.QApplication.translate("MainWindow", "From Raster...", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionImportFromLcc.setText(QtGui.QApplication.translate("MainWindow", "From LCC File...", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionHelp.setText(QtGui.QApplication.translate("MainWindow", "LCCEditor &Help", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionAbout.setText(QtGui.QApplication.translate("MainWindow", "About LCCEditor", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionValuesShowHide.setText(QtGui.QApplication.translate("MainWindow", "Show/Hide Values", None, QtGui.QApplication.UnicodeUTF8))
        self.ActionMetadataShowHide.setText(QtGui.QApplication.translate("MainWindow", "Show/Hide Metadata", None, QtGui.QApplication.UnicodeUTF8))

import main_rc
