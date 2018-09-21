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
    samknows_ofcomapi_url = "https://ofcomapi.samknows.com/mobile-coverage-pc-enhanced?postcode={}".format(postcode.replace(' ', ''))
    json_data = simple_get(samknows_ofcomapi_url)
    data = json.loads(json_data)
    return data['data']

def get_fixed_line_coverage(postcode):
    samknows_ofcomapi_url = "https://ofcomapi.samknows.com/fixed-line-coverage-pc?postcode={}".format(postcode.replace(' ', ''))
    json_data = simple_get(samknows_ofcomapi_url)
    data = json.loads(json_data)
    return data['data']
