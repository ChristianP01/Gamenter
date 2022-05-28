from unittest import result
from whoosh.query import *
from indexer import *
import urllib

def searchTitle(searcher, titleList):
    query = And(titleList)
    results = searcher.search(query, limit=10)
    return results

def searchDescription(searcher, descList):
    query = And(descList)
    results = searcher.search(query, limit=10)
    return results


def filterGenre(termsList, genre):
    results = []
    for t in termsList:
        if termsList[t][2] == genre:
            results[t] = termsList[t]
    return results

def filterYear(termsList, year, operation):
    """
    Prende in ingresso un set di risultati e fa i controlli sull'anno
    """
    results = {}
    for t in termsList:
        if operation == "=":
            if termsList[t][1] == year:
                results[t] = termsList[t]
        elif operation == ">":
            if termsList[t][1] > year:
                results[t] = termsList[t]
        elif operation == "<":
            if termsList[t][1] < year:
                results[t] = termsList[t]
        elif operation == ">=":
            if termsList[t][1] >= year:
                results[t] = termsList[t]
        elif operation == "<=":
            if termsList[t][1] <= year:
                results[t] = termsList[t]
    return results

def filterMark(termsList, mark, operation):
    """
    Prende in ingresso un set di risultati e fa i controlli sul voto
    """
    results = {}
    for t in termsList:
        if operation == "=":
            if termsList[t][3] == mark:
                results[t] = termsList[t]
        elif operation == ">":
            if termsList[t][3] > mark:
                results[t] = termsList[t]
        elif operation == "<":
            if termsList[t][3] < mark:
                results[t] = termsList[t]
        elif operation == ">=":
            if termsList[t][3] >= mark:
                results[t] = termsList[t]
        elif operation == "<=":
            if termsList[t][3] <= mark:
                results[t] = termsList[t]
    return results




def joinResults(*results):
    '''
    IL PRIMO PARAMETRO DEVE ESSERE LA LISTA DEI TITOLI
    FORMATO
    Title : [score, year, genre, mark]
    '''

    final_results = {}

    titoli = results[0]
    for t in titoli:
        if t["mark"] != "N/A":
            final_results[t['title']] = [float(t.score) * 1.5, int(t["year"]), t["genres"], int(t["mark"])]
        else:
            final_results[t['title']] = [float(t.score), int(t["year"]), t["genres"], 0]

    for r in results[1:]:
        for doc in r:
            if doc['title'] not in final_results:
                if doc["mark"] != "N/A":
                    final_results[doc['title']] = [float(doc.score), int(doc["year"]), doc["genres"], int(doc["mark"])]
                else:
                    final_results[doc['title']] = [float(doc.score), int(doc["year"]), doc["genres"], 0]
            else:
                if doc["mark"] != "N/A":
                    final_results[doc['title']] += [float(doc.score), int(doc["year"]), doc["genres"], int(doc["mark"])]
                else:
                    final_results[doc['title']] += [float(doc.score), int(doc["year"]), doc["genres"], 0]
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





"""
user_filter è fatto così:

user_filter = {
    "title" : True,
    "content" : False,
    "year" : [[">", "2000"], ["<", "2020"]],
    "mark" : [[">", "50"], ["<", "70"]],
    "genre" : ["Action", "Adventure", "Fantasy"]
}



title e content sono OBBLIGATORI, year, mark e genre sono opzionali

e serve a specificare quali filtri applicare alla query
"""

def searchQueryCLI(user_input):
    ix = openIndex()

    searcher = ix.searcher()
    while True:
        user_query = user_input[0]
        user_filter = user_input[1]
        if user_query == "":
            user_query, user_filter = yield ""
        #Provo a fare una versione che prenda un numero indefinito di parametri
        word_list = user_query.split(" ")
        word_list = [w.lower() for w in word_list]

        Lcontent = []
        Ltitle = [] 
        for word in word_list:
            Lcontent.append(Term("content", word))
            Ltitle.append(Term("title", word))
        
        results_title = []
        results_content = []

        
        if user_filter != None:
            
            if user_filter["title"]:
                results_title = searchTitle(searcher, Ltitle)
            
            if user_filter["content"]:
                results_content = searchDescription(searcher, Lcontent)
            
            if results_content is None and results_title is None:
                raise Exception("Error: you have to specify at least one field to search on")

            unfiltered_results = joinResults(results_title, results_content)

            for filter in user_filter.keys():
                if filter == "title" or filter == "content":
                    continue
                if user_filter[filter] == None:
                        continue
                elif filter == "year":
                    for year_filter in user_filter[filter]:
                        operation = year_filter[0]
                        year = int(year_filter[1])
                        unfiltered_results = filterYear(unfiltered_results, year, operation)
                elif filter == "mark":
                    for mark_filter in user_filter[filter]:
                        operation = mark_filter[0]
                        mark = int(mark_filter[1])
                        unfiltered_results = filterMark(unfiltered_results, mark, operation)
                elif filter == "genre":
                    for genre in user_filter[filter]:
                        unfiltered_results = filterGenre(unfiltered_results, genre)
            
            filtered_result = unfiltered_results

            user_query, user_filter = yield filtered_result
        else:
            resultTitle = searchTitle(searcher, Ltitle)
            resultDescription = searchDescription(searcher, Lcontent)
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
        gui.textBrowser.setPlainText("") #Inizializzo il valore iniziale del box risultati

        for r in results: #Appende i vari risultati singoli all'interno della lista
            # gui.textBrowser.setPlainText(str(gui.textBrowser.toPlainText())+str(r['title'])+" "+str(r.score)+"\n")
            
            gui.textBrowser.append(f"\n<a href=https://en.wikipedia.org/wiki/{urllib.parse.quote(str(r['title']))}> {str(r['title'])} </a>" + f"--> {round(r.score, 2)}")
            Lscores[r['title']]= r.score