# Gamenter
Gamenter è un thematic search engine per la ricerca granulare di videogiochi. Il suo indice è formato all'incirca da **18000** documenti, ed ogni documento è una fusione di informazioni da 2 fonti ben distinte:
  - Titolo, Descrizione, Anno pubblicazione e Genere sono presi da [Wikipedia](https://en.wikipedia.org)
  - Valutazione, che è presa da [Metacritic](https://www.metacritic.com/)

Ogni documento è stato generato automaticamente attraverso l'utilizzo di **web scraper** costruiti ad hoc, ed ottimizati su misura al sito da cui dovevano prendere i dati (si veda la sezione [**web scraper**](#web-scraper))

Inoltre l'utente può rendere più fine la sua ricerca applicando dei filtri sull'anno, sul genere e sulla valutazione (si veda la sezione [**filters**](#filters))
## Web scraper
I web scrapers utilizzati per questo progetto sono stati costruiti appositamente per **wikipedia** e **metacritic**. Per quanto riguarda wikipedia, **wikimedia** fornisce una serie di web API estremamente comode e mirate per ottenere dettagli precisi degli articoli presenti su wikipedia. Per cui è stato possibile ottenere una lista di tutti i videogiochi pubblicati da un certo anno ad un certo anno, e con tale lista è stato possibile ottenere informazioni dettagliate per ognuno di essi.

Per ottenere le valutazioni da metacritic, invece, il procedimento è stato un po' più complesso.
Abbiamo progettato gli scrapers per lavorare in modo sequenziale ed asincrono, per cui una volta ottenuto il database di file con i videogiochi presenti da wikipedia (in cui all'interno contengono nome, descrizione, anno e genere) è stato possibile per ognuno di essi appendere a fine file la valutazione. Per fare questo procedimento lo script in python apriva il file, leggeva il titolo, lo cercava su metacritic e, cercando "a mano" all'interno dell'html, riusciva a ricavare la valutazione (se possibile) e la appendeva al file.

Entrambi questi scraper non possono lavorare "a regime" perché siamo stati spesso bloccati dai corrispettivi siti per averli innondati di richieste, per cui ognuno di essi contiene un timeout T ogni X richieste, con X e T ricavati empiricamente a seguito di vari test. 

Per eseguire lo scraping totale da wikipedia e da metacritic occorrono circa **24 ore**
## Installazione
Per utilizzare Gamenter è sufficiente clonare questa repository e seguire le istruzione successive
### Requisiti
Per utilizzare Gamenter è sufficiente avere una versione di python superiore alla 3.8, ed il sistema di gestione dei pacchetti di python **pip**.
È presente sia una versone GUI che una versione CLI. Indipendentemente dalla versione che si desidera utilizzare, è necessario utilizzare l'ambiente virtuale fornito (si veda [**Ambiente virtuale**](#ambiente-virtuale)).
Per avviare il programma, recarsi nella cartella ./release ed eseguire rispettivamente
```bash
python gamenterCLI.py
python gamenterGUI.py
```

### Ambiente virtuale
Gamenter è stato scritto utilizzando un ambiente virtuale python3-venv ([documentazione](https://docs.python.org/3/library/venv.html)), e sui sistemi UNIX è sufficiente (se si ha la libreria **python3-venv** installata) recarsi nella root del progetto ed eseguire
```bash
source activate.sh

# OPPURE

source SearchEngine/bin/activate
```

Nel caso non si disponga di python3-venv, oppure si vuole usare un altro ambiente virtuale, è sufficiente installare manualmente le dipendenze con il comando (TODO METTI IL FILE REQUIREMENT)
```bash
pip install -r requirements.txt
```
recandosi nella root del progetto.

Le dipendenze richieste sono:
```
PyQt6==6.2.3
PyQt6-Qt6==6.2.4
PyQt6-sip==13.2.1
Whoosh==2.7.4
```
# filters
Il motore di ricerca Gamenter supporta un proprio query language molto semplice ma molto potente. È possibile infatti filtrare i risultati per anno di pubblicazione, per genere e per valutazione. È inoltre possibile specificare se fare la ricerca soltanto sui titoli dei videogiochi, sulla descrizione, oppure su entrambi.

## implementazione
Il query language è implementato attraverso un dizionario python, che al suo interno contiene vari valori
```python
f = {
    "title": True,
    "content": True,
    "year": [],
    "mark": [],
    "genre": []
}
```
**title** e **content** sono due booleani, di default impostati a True. Questi flag specificano a whoosh se effettuare la ricerca sul titolo, sulla descrizione o su entrambi. **NON** è possibile settarli entrambi a False.
**Year** e **Mark** sono due liste utilizzate per il filtro sul genere e sull'anno. Per applicare un filtro, è sufficiente appendere ad una di esse un'altra lista nel formato \["OPERATION", "NUMBER"\]. **OPERATION** è l'operazione da eseguire (tra > < >= <= =), mentre **NUMBER** è la valutazione o l'anno con cui opeare. Per esempio, se nella lista year appendo \[>, 2000\] vuol dire che sto cercando i giochi usciti dopo l'anno 2000.
è possibile appendere un numero infinito di filtri, il programma li applicherà tutti, anche se alcuni filtri potrebbero escluderne altri
```python
#Esempio per year

year = [[">", "2000"], ["<", "1990"]] #-> ovviamente l'intersezione tra questi due vincoli è un insieme vuoto, quindi il motore non darà risultati

year = [[">", "1990"], [">", "2000"]] #-> ovviamente il secondo filtro è più stringente, quindi i risultati saranno dati dal filtro più stringente
```
**Genre** invece è una semplice lista che contiene, per ogni elemento, il genere su cui filtrare
```python
#esempio

genre = ["Action", "Rpg"]
```

