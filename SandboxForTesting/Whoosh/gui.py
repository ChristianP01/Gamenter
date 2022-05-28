from PyQt6 import uic
from PyQt6 import QtCore, QtGui, QtWidgets
from whoosh.query import *
from whoosh.fields import Schema, TEXT
import sys
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QTextCursor
import os.path
from whoosh.index import create_in
import searcher

baseUIClass, baseUIWidget = uic.loadUiType("gui.ui")

class Logic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.genreList.setPlaceholderText(" ")
        f = open("generi_meglio2.txt", "r")
        genres = f.readlines()
        f.close()

        self.textBrowser.setOpenExternalLinks(True)
        # self.textBrowser.setStyleSheet('font-size: 30px;')
        # self.textBrowser.append('<a href=https://www.google.com>Google</a>')

        for genre in genres:
            self.genreList.addItem(genre)
        

        self.searchButton.clicked.connect(lambda: searcher.searchQuery(self, str(self.userQuery.toPlainText())) )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Logic(None)
    ui.showMaximized()
    app.exec()
