#!/bin/python3.6

import requests
import argparse
import secrets

parser = argparse.ArgumentParser(description='lastify-cli')
parser.add_argument('--user', required=True, help="lastfm username to query")
parser.add_argument('--page', required=False, default=1, type=int, help="lastfm paginates responses. Defaults to page 1")
parser.add_argument('--period', required=False, default='overall', help="overall|6day|1month|3month|6month|12month")
parser.add_argument('--type', required=False, default='Top', help="")

args = parser.parse_args()

user = args.user
page = args.page
period = args.period
type = args.type
api_key = secrets.apikey

def queryTopTracks():

    try:
        payload = {'user': user,
                   'api_key': api_key,
                   'format': 'json',
                   'period': period,
                   'page': page}

        r = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getTopTracks', params=payload)
        jsonResponse = r.json()

    except Exception as e:
        raise(e)

    i = 0
    while True:
        try:

            artist = jsonResponse['toptracks']['track'][i]['artist'].get("name")
            track = jsonResponse['toptracks']['track'][i].get("name")
            i += 1
            print(artist, "- " + track)
        except IndexError:
            # print(IndexError)
            break

def queryLovedTracks():

    try:
        payload = {'user': user,
                   'api_key': api_key,
                   'limit': 100,
                   'format': 'json',
                   'page': page}

        r = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getLovedTracks', params=payload)
        jsonResponse = r.json()

    except Exception as e:
        raise(e)

    i = 0
    while True:
        try:

            artist = jsonResponse['lovedtracks']['track'][i]['artist'].get("name")
            track = jsonResponse['lovedtracks']['track'][i].get("name")
            i += 1
            print(artist, "- " + track)
        except IndexError:
            # print(IndexError)
            break

def main():
    queryTopTracks()
    print("===========================================")
    queryLovedTracks()

if __name__ == "__main__":
    main()