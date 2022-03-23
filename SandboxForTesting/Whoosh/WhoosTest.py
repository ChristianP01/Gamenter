'''
Reference: https://whoosh.readthedocs.io/en/latest/quickstart.html
'''

DEBUG = True
PATH_TO_DOCUMENT = "../../Documenti"

def dprint(s):
    '''
    Debug print function
    '''
    if DEBUG:
        print(s)

def readDocument(path):
    '''
    Funzione che legge il documento passato come path.
    Il documento deve essere correttamente formattato.
    Returna una tupla del tipo (titolo, descrizione)
    '''
    try:
        with open(path, "r") as file:
            content = file.read()
            title : str = content[content.find("Titolo:") + len("Titolo: ") : content.find("\n", content.find("Titolo:"))]
            description : str = content[content.find("Descrizione:") + len("Descrizione: ") : content.find("\n", content.find("Descrizione:"))]
            return (title, description)
    except:
        raise FileNotFoundError


if __name__ == "__main__":
    from whoosh.fields import Schema, TEXT
    #Sto copiando dal tutorial, ma direi di star creando appunto uno schema che ha
    #un titolo in formato testuale e un contenuto in formato testuale
    schema = Schema(title=TEXT(stored=True), content=TEXT)

    #Leggo dalla guida che si possono creare i propri tipi di fields

    #Una volta che si ha lo schema si può creare l'indice

    import os.path
    from whoosh.index import create_in

    if not os.path.exists("index"):
        os.mkdir("index")
    ix = create_in("index", schema)

    #Una volta creato l'indice è possibile aprirlo

    from whoosh.index import open_dir

    ix = open_dir("index")


    writer = ix.writer()


    from os import listdir

    for f in listdir(PATH_TO_DOCUMENT):
        document = readDocument(PATH_TO_DOCUMENT+"/"+f)
        #Writer accetta stringhe in unicode, ma ho letto che tutte le stringhe in python3 sono in unicode quindi polleg
        writer.add_document(title=document[0], content=document[1])
    
    #Salva i documenti nell'indice
    writer.commit()

    #Creo oggetto searcher

    from whoosh.query import *
    with ix.searcher() as searcher:
        par1 = input("Inserisci primo parametro: ")
        par2 = input("Inserisci secondo parametro: ")
        #Questa query matcha i documenti che contengono par1 e par2
        query = And([Term("content", par1), Term("content", par2)])

        results = searcher.search(query)
        print(f"Totale risultati: {len(results)}")
        print("Top 10 risultati")
        for r in results:
            print(r)