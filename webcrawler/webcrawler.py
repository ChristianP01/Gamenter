import requests
import os.path
import sys
import time
import urllib.parse
import re
PATH_FILE = "./wikipedia_url.txt"

#TODO check integrità del file wikipedia_url.txt dove scarichi gli indici e guardi che siano scritti tutti

def TrovaUltimaLinea(indici):
    with open(PATH_FILE) as f:
        for line in f:
            pass
        last_line = line
        pattern_id = "^[0-9]+"
        match = re.match(pattern_id, last_line)
        start = match.start()
        end = match.end()
        last_pageid = line[start:end]
        return last_pageid

#Funzione che prende la lista di tutti i videogiochi presenti su wikipedia
def ScriviSuFile(annoinizio=1950,annofine=2022,resume=False):
    #Dizionario che conterrà come chiave il pageid, come valore una lista formata da [titolo, anno]
    indici = {}
    for anno in range(annoinizio,annofine):
        url = f"https://en.wikipedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:{anno}_video_games&prop=categories&cllimit=max&gcmlimit=max&format=json"
        print(f"Scarico videogiochi anno {anno}")
        try:
            data = requests.get(url)
            dict_data = dict(data.json())
            for page in dict_data["query"]["pages"].values():
                indici[page["pageid"]] = [page["title"],anno]
        except:
            print(f"ERRORE: non ci sono videogiochi nell'anno {anno}")
            continue
    totale_pagine = len(indici.keys())
    print(totale_pagine)

    last_pageid = ""
    if resume:
        last_pageid = TrovaUltimaLinea(indici)
        print(f"Ultimo pageid trovato nel file: {last_pageid}")
        print("Sincronizzo gli indici...")


    #una volta scaricati gli id delle pagine, li salvo su file nel formato ID###URL
    print("Inizio scrittura su file")
    file = open(PATH_FILE, 'a')
    c = 0
    cont = 0
    fin = len(indici.keys())
    for pageid in indici.keys():
        if resume:
            cont += 1
            if str(pageid) == str(last_pageid):
                resume = False
            continue

        #scarico 100 pagine, successivamente aspetto 1 minuto e poi ne scarico altre 100 (per evitare di essere bloccato)
        if (c > 100):
            print("Raggiunti i 100 download, attendo 1 minuto (per non sovraccaricare wikipedia")
            c = 0
            time.sleep(60)
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=info&pageids={pageid}&inprop=url&format=json"
        print(f"Recupero link di {pageid}, numero {c}")
        data = requests.get(url)
        dict_data = dict(data.json())
        file.write(str(pageid) + "###" + dict_data["query"]["pages"][str(pageid)]["fullurl"]+"\n")
        print(f"File {cont} su {fin}")
        c+=1
    file.close()
    print("Finita scrittura su file")
    return indici



indici = {}
#Se lancio il programma con l'opzione --force, svuota il file (se esiste) con gli url e lo riscrive da capo
#Se lancio il programma con l'opzione --resume, continua il download da dove si era fermato
#TODO se lancio il programma con --check, controlla l'integrità del file ed eventualmente scarica gli url mancanti
if (len(sys.argv) > 1):
    if sys.argv[1] == "--force":
        print("Eseguo lo scraping con l'opzione --force")
        file = open(PATH_FILE, 'w')
        file.write("")
        file.close()
        indici = ScriviSuFile(1930,2022)
    if sys.argv[1] == "--resume":
        print("Eseguo la ricerca da dove mi ero fermato...")
        ScriviSuFile(1930,2022,True)
        

#Controllo di non aver già scaricato la lista di url
if (not os.path.exists(PATH_FILE)):
    indici = ScriviSuFile(1930,2022)
else:
    print("Elenco degli url già scaricato. Se si vuole aggiornare, lanciare il programma con l'opzione --force. NB lo scaricamento degli url è un'operazione che richiede molto tempo")

s = input("Procedere con lo scaricamento delle pagine? Questa operazione richiederà molto tempo [y/N]")
if s == None or s.lower() == "n":
    exit()



#Pattern utilizzato per trovare il page id dal file (formato file PAGEID###URL). Il page id è sempre numerico
pattern_id = "^[0-9]+"


with open(PATH_FILE) as fp:
    line = fp.readline()
    while line:
        match = re.match(pattern_id, line)
        start = match.start()
        end = match.end()
        #salvo il pageid
        file_pageid = line[start:end]
        #recupero l'url
        file_urlraw = line[end+3:-1]
        #converto i caratteri strani dell'url in utf-8
        file_url = urllib.parse.unquote(file_urlraw)

        #TODO dall'url recupera  il nome della pagina (dovrebbe essere facile)
        #TODO ADESSO FAI IL MATCH CON l'ID PRESO PRIMA, TI PRENDI IL NOME FATTO BENE E LO METTI COME TITOLO, L'ANNO, GETTI LA DESCRIZIONE (GUARDA TEST.PY) E COME 
        #NOME FILE METTI file_pagename
        line = fp.readline()
