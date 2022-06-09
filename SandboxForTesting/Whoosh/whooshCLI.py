import time
from unittest import result
from searcher import searchQueryCLI as query
import searcher
import json

qgen = query(("",""))
qgen.send(None)
def stampa_logo():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("                                    WELCOME TO                                  ")
    print("\n")
    print("################################################################################")
    print("# @@@@@@   @@@@@@   @@    @@   @@@@@@    @@    @    @@@@@@@    @@@@@@   @@@@@  #")
    print("# @        @    @   @ @  @ @   @         @ @   @       @       @        @    @ #")
    print("# @  @@@   @@@@@@   @  @@  @   @@@@      @  @  @       @       @@@@@    @@@@@  #")
    print("# @    @   @    @   @  @@  @   @         @   @ @       @       @        @   @  #")
    print("# @@@@@@   @    @   @  @@  @   @@@@@@    @    @@       @       @@@@@    @    @ #")
    print("################################################################################")
    print("\n")

def come_funziona():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Gamenter è un semplice motore di ricerca tematico focalizzato sulla ricerca di videogiochi.")
    print("È possibile effettuare ricerche attraverso keyword, per poi selezionare i risultati più interessanti attraverso un filtro.")
    print("Il database di gamenter contiene all'incirca 18000 documenti, basati su altrettante pagine di wikipedia. Sono stati indicizzati utilizzando Whoosh, una libreria di Python.")
    print("Oltre a wikipedia, Gamenter ha sfruttato il sistema di valutazioni di Metacritic per fornire informazioni in più sui titoli indicizzati.")
    print("\n")
    print("Utilizzare Gamenter è molto semplice, ti basterà inserire le keyword che vuoi cercare e poi applicare eventualmente dei filtri, i risultati appariranno a schermo con tutte le informazioni necessarie.")
    print("\n\n")

def come_filtri():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Gamenter permette una ricerca più accurata tramite un sistema di filtri.")
    print("I filtri sono implementati tramite uno specifico linguaggio, creato appositamente per essere semplice.")
    print("Per esempio, se voglio cercare i giochi usciti dopo il 2010, mi basterà inserire quando richiesto 'year > 2010'.")
    print("E se volessi i giochi usciti tra il 2010 ed il 2015? semplicemente basterà applicare due filtri, 'year > 2010' ed 'year <= 2015'")
    print("La versatilità di questo sistema permette di concatenare un numero infinito di filtri, per ottenere un risultato più preciso possibile.")
    print("\n\n")

def come_ricerca():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Gamenter è molto semplice e preciso.")
    print("Le keyword inserite vengono cercate nel nostro indice prima soltanto sui titoli dei videogiochi, e poi sulla descrizione, creando due set distinti di risultati.")
    print("Una volta ottenuti questi 2 set, Gamenter li combina, dando un peso maggiore ai giochi risultanti dalla ricerca sul titolo (precisamente il peso è maggiorato del 50%).")
    print("suquesto set di risultati, in base alle esigenze dell'utente, si può decidere di applicare un filtro per rimuovere qualche gioco non richiesto.")
    print("Nei filtri è inoltre possibile rimuovere del tutto la ricerca sul titolo, oppure la ricerca sulla descrizione (di default sono entrambe abilitate, e non possono essere entrambe disabilitate contemporaneamente)")
    print("\n\n")

stampa_logo()




while True:
    print("Ciao utente, come posso esserti utile?")
    print("1) Come funziona?")
    print("2) Come utilizzo i filtri?")
    print("3) Come funziona la ricerca?")
    print("4) Portami dentro Gamenter!")
    i = input("Cosa vuoi fare? ")
    if i == "1":
        come_funziona()
    elif i == "2":
        come_filtri()
    elif i == "3":
        come_ricerca()
    elif i == "4":
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        break
    else:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nInserisci un opzione valida! \n\n")



while True:
    f = {
        "title": True,
        "content": True,
        "year": [],
        "mark": [],
        "genre": []
    }
    q = input("Inserisci le keyword da ricercare: ")
    
    print("Inserire i filtri, per proseguire premere INVIO")
    print("Inserire un filtro alla volta tra cui:")
    print("year [operation] [year]")
    print("mark [operation] [year]")
    print("genre [genre]")
    print("title [True/False]")
    print("content [True/False]\n")
    while True:
        i = input("Inserisci filtro: ")
        if i == "":
            break
        searcher.parse_filter(f,i)

    print("\n")
    t0 = time.time()
    result = qgen.send((q,f))

    print("Risultati:")
    try:
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for res in sorted_result:
            #score anno, genere, voto
            print(f"{res[0]}: uscito nel {res[1][1]} con voto {res[1][3]}. Genere: {res[1][2]} e scoring {round(res[1][0], 2)}\n")
    except:
        print("Nessun risultato per la query fornita")
    print("#######################################################")
    print(f"# Risultati forniti in {round(time.time() - t0, 19)} secondi! #")
    print("#######################################################")
    input("\nPremi invio per proseguire...")
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
