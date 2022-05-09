from pprint import pprint
from whoosh.fields import Schema, TEXT
from whoosh.query import *
from whoosh.index import open_dir
from whoosh.lang.porter import stem
from indexer import *

def searchTitle(searcher, titleList):
    query = And(titleList)
    results = searcher.search(query, limit=10)
    return results

def searchDescription(searcher, descList):
    query = And(descList)
    results = searcher.search(query, limit=10)
    return results

def joinResults(*results):
    '''
    IL PRIMO PARAMETRO DEVE ESSERE LA LISTA DEI TITOLI
    '''

    final_results = {}

    titoli = results[0]
    for t in titoli:
        final_results[t['title']] = float(t.score) * 1.5

    for r in results[1:]:
        for doc in r:
            if doc['title'] not in final_results:
                final_results[doc['title']] = float(doc.score)
            else:
                final_results[doc['title']] += float(doc.score)
    return final_results

# Utilizza la proximity retrieval per effettuare query all'inverted index
def proximitySearch(word_list, ix):
    from whoosh import query
    from whoosh.query import spans
    
    L = []
    for word in word_list:
        L.append(Term("title", word))

    q = spans.SpanNear2(L, slop=5, ordered=False)

    
    results = ix.searcher().search(q)
        
    return results







def searchQueryCLI(user_query):
    ix = openIndex()

    searcher = ix.searcher()
    while True:
        #Provo a fare una versione che prenda un numero indefinito di parametri
        word_list = user_query.split(" ")
        word_list = [w.lower() for w in word_list]

        Lcontent = []
        Ltitle = [] 
        for word in word_list:
            Lcontent.append(Term("content", word))
            Ltitle.append(Term("title", word))
        
        resultTitle = searchTitle(searcher, Ltitle)
        resultDescription = searchDescription(searcher, Lcontent)
        
        #query = And(Lcontent) | Or(Ltitle)
        #query = And(Ltitle)
        #query = And(Lcontent)
        #query = And(Lcontent) | Or(Ltitle)
        #results = searcher.search(query, limit=10)
        #print(results)
        user_query = yield joinResults(resultTitle, resultDescription)

# Ricerca attraverso proximity retrieval con range di voto
def searchByMark(word_list, ix, mark_min=None, mark_max=None):

    marked_games = []
    
    if mark_min is None:
        mark_min = 0

    if mark_max is None:
        mark_max = 100

    results_games = proximitySearch(word_list, ix)

    for r in results_games:
        try:
            if int(r['mark']) in range(mark_min, mark_max):
                marked_games.append(r)
        except:
            continue

    print(f"\nMarked games: {len(marked_games)}")
    for r in marked_games:
        print(f"{r['title']}, with value of {r['mark']}")

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