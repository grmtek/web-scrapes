import collections
import re
import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def parseFixtures():
    fullgame = collections.defaultdict(list)

    try:
        html = urlopen("https://www.skysports.com/cricket/teams/south-africa/fixtures")
        bs = BeautifulSoup(html.read(), 'html.parser')
        fixturedates = bs.find_all('h3', {'class': 'text-h5 box strap3 -interact -caps -center'})
        fixturelist = bs.find_all('div', {'class':'event-grp'})

    except Exception as e:
        raise(e)

    for date in fixturedates:
        gameday = [date.get_text()]

        for fullday in gameday:
            fullgame["date"].append(fullday[:])

    for game in fixturelist:
        gameinfo = [game.get_text().replace("\n", " ")]
        for cricmatch in gameinfo:
            cricmatch = re.findall('[A-Z][a-z]*[A-Z a-z]*[v]*[A-Za-z0-9 ]*[0-9]{4}', cricmatch)
            fullgame["match"].append(cricmatch[:])

    return(fullgame)

def proteasFixtures():
    fullgame = parseFixtures()
    with open("schedule.json", 'w') as outfile:
        json.dump(fullgame, outfile)

    pprint.pprint(fullgame)

def main():
    parseFixtures()
    proteasFixtures()

if __name__ == "__main__":
    main()