from socket import AI_PASSIVE
from unittest import result
from searcher import searchQueryCLI as query
import json

qgen = query(("",""))
qgen.send(None)


def check_filter(f):
    if f[0] not in ["year", "mark", "genre", "title", "content"]:
        return False
    if f[0] in ["year", "mark"]:
        if f[1] not in ["<", ">", "=", ">=" , "<="]:
            return False
        try:
            int(f[2])
        except ValueError:
            return False
    if f[0] in ["title", "content"]:
        if f[1] not in ["True", "False"]:
            return False
    if f[0] == "genre":
        if len(f) == 1:
            return False
            
    return True 

def parse_filter(f, input):
    l_input = input.split(" ")
    if check_filter(l_input):
        if l_input[0] == "year":
            l_command = [l_input[1], l_input[2]]
            f["year"].append(l_command)
        if l_input[0] == "mark":
            l_command = [l_input[1], l_input[2]]
            f["mark"].append(l_command)
        if l_input[0] == "genre":
            #NON FUNZIONA SE IL GENERE E' SEPARATO DA DEGLI SPAZI
            for genere in l_input[1:]:
                f["genre"].append(genere)
        if l_input[0] == "title":
            if l_input[1] == "True":
                f["title"] = True
            else:
                f["title"] = False
        if l_input[0] == "content":
            if l_input[1] == "True":
                f["content"] = True
            else:
                f["content"] = False
    else:
        print("Errore nel filtro occhio")

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
        parse_filter(f,i)

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
