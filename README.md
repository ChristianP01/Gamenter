# Gamenter
Gamenter è un thematic search engine per la ricerca granulare di videogiochi. Il suo indice è formato all'incirca da **18000** documenti, ed ogni documento è una fusione di informazioni da 2 fonti ben distinte:
  - Titolo, Descrizione, Anno pubblicazione e Genere sono presi da [Wikipedia](https://en.wikipedia.org)
  - Valutazione, che è presa da [Metacritic](https://www.metacritic.com/)

Ogni documento è stato generato automaticamente attraverso l'utilizzo di **web scraper** costruiti ad hoc, ed ottimizati su misura al sito da cui dovevano prendere i dati (si veda la sezione **web scraper** TODO METTI LINK)

Inoltre l'utente può rendere più fine la sua ricerca applicando dei filtri sull'anno, sul genere e sulla valutazione (si veda la sezione **filters** TODO METTI LINK)
## Web scraper

## Installazione
### Requisiti
Per utilizzare Gamenter è sufficiente avere una versione di python superiore alla 3.8, ed il sistema di gestione dei pacchetti di python **pip**.
È presente sia una versone GUI che una versione CLI. Indipendentemente dalla versione che si desidera utilizzare, è necessario utilizzare l'ambiente virtuale fornito (si veda **Ambiente virtuale** TODO METTI LINK).
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
