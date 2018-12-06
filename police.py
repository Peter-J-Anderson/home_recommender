#!/usr/bin/env python
import logging
from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint 
from basic_request import *
from location import *

class crime_instance:
    category = ""
    context = ""
    crime_id = ""
    geo_coords = None
    location_street_id = ""
    location_street_desc = ""
    location_subtype = ""
    location_type = ""
    month = ""
    outcome_status = ""
    persistent_id = ""

    def __init__(self, crime_id, persistent_id):
        self.crime_id = crime_id
        self.persistent_id = persistent_id

    def output(self):
        print("context: {}".format(self.context))
        print("\tmonth: {}".format(self.month))
        print("\tstread_desc: {}".format(self.location_street_desc))
        print("\toutcome_status: {}".format(self.outcome_status))
        print("\tid: {}".format(self.persistent_id))

def get_crime_stats(latitude, longitude):
    """
    get crime stats 
    """
    police_url = "https://data.police.uk/api/crimes-street"
    lat_long1 = "{},{}".format((latitude - 0.0035),(longitude - 0.0035))
    lat_long2 = "{},{}".format((latitude + 0.0035),(longitude - 0.0035))
    lat_long3 = "{},{}".format((latitude),(longitude + 0.0035))

    api_args = "all-crime?poly={}:{}:{}&date=2017-01".format(lat_long1, lat_long2, lat_long3)
    request_url = "{}/{}".format(police_url, api_args)
    # print(request_url)
    json_data = simple_get(request_url)
    data = json.loads(json_data)

    crime_instances = list()
    for crime in data:
        instance = crime_instance(crime['id'], crime['persistent_id'])
        instance.context = crime['context']
        instance.location_subtype = crime['location_subtype']
        instance.location_type = crime['location_type']
        instance.outcome_status = crime['outcome_status']
        instance.longitude = crime['location']['latitude']

        instance.latitude = crime['location']['longitude']
        instance.location_street_id = crime['location']['street']['id']
        instance.location_street_desc = crime['location']['street']['name']
        instance.latitude = crime['month']

        crime_instances.append(instance)

    return crime_instances