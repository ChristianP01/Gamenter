from PyQt6 import uic
from PyQt6 import QtCore, QtGui, QtWidgets
from whoosh.query import *
from whoosh.fields import Schema, TEXT
import sys
import os.path
from whoosh.index import create_in
import main

baseUIClass, baseUIWidget = uic.loadUiType("gui.ui")

class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        #self.resultsText.setPlainText( main.searchQuery(self, str( self.userQuery.toPlainText() )) )
        self.pushButton.clicked.connect(lambda: main.searchQuery(self, str(self.userQuery.toPlainText())) )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Logic(None)
    ui.showMaximized()
    app.exec()
