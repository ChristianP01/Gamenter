from numpy import empty
import requests
import os.path
import sys
import time
import urllib.parse
import re
PATH_FILE = "./wikipedia_url.txt"
PATH_DOCUMENT = "./Documenti/"


def TrovaUltimaLinea(indici):
    '''
    Funzione che prende in input il dict indici e restituisce in output il pageid dell'ultima pagina scritta dentro wikipedia_url.txt
    '''
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

def ScaricamentoIndici(annoinizio=1950, annofine=2022):
    '''
    Funzione che prende in ingresso il range di anni in cui scaricare la lista di articoli di videogiochi usciti in tali anni.
    Restituisce il dict indici che contiene tutti i pageid, i titoli e gli anni di uscita
    '''

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
    return indici


def ScriviSuFile(resume=False):
    '''
    Funzione che prende, partendo dai pageid contenuti in indici, tutti gli url delle pagine legate a tali indici.
    Prende in ingresso un flag che se settato a true, cerca di riprendere il download da dove l'aveva lasciato, consultando il file wikipedia_url.txt
    '''
    indici = ScaricamentoIndici()
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
if (len(sys.argv) > 1):
    if sys.argv[1] == "--force":
        print("Eseguo lo scraping con l'opzione --force")
        file = open(PATH_FILE, 'w')
        file.write("")
        file.close()
        indici = ScriviSuFile()
    if sys.argv[1] == "--resume":
        print("Eseguo la ricerca da dove mi ero fermato...")
        ScriviSuFile(True)
        

#Controllo di non aver già scaricato la lista di url
if (not os.path.exists(PATH_FILE)):
    indici = ScriviSuFile()
else:
    print("Elenco degli url già scaricato. Se si vuole aggiornare, lanciare il programma con l'opzione --force. NB lo scaricamento degli url è un'operazione che richiede molto tempo")

s = input("Procedere con lo scaricamento delle pagine? Questa operazione richiederà molto tempo [y/N]")
if s == None or s.lower() == "n":
    exit()

if len(indici) == 0:
    indici = ScaricamentoIndici()


#Pattern utilizzato per trovare il page id dal file (formato file PAGEID###URL). Il page id è sempre numerico
pattern_id = "^[0-9]+"

'''
Pezzo di codice che legge gli url dal file, estrae l'id e il nome della pagina e scarica la descrizione breve di tale pagine, associandola
tramite il pageid al dict indici per trovare l'anno ed il nome (human readable) del videogioco in questione.
Salva tutte le pagine in file di testo separati.
'''
with open(PATH_FILE) as fp:
    line = fp.readline()
    c=0
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
        page_name = file_url[file_url.find("###")+31:]
        nome_leggibile = ""
        anno_uscita = ""

        for k,v in indici.items():
            if str(k) == str(file_pageid):
                nome_leggibile = v[0]
                anno_uscita = v[1]
                break
        if (nome_leggibile == ""):
            print(f"Match non trovato ({file_pageid}, {page_name})")
            line = fp.readline()
            continue

        response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': page_name,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }).json()
        page = next(iter(response['query']['pages'].values()))
        estratto = page['extract']


        try:
            file = open(f"{PATH_DOCUMENT}{page_name}", "w")
            contenuto_file = f"Titolo: {nome_leggibile}\n\nAnno: {anno_uscita}\n\nDescrizione: {estratto}"
            file.write(contenuto_file)
            file.close()
        except:
            print (f"Scrittura non riuscita di {nome_leggibile}")
        
        c+=1
        if (c > 100):
            c=0
            print("Scaricate 100 descrizioni, entro in pausa per 65 secondi")
            time.sleep(65)
        line = fp.readline()
