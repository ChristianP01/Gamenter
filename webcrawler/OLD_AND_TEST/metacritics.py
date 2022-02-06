from distutils import text_file
import bs4, requests, webbrowser
from matplotlib.pyplot import title
import functools
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
from pprint import pprint
import urllib.parse
import time


PATH_TO_DIRECTORY = "../../DocumentiTest" #Teddy
#I file sono 18828 (contati con wc, non sono calcolati dinamicamente, magari TODO di aggiungere il calcolo dinamico)
FILE_NUMBER = 18828

def getMark(game_name):
    
    domain = "https://www.metacritic.com"
    game_title = urllib.parse.quote(game_name)
    result_link = domain+"/search/game/"+game_title+"/results"

    UserAgent = Request(result_link, headers={ 'User-Agent' : 'Mozilla/5.0' })
    html = urlopen(UserAgent)
    parser = BeautifulSoup(html, 'html.parser')
    try:
        results = parser.find('ul', class_='search_results module').find_all('a', href = True)
        listed_games = [result["href"] for result in results]

        try:
            if len(listed_games) > 1:
                i = 1
                for result in listed_games:
                    print(f"{i}. {result}")
                    i += 1
                print("x. Il gioco non è presente")
                choice = input("Choose the right number: ")
                if choice == 'x':
                    raise Exception("Gioco non trovato")
            else:
                choice = 1
            gamepage_link = domain+listed_games[int(choice)-1]
            #print(f"\nHai scelto : {listed_games[0]}")

            UserAgent = Request(gamepage_link, headers={ 'User-Agent' : 'Mozilla/5.0' })
            html = urlopen(UserAgent)
            mark = BeautifulSoup(html, 'html.parser').find('span', itemprop='ratingValue').get_text()
            
            if mark.isnumeric():
                return mark
            else:
                raise TypeError("N\A")
        except:
            raise Exception("Gioco non trovato")
    except:
        raise Exception("Gioco non trovato")



import os
#E' dove ho io la lista di documenti... Al momento lascio così perché a github non gli piacciono i 18000 file e quindi li tengo fuori dal progetto
directory = PATH_TO_DIRECTORY
 

c=0
for filename in os.listdir(directory):
    c+=1
    print(f"####################################\n{c}/{FILE_NUMBER}\n####################################")
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        #time.sleep(0.5)
        file_game = open(f,'r')
        game_name = file_game.readline()
        text_from_file = file_game.read()
        if (text_from_file.find("Valutazione:") < 0):
            title = game_name[8:-1]
            print(f"Ricerco {game_name}")
            file_game.close()
            file_game = open(f,'a')
            try:
                voto = getMark(title)
                print(title+": "+str(voto))
                file_game.write("\n\nValutazione: "+str(voto)+"\n")
            except:
                print(f"{title}: Gioco non trovato")
                file_game.write("\n\nValutazione: Non presente\n")
