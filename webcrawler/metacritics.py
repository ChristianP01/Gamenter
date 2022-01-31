import bs4, requests, webbrowser
from matplotlib.pyplot import title
import functools
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
from pprint import pprint
import urllib.parse
import time

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

        #print(f"\nHai scelto : {listed_games[0]}")

        gamepage_link = domain+listed_games[0]
        UserAgent = Request(gamepage_link, headers={ 'User-Agent' : 'Mozilla/5.0' })
        html = urlopen(UserAgent)
        mark = BeautifulSoup(html, 'html.parser').find('span', itemprop='ratingValue').get_text()
        
        if mark.isnumeric():
            return mark
        else:
            raise TypeError("N\A")
    except:
        raise Exception("Gioco non trovato")



import os
#E' dove ho io la lista di documenti... Al momento lascio così perché a github non gli piacciono i 18000 file e quindi li tengo fuori dal progetto
directory = '../../Documenti'
 

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        #time.sleep(0.5)
        file_game = open(f,'r')
        game_name = file_game.readline()
        title = game_name[8:-1]
        try:
            print(title+": "+getMark(title))
        except:
            print(f"{title}: Gioco non trovato")
