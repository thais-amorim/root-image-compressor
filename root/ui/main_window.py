from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5. QtGui import *
from root.ui import SideBar
from root.ui import ImageView
from root.ui import Window
import sys
import numpy as np


class MainWindow(Window):

    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout()
        self.initToolBar()
        self.initMenuBar()
        self.setLayouts()

    def setLayouts(self):

        self.main_layout.addWidget(self.imageView)
        self.main_layout.addWidget(self.side_bar)
        self.main_layout.setStretch(0, 40)

        main_widget = QWidget()
        main_widget.setObjectName("main-widget")
        main_widget.setLayout(self.main_layout)
        main_widget.setStyleSheet(
            "QWidget#main-widget{ border:2px solid rgb(150,150, 150);} ")
        self.setCentralWidget(main_widget)

    def initMenuBar(self):

        self.statusBar()

        # menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        compressMenu = mainMenu.addMenu("Compress")
        uncompressMenu = mainMenu.addMenu("Uncompress")

        # fileMenu
        closeAction = QAction("&Exit", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.setStatusTip("Leave The App")
        closeAction.triggered.connect(self.closeApplication)

        fileMenu.addAction(closeAction)

    def initToolBar(self):
        openAction = QAction(QtGui.QIcon(
            'assets/icons/open.png'), "&Open Ctrl+O", self)
        saveAction = QAction(QtGui.QIcon(
            'assets/icons/save.png'), "&Save Ctrl+S", self)
        saveAllAction = QAction(QtGui.QIcon(
            'assets/icons/save-as.png'), "&Save As Ctrl+Shift+S", self)
        undoAction = QAction(QtGui.QIcon(
            'assets/icons/undo.png'), "&Undo Ctrl+Z", self)
        redoAction = QAction(QtGui.QIcon(
            'assets/icons/redo.png'), "&Redo Ctrl+R", self)
        brushAction = QAction(QtGui.QIcon(
            'assets/icons/brush.png'), "&Brush", self)

        openAction.setShortcut("Ctrl+O")
        saveAction.setShortcut("Ctrl+S")
        saveAllAction.setShortcut("Ctrl+Shift+S")
        undoAction.setShortcut(QtGui.QKeySequence("Ctrl+Z"))
        redoAction.setShortcut(QtGui.QKeySequence("Ctrl+Y"))

        openAction.triggered.connect(self.fileOpen)
        saveAction.triggered.connect(self.saveFile)
        undoAction.triggered.connect(self.undoLastAction)
        redoAction.triggered.connect(self.redoLastAction)

        self.toolbar = self.addToolBar("Extraction")

        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(saveAllAction)
        self.toolbar.addAction(undoAction)
        self.toolbar.addAction(redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(brushAction)
