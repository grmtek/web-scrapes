import collections
import json
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup

def parseEvents():
    gigschedule = collections.defaultdict(list)

    try:
        page_url = 'https://bachtrack.com/search-events/city=672'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        resp = Request(page_url, headers=headers)
        response = urlopen(resp)
        bs = BeautifulSoup(response.read(), 'html.parser')
        giginfo = bs.find_all('div', {'class':'listing-programme-simple'}, limit=7)
        del(giginfo[1]) #removes 'wishlist' entry
        gigdates = bs.find_all('div', {'class': 'listing-shortform-dates'}, limit=7)
        gigvenues = bs.find_all('div', {'class': 'li-shortform-venue'}, limit=7)


    except Exception as e:
        raise(e)

    for dayofgig in gigdates:
        schedule = [dayofgig.get_text()]
        for date in schedule:
            date = date.strip()
            date = date + ':'
            gigschedule["date"].append(date[:])

    for artists in giginfo:
        bands = [artists.get_text()]

        for band in bands:
            band = band.replace('\n', ' ')
            band = band + ' -'
            gigschedule["- piece"].append(band[:])


    for locations in gigvenues:
        places = [locations.get_text()]
        for venue in places:
            venue = venue.strip()
            venue = '@ ' + venue
            gigschedule["- venue"].append(venue[:])

    return gigschedule

def torontoShows():
    gigschedule = parseEvents()
    with open("tso-schedule.json", 'w') as outfile:
        json.dump(gigschedule, outfile)
    for each_row in zip(*([i] + (j)
                          for i, j in gigschedule.items())):
        print("🎻", *each_row, "🎺")


def main():
    parseEvents()
    torontoShows()

if __name__ == "__main__":
    main()
