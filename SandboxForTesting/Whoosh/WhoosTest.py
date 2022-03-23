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
    Il documento deve essere correttamente formattato
    '''
    try:
        with open(path, "r") as file:
            content = file.read()
            dprint(content)
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

    #Questa roba andrà fatta per ogni file della cartella documenti, andandosi a prendere il titolo ed il contenuto

    writer = ix.writer()
    #writer.add_document(title=u"My document", content=u"Contenuto")

    from os import listdir

    for f in listdir(PATH_TO_DOCUMENT):
        readDocument(PATH_TO_DOCUMENT+"/"+f)
