'''
Reference: https://whoosh.readthedocs.io/en/latest/quickstart.html
'''
from whoosh.fields import Schema, TEXT
from whoosh.query import *
from whoosh.index import open_dir
from os import listdir

DEBUG = True
PATH_TO_DOCUMENT = "../../Documenti"

def searchQuery2(user_query):
    print(f"Stai cercando la query {user_query}")

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
    pass

def openIndex():
    #Sto copiando dal tutorial, ma direi di star creando appunto uno schema che ha
    #un titolo in formato testuale e un contenuto in formato testuale
    schema = Schema(title=TEXT(stored=True), content=TEXT)

    #Leggo dalla guida che si possono creare i propri tipi di fields

    #Una volta che si ha lo schema si può creare l'indice

    import os.path
    from whoosh.index import create_in
    import whoosh.index as index

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
    else:
        ix = index.open_dir("index")
    return ix



def searchQueryCLI(user_query):
    ix = openIndex()

    searcher = ix.searcher()
    while True:
        #Provo a fare una versione che prenda un numero indefinito di parametri
        word_list = user_query.split(" ")  
        L = [] 
        for word in word_list:
            L.append(Term("content", word))
        query = And(L)
        results = searcher.search(query)
        user_query = yield results


def searchQuery(gui, user_query):
    ix = openIndex()
    #Creo oggetto searcher
    with ix.searcher() as searcher:
        #Provo a fare una versione che prenda un numero indefinito di parametri
        word_list = user_query.split(" ")
        print(f"Lista parole: {word_list}")
        
        L = []
        for word in word_list:
            L.append(Term("content", word))
        query = And("content", L)

        results = searcher.search(query)
        

        gui.resultsText.setPlainText("") #Inizializzo il valore iniziale del box risultati

        for r in results: #Appende i vari risultati singoli all'interno della lista
            gui.resultsText.setPlainText(str(gui.resultsText.toPlainText())+str(r['title'])+"\n")
