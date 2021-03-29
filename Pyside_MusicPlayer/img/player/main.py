# This Python file uses the following encoding: utf-8
import sys
import os

import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic

app = QtWidgets.QApplication(sys.argv)


if __name__ == "__main__":
    window = uic.loadUi("form.ui")
    window.show()
    app.exec()
