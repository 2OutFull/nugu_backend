import requests
import json

url = "https://www.thesportsdb.com/api/v1/json/1/search_all_teams.php?l=Italian%20Serie%20A"
r = requests.get(url).text
tt = json.loads(r)

for t in tt["teams"]:
    print(t["strTeam"], t["idTeam"])
