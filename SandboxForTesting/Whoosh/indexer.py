from pprint import pprint
from whoosh.fields import Schema, TEXT




PATH_TO_DOCUMENT = "../../Documenti"

def readDocument(path):
    '''
    Funzione che legge il documento passato come path.
    Il documento deve essere correttamente formattato.
    Returna una tupla del tipo (titolo, descrizione, valutazione, genere, anno)
    '''
    try:
        with open(path, "r") as file:
            content = file.read()
            title : str = content[content.find("Titolo:") + len("Titolo: ") : content.find("\n", content.find("Titolo:"))]
            description : str = content[content.find("Descrizione:") + len("Descrizione: ") : content.find("\n", content.find("Descrizione:"))]
            mark : str = content[content.find("Valutazione:") + len("Valutazione: ") : content.find("\n", content.find("Valutazione:"))]
            genres : str = content[content.find("Genere:") + len("Genere: ") : content.find("\n", content.find("Genere:"))]
            year : str = content[content.find("Anno:") + len("Anno: ") : content.find("\n", content.find("Anno:"))]
            
 
            """
            title = stem(title)
            description = stem(description)
            mark = stem(mark)
            genres = stem(genres)
            """


            return (title, description, mark, genres, year)
    except:
        raise FileNotFoundError

def openIndex():
    #Sto copiando dal tutorial, ma direi di star creando appunto uno schema che ha
    #un titolo in formato testuale e un contenuto in formato testuale
    from whoosh import analysis
    ana = analysis.StemmingAnalyzer(stoplist=None, minsize=0, maxsize=0)
    schema = Schema(title=TEXT(stored=True, analyzer=ana), content=TEXT(stored=True, analyzer=ana),
        mark=TEXT(stored=True, analyzer=ana), genres=TEXT(stored=True, analyzer=ana), year=TEXT(stored=True, analyzer=ana))

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
            document = readDocument(PATH_TO_DOCUMENT+"/"+f)

            #Writer accetta stringhe in unicode, ma ho letto che tutte le stringhe in python3 sono in unicode quindi polleg
            writer.add_document(title=document[0], content=document[1], mark = document[2], genres = document[3], year = document[4])

            if document[3] not in genres_list:
                genres_list.append(document[3])


        #print(f"Tutti i generi trovati sono:")
        #pprint(genres_list)
        
        #Salva i documenti nell'indice
        writer.commit()
    else:
        ix = index.open_dir("index")
    return ix