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

def get_mobile_coverage(postcode):
    samknows_ofcomapi_url = "https://ofcomapi.samknows.com/mobile-coverage-pc-enhanced?postcode{}".format(postcode)
    data = simple_get(samknows_ofcomapi_url)
    route = None
    return route
