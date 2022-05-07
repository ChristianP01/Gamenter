'''
Reference: https://whoosh.readthedocs.io/en/latest/quickstart.html
'''
from pprint import pprint
from whoosh.fields import Schema, TEXT
from whoosh.query import *
from whoosh.index import open_dir
from whoosh.lang.porter import stem

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


def readDocument2(path):
    '''
    Funzione che legge il documento passato come path.
    Il documento deve essere correttamente formattato.
    Returna una tupla del tipo (titolo, descrizione, valutazione, genere)
    '''


    try:
        with open(path, "r") as file:
            content = file.read()
            title : str = content[content.find("Titolo:") + len("Titolo: ") : content.find("\n", content.find("Titolo:"))]
            description : str = content[content.find("Descrizione:") + len("Descrizione: ") : content.find("\n", content.find("Descrizione:"))]
            mark : str = content[content.find("Valutazione:") + len("Valutazione: ") : content.find("\n", content.find("Valutazione:"))]
            genres : str = content[content.find("Genere:") + len("Genere: ") : content.find("\n", content.find("Genere:"))]
            
 
            """
            title = stem(title)
            description = stem(description)
            mark = stem(mark)
            genres = stem(genres)
            """


            return (title, description, mark, genres)
    except:
        raise FileNotFoundError


if __name__ == "__main__":
    pass

def openIndex():
    #Sto copiando dal tutorial, ma direi di star creando appunto uno schema che ha
    #un titolo in formato testuale e un contenuto in formato testuale
    from whoosh import analysis
    ana = analysis.StemmingAnalyzer(stoplist=None, minsize=0, maxsize=0)
    schema = Schema(title=TEXT(stored=True, analyzer=ana), content=TEXT(stored=True, analyzer=ana),
        mark=TEXT(stored=True, analyzer=ana), genres=TEXT(stored=True, analyzer=ana) )

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
        genres_list = []

        from os import listdir
        
        

        for f in listdir(PATH_TO_DOCUMENT):
            document = readDocument2(PATH_TO_DOCUMENT+"/"+f)

            #Writer accetta stringhe in unicode, ma ho letto che tutte le stringhe in python3 sono in unicode quindi polleg
            writer.add_document(title=document[0], content=document[1], mark = document[2], genres = document[3], )

            if document[3] not in genres_list:
                genres_list.append(document[3])


        print(f"Tutti i generi trovati sono:")
        pprint(genres_list)
        
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

        Lcontent = []
        Ltitle = [] 
        for word in word_list:
            Lcontent.append(Term("content", word))
            Ltitle.append(Term("title", word))
        #query = And(Lcontent) | Or(Ltitle)

        query = And(Ltitle)
        #query = And(Lcontent)

        #query = And(Lcontent) | Or(Ltitle)

        results = searcher.search(query, limit=10)
        #print(results)
        user_query = yield results

def searchQuery(gui, user_query):

    ix = openIndex()
    #Creo oggetto searcher
    with ix.searcher() as searcher:
        word_list = user_query.split(" ")
        print(f"Lista parole: {word_list}")
        
        Lcontent = []
        Ltitle = []
        Lscores = {}
        for word in word_list:
            Lcontent.append(Term("content", word))
            Ltitle.append(Term("title", word))

        query = And(Lcontent) | Or(Ltitle) 
        results = searcher.search(query)
        gui.resultsText.setPlainText("") #Inizializzo il valore iniziale del box risultati

        for r in results: #Appende i vari risultati singoli all'interno della lista
            gui.resultsText.setPlainText(str(gui.resultsText.toPlainText())+str(r['title'])+" "+str(r.score)+"\n")
            Lscores[r['title']]= r.score
            

def proximitySearch(word_list, ix):
    from whoosh import query
    from whoosh.query import spans

    L = []
    for word in word_list:
        L.append(Term("title", word))

    q = spans.SpanNear2(L, slop=5, ordered=False)

    
    results = ix.searcher().search(q)
        
    return results


def searchByMark(word_list, ix, mark_min=None, mark_max=None):

    marked_games = []

    if mark_min is None:
        mark_min = 0

    if mark_max is None:
        mark_max = 100

    results_games = proximitySearch(word_list, ix)
    print("All games: ")
    for r in results_games:
        print(f"{r['title']} with value of {r['mark']}")

    for r in results_games:
        try:
            if float(r['mark']) in range(mark_min, mark_max):
                marked_games.append(r)
        except:
            continue

    print("Marked games: ")
    for r in marked_games:
        print(f"{r['title']} with value of {r['mark']}")


x = input("Inserisci query: ")
word_list = x.split(" ")
ix = openIndex()

searchByMark(word_list, ix, 20, 80)