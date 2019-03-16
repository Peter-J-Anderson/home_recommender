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


def _convert_coverage_to_signal(coverage):
	result = ""
	if coverage == "A":
		result = "50%"
	elif coverage == "G":
		result = "99%"
	elif coverage == "R":
		result = "00%"

	return result

def get_mobile_coverage(postcode):
    samknows_ofcomapi_url = "https://ofcomapi.samknows.com/mobile-coverage-pc-enhanced?postcode={}".format(postcode.replace(' ', ''))
    json_data = simple_get(samknows_ofcomapi_url)
    data = json.loads(json_data)
    return data['data']

def output_mobile_coverage(data):
	for provider in data:
		print("Provider: {}".format(provider['provider']))
		print("\tData (indoors): {}".format(_convert_coverage_to_signal(provider['data_indoor'])))
		print("\tData (outdoor): {}".format(_convert_coverage_to_signal(provider['data_outdoor'])))

def get_fixed_line_coverage(postcode):
    samknows_ofcomapi_url = "https://ofcomapi.samknows.com/fixed-line-coverage-pc?postcode={}".format(postcode.replace(' ', ''))
    json_data = simple_get(samknows_ofcomapi_url)
    data = json.loads(json_data)
    return data['data']
