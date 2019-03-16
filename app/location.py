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
from google_api import *

class geo_coords(object):
    latitude = ""
    longitude = ""

    def __init__(self, latitude, longitude):
        self.latitude = latitude 
        self.longitude = longitude