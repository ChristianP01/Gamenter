from distutils import text_file
import bs4, requests, webbrowser
from matplotlib.pyplot import title
import functools
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
from pprint import pprint
import urllib.parse
from methods import connectTo, getMark

#PATH_TO_DIRECTORY = "../../DocumentiTest" #Teddy
#I file sono 18828 (contati con wc, non sono calcolati dinamicamente, magari TODO di aggiungere il calcolo dinamico)
os.system("clear")
PATH_TO_DIRECTORY = "/home/christian/Università/Gestione dell'informazione/Progetto/Documenti/DocumentiTest/" #Preti
FILE_NUMBER = 18828
directory = PATH_TO_DIRECTORY
c = 0

for filename in os.listdir(directory):
    c += 1
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        file_game = open(f,'r')
        game_name = file_game.readline()
        text_from_file = file_game.read()
        if (text_from_file.find("Valutazione:") < 0):
            print(f"\n\n\n############\n#{c}/{FILE_NUMBER}#\n############")
            title = game_name[8:-1]
            print(f"Searching for {title}")
            file_game.close()
            try:
                file_game = open(f,'a')
                mark = getMark(title)   #Chiama getMark() in methods.py 
                print(title+": "+str(mark))
                file_game.write("\n\nValutazione: "+str(mark)+"\n")
            except:
                print(f"{title}: Gioco non trovato")
                file_game.write("\n\nValutazione: Non presente\n")