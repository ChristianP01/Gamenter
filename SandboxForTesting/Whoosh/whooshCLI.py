from unittest import result
from main import searchQueryCLI as query


qgen = query("")
qgen.send(None)
while True:
    q = input("Inserisci ricerca: ")

    print("\n\n\n\n\n\n")
    result = qgen.send(q)
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
