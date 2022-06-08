from unittest import result
from searcher import searchQueryCLI as query
import searcher
import json

qgen = query(("",""))
qgen.send(None)








while True:
    q = input("Inserisci ricerca: ")
    f = {
        "title": True,
        "content": True,
        "year": [],
        "mark": [],
        "genre": []
    }
    print("\n\n")
    print("Inserire i filtri, per interrompere inserire una stringa vuota")
    print("Inserire un filtro alla volta, i possibili filtri sono:")
    print("year [operation] [year]")
    print("mark [operation] [year]")
    print("genre [genre]")
    print("title [True/False]")
    print("content [True/False]")
    print("\n\n")
    while True:
        i = input("Inserisci filtro: ")
        if i == "":
            break
        searcher.parse_filter(f,i)

    print("\n\n")
    result = qgen.send((q,f))

    print("Risultati:")
    try:
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for res in sorted_result[:10]:
            #score anno, genere, voto
            print(f"{res[0]}: uscito nel {res[1][1]} con voto {res[1][3]}. Genere: {res[1][2]} e scoring {res[1][0]}\n\n")
    except:
        print("Nessun risultato per la query fornita")
