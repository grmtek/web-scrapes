#!/bin/python3.6
import pprint

import json
import requests
import argparse
import secrets
import collections


parser = argparse.ArgumentParser(description='nastify-cli')
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
spotify_user_id = secrets.spotify_user_id
spotify_token = secrets.spotify_token

def querytoptracks():
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
    track_list = collections.defaultdict(list)
    while True:

        try:

            artist = jsonResponse['toptracks']['track'][i]['artist'].get("name")
            track_list["artist"].append(artist[:])
            track = jsonResponse['toptracks']['track'][i].get("name")
            track_list["track"].append(track[:])
            i += 1
#            print(artist, "- " + track)
#            print(track_list)
        except IndexError:
            # print(IndexError)
            break

    return track_list


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

def pulltrackURI():
    track_list = querytoptracks()
   # print(track_list)

    i = 0
    for object in track_list:
        while i >= 0:

            try:

                artist = track_list["artist"][i].replace(" ", "%20")
                track = track_list["track"][i].replace(" ", "%20")
                uris = []
                query = f"https://api.spotify.com/v1/search?query=track%3A{track}+artist%3A{artist}&type=track&offset=0&limit=1"
                response = requests.get(
                    query,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {spotify_token}"
                    }
                )

                if response.status_code != 200:
                    print(f"\nERROR RESPONSE CODE: {response.status_code}\n")

                response_json = response.json()
                songs = response_json["tracks"]["items"]

                for uri in songs:
                    #print(songs[0]["uri"])
                    if songs[0]["uri"] == "":
                        pass
                    else:
                        uris.append(songs[0]["uri"])
                        return uris
                print(uris)


                #if range(len(track_list)):
                #    print(range(len(track_list)))
                i += 1

                #return songs
            except IndexError:
                print("end of index reached")
                i = -1
                pass



           # return uri

def addsongstoplaylist():
    uris = pulltrackURI()



def main():
    querytoptracks()
    pulltrackURI()
    addsongstoplaylist()
    #print("===========================================")
#    queryLovedTracks()

if __name__ == "__main__":
    main()