Per compilare il file Benchmarks.pdf, assicurarsi di avere latex installato attraverso il comando:

```
pdflatex --version
```

Verificato ciò, installare i seguenti package:
   - Pythontex
   - FvExtra
   
Una volta installati, entrare nella root folder e usare i comandi:



Questo creerà il file .pdf, ma non avrà compilati gli snippet di codice, essi si troveranno nel file Benchmarks.pytxcode
```
pdflatex Benchmarks.tex
```



Questo eseguirà gli snippet di codice.
```
pythontex.py Benchmarks.tex
```



Compilare quindi tutto il file .tex
```
pdflatex Benchmarks.tex
```




Il file PDF sarà ora correttamente creato!
