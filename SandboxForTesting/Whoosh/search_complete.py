# File su cui far partire tutti i tipi di ricerca implementati
import os
from main import searchByMark, proximitySearch, openIndex
ix = openIndex()

while(True):
    os.system("clear")
    choice = input("\n\n1. Ricerca su titolo. \n2. Ricerca su titolo+anno. \n3. Ricerca su titolo+voto\nScelta: ")

    if int(choice) == 3:
        x = input("Inserisci query: ")
        word_list = x.split(" ")
        word_list = [w.lower() for w in word_list]

        mark_min = input("Inserisci voto minimo: ")
        mark_max = input("Inserisci voto massimo: ")

        if mark_min.isnumeric() == False:
            mark_min = None
        else:
            mark_min = int(mark_min)

        if mark_max.isnumeric() == False:
            mark_max = None
        else:
            mark_max = int(mark_max)

        searchByMark(word_list, ix, mark_min, mark_max)

        x = input("\n\nPremi un tasto per continuare...\nOppure CTRL+C per terminare.")