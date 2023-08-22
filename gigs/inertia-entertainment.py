import collections
import json
import pprint
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup

def parseEvents():
    gigschedule = collections.defaultdict(list)

    try:
        page_url = 'https://inertia-entertainment.com'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        resp = Request(page_url, headers=headers)
        response = urlopen(resp)
        bs = BeautifulSoup(response.read(), 'html.parser')
        giginfo = bs.find_all('h1', {'class': 'elementor-heading-title'})
        del(giginfo[0])
        pprint.pprint(giginfo)
        gigdates = bs.find_all('li', {'class': 'elementor-icon-list-item elementor-repeater-item-1777b88 elementor-inline-item'})
        gigvenues = bs.find_all('li', {'class': 'elementor-icon-list-item elementor-repeater-item-2c0120c elementor-inline-item'})
#        gigextradetails = bs.find('ul', {'class': 'events'}).find_all('div', {'class': 'details'})

    except Exception as e:
        raise(e)

    for artists in giginfo:
        bands = [artists.get_text()]

        for band in bands:
            gigschedule["band"].append(band[:])


    for dayofgig in gigdates:
        schedule = [dayofgig.get_text()]
        for date in schedule:
            date = date.strip()
            gigschedule["- date"].append(date[:])

    for locations in gigvenues:
        places = [locations.get_text()]
        for venue in places:
            venue = venue.strip()
            gigschedule["- venue"].append(venue[:])
#
#    for info in gigextradetails:
#        fyi = [info.get_text()]
#        for details in fyi:
#            gigschedule["details"].append(details[:])
#
    return(gigschedule)


def torontoGigs():
    gigschedule = parseEvents()
    with open("inertia-schedule.json", 'w') as outfile:
        json.dump(gigschedule, outfile)
    for each_row in zip(*([i] + (j)
                          for i, j in gigschedule.items())):
        print("🎸", *each_row, "🤘")


#    pprint.pprint(gigschedule)

def main():
    parseEvents()
    torontoGigs()

if __name__ == "__main__":
    main()
