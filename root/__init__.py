from root.ui import MainWindow
from root.compressor import Huffman
from root.util import ImageUtil as util
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
sys.path.insert(0, sys.path[0] + '\\ui')
print(sys.path)


def main():
    #    app = QApplication([])
    #    GUI = MainWindow()
    #    app.exec_()
    compressor = Huffman("images/benchmark.bmp")
    compressor.compress()


if __name__ == "__main__":
    main()
