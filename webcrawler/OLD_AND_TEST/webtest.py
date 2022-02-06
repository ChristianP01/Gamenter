import requests
import os.path
import sys
import time
PATH_FILE = "./wikipedia_url.txt"

#Funzione che prende la lista di tutti i videogiochi presenti su wikipedia
def ScriviSuFile(annoinizio=1950,annofine=2022):
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
   


indici = ScriviSuFile(1930,2022)


