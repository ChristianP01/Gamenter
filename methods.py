from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib

def connectTo(link):
    """
    Si connette al link passato come argomento.
    :param link: Il link a cui bisogna connettersi.
    :type link: String
    :return: parser, è il sorgente html. Usando find() e find_all()
    si possono recuperare i tag necessari. 
    """ 

    UserAgent = Request(link, headers={ 'User-Agent' : 'Mozilla/5.0' })
    html = urlopen(UserAgent)
    parser = BeautifulSoup(html, 'html.parser')
    return parser



#Permette di ottenere il voto facendo una media di tutte le piattaforme in cui quel gioco viene trovato, 
#in modo da non dover inserire i valori a mano ogni volta
def getMark(game_name):
    """
    Si connette al link passato come argomento.
    :param game_name: Il nome del gioco di cui si vuole il voto.
    :type game_name: String
    :return: mark, è il voto del gioco, vale int se accettabile, "N\A" altrimenti. 
    """ 

    domain = "https://www.metacritic.com"
    game_title = urllib.parse.quote(game_name)
    result_link = domain+"/search/game/"+game_title+"/results"
    results = connectTo(result_link).find('ul', class_='search_results module').find_all('a', href = True)
    listed_games = [result["href"] for result in results]
    platform_marks = 0 #Indica il numero di piattaforme che hanno un voto "reale", per fare la media
    avg_mark = 0

    if len(listed_games) > 1:
        i = 1
        for result in listed_games:
            
            try: #Uso un try-except per verificare se il voto è presente.
                    #NB. "I valori "tbd" e " " sono considerati non validi, saranno sostituiti con "N/A"
                mark = connectTo(domain+result).find('span', itemprop='ratingValue').get_text()
            except:
                mark = "N/A"

            if mark.isdecimal():
                platform_marks += 1
                avg_mark += int(mark)

    elif len(listed_games) == 0: 
        raise Exception("No results found!")

    try:
        mark = avg_mark/platform_marks
        return round(int(mark))
    except:
        return "N/A"



def getGenres(game_name):
    """
    Si connette al link passato come argomento.
    :param game_name: Il nome del gioco di cui si vuole il voto.
    :type game_name: String
    :return: genres, è una lista contenente str, generi del gioco, "N\A" altrimenti. 
    """ 

    domain = "https://www.metacritic.com"
    game_title = urllib.parse.quote(game_name)
    result_link = domain+"/search/game/"+game_title+"/results"
    results = connectTo(result_link).find('ul', class_='search_results module').find_all('a', href = True)
    listed_games = [result["href"] for result in results]

    if len(listed_games) > 1:
        i = 1
        for result in listed_games:
            try: #Uso un try-except per verificare se il voto è presente.
                    #NB. "I valori "tbd" e " " sono considerati non validi, saranno sostituiti con "N/A"
                mark = connectTo(domain+result).find('span', itemprop='ratingValue').get_text()
            except:
                mark = "N/A"

            print(f"{i}. {result}, with a score of {mark}")
            i += 1
        print("x. Game is not in the list")
        choice = input("Choose the right number: ")
        if choice == 'x':
            raise Exception("Game was not in the list")

    elif len(listed_games) == 1:
        choice = 1

    elif len(listed_games) == 0: 
        raise Exception("No results found!")

    genres = connectTo(domain+listed_games[int(choice)-1]).find('li', class_='summary_detail product_genre')\
        .find_all('span', class_="data") 

    genres = [genre.text for genre in genres]
    return genres