from root.ui import MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
sys.path.insert(0, sys.path[0] + '\\ui')
print(sys.path)


def main():
    app = QApplication([])
    GUI = MainWindow()
    app.exec_()


if __name__ == "__main__":
    main()
