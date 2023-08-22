import collections
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def parseFixtures():
    fullgame = collections.defaultdict(list)

    try:
        html = urlopen("https://www.cricschedule.com/team/south-africa.php")
        bs = BeautifulSoup(html.read(), 'html.parser')
        fixturedates = bs.find_all('abbr', {'class': 'dtstart'})
        fixturevenue = bs.find_all('span', {'class': 'location'})
        fixturelist = bs.find_all('a', {'class': 'url'})

    except Exception as e:
        raise(e)

    for date in fixturedates:
        gameday = [date.get_text()]

        for fullday in gameday:
            fullday = fullday.strip()
            fullday = fullday + ":"
            fullgame["date"].append(fullday[:])

    for game in fixturelist:
        gameinfo = [game.get_text()]
        for cricmatch in gameinfo:
            fullgame["match"].append(cricmatch[:])

    for venue in fixturevenue:
        location = [venue.get_text()]
        for cricdate in location:
            cricdate = cricdate.strip()
            cricdate = '@' + cricdate
            fullgame["venue"].append(cricdate[:])

    return fullgame

def proteasFixtures():
    fullgame = parseFixtures()
    with open("cricket-schedule.json", 'w') as outfile:
        json.dump(fullgame, outfile)
    for each_row in zip(*([i] + (j)
                          for i, j in fullgame.items())):
        print('🏏', *each_row, '🌴')

def main():
    parseFixtures()
    proteasFixtures()

if __name__ == "__main__":
    main()