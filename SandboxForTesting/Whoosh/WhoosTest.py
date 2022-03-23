from whoosh.fields import Schema, TEXT

#Sto copiando dal tutorial, ma direi di star creando appunto uno schema che ha
#un titolo in formato testuale e un contenuto in formato testuale
schema = Schema(title=TEXT, content=TEXT)
