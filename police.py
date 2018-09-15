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
    response = simple_get(request_url)
    return response