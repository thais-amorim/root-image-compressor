from root.ui import MainWindow
from root.compressor import LzwCompressor
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
    img = util.read_image("images/benchmark.bmp")
    compressor = LzwCompressor(img)
    compressed_img = compressor.compress()
    util.save_image("images/compressed.bmp",compressed_img)


if __name__ == "__main__":
    main()
