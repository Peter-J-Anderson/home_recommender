#!/usr/bin/env python
import logging
from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json
from location import GeoCoords
from pprint import pprint 
from basic_request import *
from google_api import *
from location import *

class rightmove_property(object):
    url = ""
    ad_address = ""
    geo_coords = None
    rough_address = None
    def __init__(self, url, ad_address, geo_coords):
        self.url = url
        self.ad_address = ad_address
        self.geo_coords = geo_coords

    def output(self):
        print(self.url)
        print(self.ad_address)

def get_lat_long(soup):
    """
    get lat long of property from the minimap display
    """
    if soup is None:
        raise Exception("soup cannot be None")
    
    mini_map_src = soup.find("a", {"class" : "js-ga-minimap"}).img['src']
    longitude = re.search('longitude=([^&]*)', mini_map_src).group(1)
    latitude = re.search('latitude=([^&]*)', mini_map_src).group(1)
    return GeoCoords(latitude, longitude)

def get_rightmove_property(url):
    """
    Pase html of the given URL to get a property
    """
    response = simple_get(url)
    if response is None:
        raise Exception('Error retrieving content at {}'.format(url))
    soup = BeautifulSoup(response, 'html.parser')
    ad_address = soup.find(itemprop = 'streetAddress')['content']
    geo_coords = get_lat_long(soup)
    rm_property = rightmove_property(url, ad_address, geo_coords)
    rough_address = get_rough_address_from_lat_long(rm_property.geo_coords.latitude, rm_property.geo_coords.longitude, rm_property.ad_address)
    rm_property.rough_address = rough_address
    return rm_property
