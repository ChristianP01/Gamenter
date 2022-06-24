from PyQt6 import uic
from PyQt6 import QtCore, QtGui, QtWidgets
from whoosh.query import *
from whoosh.fields import Schema, TEXT
from searcher import searchQueryCLI as query
import urllib
import sys
#from PyQt5.QtWidgets import QTextBrowser
#from PyQt5.QtGui import QTextCursor
import os.path
from whoosh.index import create_in
import searcher

baseUIClass, baseUIWidget = uic.loadUiType("gui.ui")

class Logic(baseUIWidget, baseUIClass):
    qgen = query(("",""))
    qgen.send(None)

    def __init__(self, parent=None):
        super(Logic, self).__init__(parent)
        self.setupUi(self)
        self.genreList.setPlaceholderText(" ")
        self.searchButton.setIcon(QtGui.QIcon('images/search.jpg'))
        f = open("generi_meglio2.txt", "r")
        genres = f.readlines()
        f.close()

        self.textBrowser.setOpenExternalLinks(True)

        for genre in genres:
            self.genreList.addItem(genre)

        self.querySyntax.setPlaceholderText("Esempio: \n\n"\
            "year > 2010 \n"
            "year < 2020 \n"
            "mark > 80 \n"
            "mark <=85 \n"
            "content True/False (Default, True) \n"
            "title True/False (Default, True) \n"
        )

        #self.searchButton.clicked.connect(lambda: searcher.searchQuery(self, str(self.userQuery.toPlainText())) )
        self.searchButton.clicked.connect(lambda: self.filtered_query(str(self.userQuery.toPlainText())))

    def filtered_query(self, q):
        f = {
        "title": True,
        "content": True,
        "year": [],
        "mark": [],
        "genre": []
        }
        Lscores = {}
        filters = self.querySyntax.toPlainText()
        filters = filters.split("\n")
        for i in filters:
            searcher.parse_filter(f,i)
        
        results = self.qgen.send((q,f))
        sorted_result = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        self.textBrowser.setPlainText("") #Inizializzo il valore iniziale del box risultati
        for r in sorted_result: #Appende i vari risultati singoli all'interno della lista
            # gui.textBrowser.setPlainText(str(gui.textBrowser.toPlainText())+str(r['title'])+" "+str(r.score)+"\n")
            
            self.textBrowser.append(f"\n<a href=https://en.wikipedia.org/wiki/{urllib.parse.quote(r[0])}> {str(r[0])} </a>" + f", con score {round(float(r[1][0]), 2)}, con valutazione {str(r[1][3])}, uscito nel {str(r[1][1])} e avente genere {str(r[1][2])}")
            Lscores[r[0]]= r[1][0]

        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Logic(None)
    ui.showMaximized()
    app.exec()
