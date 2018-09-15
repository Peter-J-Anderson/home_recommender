#!/usr/bin/env python
import logging
from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json
import os
from pprint import pprint 
from basic_request import *

def get_street_name(latitude, longitude, address):
    geoencoding_api_key = os.environ['GOOGLE_GEOCODING_API_KEY']
    geoencoding_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(latitude, longitude,geoencoding_api_key)
    print(geoencoding_url)
    data = simple_get(geoencoding_url)
    route = None
    pprint(data)
    return route
