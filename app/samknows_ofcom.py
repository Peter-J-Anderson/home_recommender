#!/usr/bin/env python
"""
Module for interacting with sam knows ofcom
"""
from __future__ import print_function
import json

from basic_request import simple_get

def _convert_coverage_to_signal(coverage):
    """
    Convert signal grade to percent string
    """
    result = ""
    if coverage == "A":
        result = "50%"
    elif coverage == "G":
        result = "99%"
    elif coverage == "R":
        result = "00%"

    return result

def get_mobile_coverage(postcode):
    """
    Get mobile coverage data based on postcode
    """
    base_url = "https://ofcomapi.samknows.com/mobile-coverage-pc-enhanced"
    query_url = "{}?postcode={}".format(base_url, postcode.replace(' ', ''))
    json_data = simple_get(query_url)
    data = json.loads(json_data)
    return data['data']

def output_mobile_coverage(data):
    """
    Output mobile phone coverage data
    """
    for provider in data:
        print("Provider: {}".format(provider['provider']))
        print("\tData (indoors): {}".format(_convert_coverage_to_signal(provider['data_indoor'])))
        print("\tData (outdoor): {}".format(_convert_coverage_to_signal(provider['data_outdoor'])))

def get_fixed_line_coverage(postcode):
    """
    Get fixed line coverage data based on postcode
    """
    base_url = "https://ofcomapi.samknows.com/fixed-line-coverage-pc"
    query_url = "{}?postcode={}".format(base_url, postcode.replace(' ', ''))
    json_data = simple_get(query_url)
    data = json.loads(json_data)
    return data['data']
