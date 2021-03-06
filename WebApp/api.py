import requests
import pprint
import json
import os
# from dotenv import load_dotenv
from flask import flash
import logging
# get a key here https://console.developers.google.com/apis/credentials
key = os.environ.get('CIVICS_API_KEY')
# electionId = 2000 for testing purposes
# electionId = 2000
# Google Civics VoterInfoQuery API to get pollsite location
def poll_search(address):
    params = {
        'address': address,
        'key': key
    #    'electionId': electionId
    }
    #address.replace('+','%20')
    # call api
    url = 'https://civicinfo.googleapis.com/civicinfo/v2/voterinfo?'
    req = requests.get(url, params=params)
    data = req.json()
    polling_hours = ""
    #print (data)
    try:
        # GCivic poll location information
        location_name = data['pollingLocations'][0]['address']['locationName']
        location_address = data['pollingLocations'][0]['address']['line1']
        location_city = data['pollingLocations'][0]['address']['city']
        location_state = data['pollingLocations'][0]['address']['state']
        location_zip = data['pollingLocations'][0]['address']['zip']
        full_location = location_address + ', ' + location_city + ', ' + location_state + ', ' + location_zip
        # # early
        # location_name2 = data['earlyVoteSites'][0]['address']['locationName']
        # location_address2 = data['earlyVoteSites'][0]['address']['line1']
        # location_city2 = data['earlyVoteSites'][0]['address']['city']
        # location_state2 = data['earlyVoteSites'][0]['address']['state']
        # location_zip2 = data['earlyVoteSites'][0]['address']['zip']
        # full_location2 = location_address2 + ', ' + location_city2 + ', ' + location_state2 + ', ' + location_zip2
        # polling hours
        try:
            polling_hours = data['pollingLocations'][0]['pollingHours']
        except:
            flash(location_name,"Location Name:")
            flash(full_location,"Full Address:")
            flash(polling_hours,"Polling Hours:")
        # flash(full_location2)
        return full_location
    # Keyerror for polling location
    except KeyError:
        flash("we couldn't find a poll location for the address you've entered.","Sorry,")

# Google Civic representativeByAddress
def rep_search(address):
    params = {
        'address': address,
        'key': key
    }
    url = 'https://civicinfo.googleapis.com/civicinfo/v2/representatives?'
    req = requests.get(url, params=params)
    data = req.json()
    return data

#States data from json
def states():
    f = open('states.json')
    data = json.load(f)
    return data

#upcoming elections Google Civic electionQuery
def election_search():
    params = {
        'key': key
    }
    url = 'https://civicinfo.googleapis.com/civicinfo/v2/elections?'
    req = requests.get(url,params=params)
    data = req.json()
    # f = open('elections.json')
    # data = json.load(f)
    return data
