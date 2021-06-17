import collections
import json
import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup

def parseEvents():
    gigschedule = collections.defaultdict(list)

    try:
        html = urlopen("https://inertia-entertainment.com/")
        bs = BeautifulSoup(html.read(), 'html.parser')
        giginfo = bs.find('ul', {'class': 'eventsList'}).find_all('h3')
        gigdates = bs.find('ul', {'class': 'eventsList'}).find_all('p', {'class': 'date'})
        gigtimes = bs.find('ul', {'class': 'eventsList'}).find_all('p', {'class': 'time'})
        gigvenues = bs.find('ul', {'class': 'eventsList'}).find_all('p', {'class': 'venue'})
        gigextradetails = bs.find('ul', {'class': 'eventsList'}).find_all('div', {'class': 'details'})

    except Exception as e:
        raise(e)

    for artists in giginfo:
        bands = [artists.get_text()]
        for band in bands:
            gigschedule["band"].append(band[:])

    for dayofgig in gigdates:
        schedule = [dayofgig.get_text()]
        for date in schedule:
            gigschedule["date"].append(date[:])

    for details in gigtimes:
        hourofmetal = [details.get_text()]
        for time in hourofmetal:
            gigschedule["time"].append(time[:])

    for locations in gigvenues:
        places = [locations.get_text()]
        for venue in places:
            gigschedule["venue"].append(venue[:])

    for info in gigextradetails:
        fyi = [info.get_text()]
        for details in fyi:
            gigschedule["details"].append(details[:])

    return(gigschedule)


def torontoGigs():
    gigschedule = parseEvents()
    with open("inertia-schedule.json", 'w') as outfile:
        json.dump(gigschedule, outfile)
    for each_row in zip(*([i] + (j)
                          for i, j in gigschedule.items())):
        print(*each_row, "\n=============================="
                         "================================="
                         "=================================="
                         "=============\n")

#    pprint.pprint(gigschedule)

def main():
    parseEvents()
    torontoGigs()

if __name__ == "__main__":
    main()