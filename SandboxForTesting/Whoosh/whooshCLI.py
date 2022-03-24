from unittest import result
from main import searchQueryCLI as query


qgen = query("")
qgen.send(None)
while True:
    q = input("Inserisci ricerca: ")


    result = qgen.send(q)
    print(result)
    for r in result:
        print(r)