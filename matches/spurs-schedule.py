import collections
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def parseFixtures():
    fullgame = collections.defaultdict(list)

    try:
        html = urlopen("https://www.theguardian.com/football/tottenham-hotspur/fixtures")
        bs = BeautifulSoup(html.read(), 'html.parser')
        hometeam = bs.find_all('div', {'class': 'football-match__team football-match__team--home football-team'})
        awayteam = bs.find_all('div', {'football-match__team football-match__team--away football-team'})
        fixturedates = bs.find_all('div', {'class': 'date-divider'})
        tournament = bs.find_all('a', {'class': 'football-matches__heading'})
        fixturetime = bs.find_all('td', {'class': 'football-match__status football-match__status--f table-column--sub'})
        fixturetimezone = bs.find_all('span', {'class': 'football-matches__timezone'})

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
            fullgame["date"].append(fullday[:])

    for team in hometeam:
        homesquad = [team.get_text()]

        for club in homesquad:
            club = club.strip()
            club = club + ' vs'
            fullgame["home"].append(club[:])

    for team in awayteam:
        awaysquad = [team.get_text()]

        for club in awaysquad:
            club = club.strip()
            fullgame["away"].append(club[:])

    for td in fixturetime:
        gametime = [td.get_text()]

        for time in gametime:
            time = time.strip()
            time = '@' + time
            fullgame["time"].append(time[:])

    for zone in fixturetimezone:
        gametimez = [zone.get_text()]

        for timezone in gametimez:
            tz = timezone.strip()

            fullgame["zone"].append(tz[:])

    return fullgame

def spursFixtures():
    fullgame = parseFixtures()
    with open("coys-schedule.json", 'w') as outfile:
        json.dump(fullgame, outfile)
    for each_row in zip(*([i] + (j)
                          for i, j in fullgame.items())):
        print('⚽', *each_row)

def main():
    parseFixtures()
    spursFixtures()

if __name__ == "__main__":
    main()
