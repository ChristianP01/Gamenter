from socket import AI_PASSIVE
from unittest import result
from searcher import searchQueryCLI as query
import json

qgen = query(("",""))
qgen.send(None)

def parse_filter(f, input):
    l_input = input.split(" ")
    if l_input[0] == "year":
        l_command = [l_input[1], l_input[2]]
        f["year"].append(l_command)
    if l_input[0] == "mark":
        l_command = [l_input[1], l_input[2]]
        f["mark"].append(l_command)
    if l_input[0] == "genre":
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
    #return f

while True:
    q = input("Inserisci ricerca: ")
    f = {
        "title": True,
        "content": True,
        "year": [],
        "mark": [],
        "genre": []
    }
    print("Inserire i filtri, per interrompere inserire una stringa vuota")
    while True:
        i = input("Inserisci filtro: ")
        if i == "":
            break
        parse_filter(f,i)

    #f = json.loads(f)
    print("\n\n\n\n\n\n")

    result = qgen.send((q,f))
    #print(result)
    '''
    print("RICERCA PER TITOLO")
    for r in result[0]:
        print(f"{r['title']} con rank {r.score}")

    print("RICERCA PER DESCRIZIONE")
    for r in result[1]:
        print(f"{r['title']} con rank {r.score}")
    '''

    print("RICERCA JOINATA TITLE E DESCRIPTION")

    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    for res in sorted_result[:10]:
        print(f"{res[0]} con valutazione {res[1]}")
