import bs4, requests, webbrowser
from matplotlib.pyplot import title
import functools
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
from pprint import pprint
import urllib.parse
import time

os.system("clear")

def getMark(game_name):

    moreResults = False
    
    domain = "https://www.metacritic.com"
    game_title = urllib.parse.quote(game_name)
    result_link = domain+"/search/game/"+game_title+"/results"

    UserAgent = Request(result_link, headers={ 'User-Agent' : 'Mozilla/5.0' })
    html = urlopen(UserAgent)
    parser = BeautifulSoup(html, 'html.parser')
    try:
        results = parser.find('ul', class_='search_results module').find_all('a', href = True)
        listed_games = [result["href"] for result in results]

        if len(listed_games) > 1:
            moreResults = True
            print(f"You've searched for {title}")
            i = 1
            for result in listed_games:
                print(f"{i}. {result}\n")
                i += 1

            choice = input("Choose the right number: ")
            gamepage_link = domain+listed_games[int(choice)-1]
            print("il link è "+ gamepage_link)
            UserAgent = Request(gamepage_link, headers={ 'User-Agent' : 'Mozilla/5.0' })
            html = urlopen(UserAgent)
            mark = BeautifulSoup(html, 'html.parser').find('span', itemprop='ratingValue').get_text()

        if not moreResults:
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

directory = '/home/christian/Università/Gestione dell\'informazione/Progetto/Documenti/'

for filename in os.listdir(directory):

    file_game = open(directory+filename,'r')
    game_name = file_game.readline()
    title = game_name[8:-1]
    alreadyRanked = os.system(f"cat {directory+filename} | tail -n1")
    file_game.close()
    try:
            game_rank=getMark(title)
            print(title+": " + game_rank )
            ins = open(directory+filename, 'a')
            ins.write(f"\n\nValutazione: {game_rank}")
            ins.close()

    except:
        print(f"{title}: Nessun voto\n\n")