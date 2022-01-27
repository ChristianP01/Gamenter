import requests

indici = {}
for anno in range(1940,2022):
    url = f"https://en.wikipedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:{anno}_video_games&prop=categories&cllimit=max&gcmlimit=max&format=json"
    print(f"Scarico videogiochi anno {anno}")
    try:
        data = requests.get(url)
        dict_data = dict(data.json())
        for page in dict_data["query"]["pages"].values():
            indici[page["pageid"]] = [page["title"],anno]
    except:
        print(f"ERRORE: non ci sono videogiochi nell'anno {anno}")
        continue
    

for a,b in indici.items():
    print(f"Page id: {a}")
    print(f"Titolo {b[0]}, anno {b[1]}")
    print("\n")