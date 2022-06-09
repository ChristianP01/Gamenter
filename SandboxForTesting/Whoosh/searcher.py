from unittest import result
from whoosh.query import *
from indexer import *
import urllib

'''
                                                #################################################
                                                #       Blocco di funzioni utilizzato per       #
                                                #        applicare i filtri alla ricerca        #
                                                #################################################
'''
def searchTitle(searcher, titleList):
    '''
    Applica una query booleana "AND" a tutte le keyword in titleList sui titoli dei documenti

    INPUT: il searcher e la lista delle keyword
    OUTPUT: un set di risultati di whoosh
    '''
    query = And(titleList)
    results = searcher.search(query)
    return results

def searchDescription(searcher, descList):
    '''
    Applica una query booleana "AND" a tutte le keyword in descList sulla descrizione dei documenti

    INPUT: il searcher e la lista delle keyword
    OUTPUT: un set di risultati di whoosh
    '''
    query = And(descList)
    results = searcher.search(query)
    return results


def filterGenre(termsList, genre):
    '''
    Esclude dai risultati i giochi che non appartengono ad un dato genere (1 o più)

    INPUT: la lista dei "termini" (prodotta da join_result) ed il genere
    OUTPUT: la nuova lista dei "termini" filtrata
    '''
    results = []
    for t in termsList:
        if termsList[t][2] == genre:
            results[t] = termsList[t]
    return results

def filterYear(termsList, year, operation):
    """
    Prende in ingresso un set di risultati e fa i controlli sull'anno

    INPUT: la lista dei "termini" (prodotta da join_result), l'anno e l'operazione
    OUTPUT: la nuova lista dei "termini" filtrata
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

    INPUT: la lista dei "termini" (prodotta da join_result), il voto e l'operazione
    OUTPUT: la nuova lista dei "termini" filtrata
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


'''
                                                    ##################################################
                                                    #                  Fine blocco                   #
                                                    ##################################################
'''


def joinResults(*results):
    '''
    Funzione che prende in ingresso l'output di search_title e search_description e li joina.

    Durante la fase di join, i risultati ricavati dal titolo (che DEVONO essere passati per primi) avranno un peso maggiore del 50% rispetto 
    ai risultati trovati facendo la ricerca sulla descrizione
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



def check_filter(f):
    '''
    Funzione che prende in ingresso un filtro-"lista" e controlla che sia corretto sintatticamente

    INPUT: Una lista composta da TIPO OPERAZIONE [DATO]
    OUTPUT: True o False in base alla correttezza sintattica
    '''
    if f[0] not in ["year", "mark", "genre", "title", "content"]:
        return False
    if f[0] in ["year", "mark"]:
        if f[1] not in ["<", ">", "=", ">=" , "<="]:
            return False
        try:
            int(f[2])
        except ValueError:
            return False
    if f[0] in ["title", "content"]:
        if f[1] not in ["True", "False"]:
            return False
    if f[0] == "genre":
        if len(f) == 1:
            return False
    return True 


def parse_filter(f, input):
    '''
    Funzione che prende in ingresso il dizionario dei filtri ed una stringa filtro da parsare

    INPUT: Il dizionario dei filtri base o già riempito con qualcosa e una stringa rappresentante un filtro
    OUTPUT: Il dizionario dei filtri aggiornato (eventualmente invariato se il filtro non è corretto)
    '''
    l_input = input.split(" ")
    if check_filter(l_input):
        if l_input[0] == "year":
            l_command = [l_input[1], l_input[2]]
            f["year"].append(l_command)
        if l_input[0] == "mark":
            l_command = [l_input[1], l_input[2]]
            f["mark"].append(l_command)
        if l_input[0] == "genre":
            #NON FUNZIONA SE IL GENERE E' SEPARATO DA DEGLI SPAZI
            for genere in l_input[1:]:
                f["genre"].append(genere)
        if l_input[0] == "title":
            if l_input[1] == "True":
                f["title"] = True
            else:
                f["title"] = False
        if l_input[0] == "content":
            if l_input[1] == "True":
                f["content"] = True
            else:
                f["content"] = False
    else:
        print("Errore nel filtro! Controlla che la sintassi sia corretta")


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
    '''
    Generatore che funge da interfaccia con l'indice ed il searcher di whoosh
    '''
    ix = openIndex()
    searcher = ix.searcher()
    #user_input è una tupla
    user_query = user_input[0]
    user_filter = user_input[1]
    while True:
        #Controllo dell'input
        if user_query == "":
            user_query, user_filter = yield ""

        word_list = user_query.split(" ")
        word_list = [w.lower() for w in word_list]

        Lcontent = []
        Ltitle = [] 

        #Creo le liste di termini da utilizzare durante la ricerca
        for word in word_list:
            Lcontent.append(Term("content", word))
            Ltitle.append(Term("title", word))
        
        results_title = []
        results_content = []


        if user_filter != None:
            #Applico la ricerca sul titolo, se specificato dai filtri
            if user_filter["title"]:
                results_title = searchTitle(searcher, Ltitle)
            #Applico la ricerca sul contenuto, se specificato dai filtri
            if user_filter["content"]:
                results_content = searchDescription(searcher, Lcontent)
            #Se non è specificata alcun tipo di ricerca, sollevo un'eccezione
            if results_content is None and results_title is None:
                raise Exception("Error: you have to specify at least one field to search on")

            #Creo la lista di risultati pesata e joinata
            unfiltered_results = joinResults(results_title, results_content)
            #Applico i filtri
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



'''
                                        #################################################################
                                        #             Le funzioni qua sotto vengono utilizzate          #
                                        #                     solamente da gui.py                       #
                                        #################################################################
'''


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
    user_query = user_query.lower()
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

