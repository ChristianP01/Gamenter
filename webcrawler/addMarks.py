from matplotlib.pyplot import title
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from pprint import pprint
#Libreria definita da noi
from methods import connectTo, getMark


os.system("clear")

#I file sono 18828 (contati con wc, non sono calcolati dinamicamente, magari TODO di aggiungere il calcolo dinamico)
FILE_NUMBER = 18828

#Switchare in base a chi esegue lo script (o comunque inserire dentro PATH_TO_DIRECTORY il path corretto)
PATH_TO_DIRECTORY = "../../DocumentiTest" #Teddy
#PATH_TO_DIRECTORY = "/home/christian/Università/Gestione dell'informazione/Progetto/Documenti/DocumentiTest/" #Preti

directory = PATH_TO_DIRECTORY

#Contatore usato puramente a livello di feedback durante l'inserimento delle valutazioni
c = 0

#Semplicemente lo script scorre tutti i file dentro il PATH inserito, prende il titolo del videgioco, lo cerca su metacritics e fa selezionare
#all'utente la valutazione più corretta. Una volta selezionata l'appende a fondo file e passa al prossimo
for filename in os.listdir(directory):
    c += 1
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        #Apertura del file in lettura per controllare che non ci sia già la valutazione e per recuperare il titolo
        file_game = open(f,'r')
        game_name = file_game.readline()
        text_from_file = file_game.read()
        if (text_from_file.find("Valutazione:") < 0):
            print(f"\n\n\n############\n#{c}/{FILE_NUMBER}#\n############")
            title = game_name[8:-1]
            print(f"Searching for {title}")

            #Chiusura del file in lettura e apertura del file in "append"
            file_game.close()
            try:
                file_game = open(f,'a')
                mark = getMark(title)   #Chiama getMark() in methods.py 
                print(title+": "+str(mark))
                file_game.write("\n\nValutazione: "+str(mark)+"\n")
            except:
                print(f"{title}: Gioco non trovato")
                file_game.write("\n\nValutazione: Non presente\n")
        else:
            #Se la stringa "Valutazione:" è già presente nel file
            continue
