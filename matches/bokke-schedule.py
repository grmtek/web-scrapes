import collections
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def parseFixtures():
    fullgame = collections.defaultdict(list)

    try:
        html = urlopen("https://www.skysports.com/rugby-union/teams/south-africa/fixtures")
        bs = BeautifulSoup(html.read(), 'html.parser')
        fixturedates = bs.find_all('h4', {'class': 'fixres__header2'})
        tournament = bs.find_all('h5', {'class': 'fixres__header3'})
        fixturetime = bs.find_all('span', {'class': 'matches__date'})
        hometeam = bs.find_all('span', {'class': 'matches__item-col matches__participant matches__participant--side1'})
        awayteam = bs.find_all('span', {'class' : 'matches__item-col matches__participant matches__participant--side2'})

    except Exception as e:
        raise(e)

    for gametype in tournament:
        game = [gametype.get_text()]

        for mode in game:
            mode = mode.strip()
            mode = '[' + mode + ']'
            fullgame["tournament"].append(mode[:])

    for date in fixturedates:
        gameday = [date.get_text()]

        for fullday in gameday:
            fullday = fullday.strip()
            fullday = fullday + ":"
            fullgame[" date"].append(fullday[:])


    for team in hometeam:
        homesquad = [team.get_text()]

        for club in homesquad:
            club = club.strip()
            club = club + ' vs'
            fullgame[" home"].append(club[:])

    for team in awayteam:
        awaysquad = [team.get_text()]

        for club in awaysquad:
            club = club.strip()
            fullgame[" away"].append(club[:])

    for td in fixturetime:
        gametime = [td.get_text()]

        for time in gametime:
            time = time.strip()
            time = '@ ' + time + ' (UTC)'
            fullgame[" time"].append(time[:])

    return fullgame

def bokkeFixtures():
    fullgame = parseFixtures()
    with open("springboks-schedule.json", 'w') as outfile:
        json.dump(fullgame, outfile)
    for each_row in zip(*([i] + (j)
                          for i, j in fullgame.items())):
        print('🏉', *each_row)

def main():
    parseFixtures()
    bokkeFixtures()

if __name__ == "__main__":
    main()