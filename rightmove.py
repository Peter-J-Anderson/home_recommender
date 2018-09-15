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

class rightmove_property(object):
    url = ""
    address = ""
    street_name = ""
    geo_coords = None
    def __init__(self, url, address, geo_coords):
        self.url = url
        self.address = address
        self.geo_coords = geo_coords

class geo_coords(object):
    latitude = ""
    longitude = ""

    def __init__(self, latitude, longitude):
        self.latitude = latitude 
        self.longitude = longitude


def get_lat_long(soup):
    """
    get lat long of property from the minimap display
    """
    if soup is None:
        raise Exception("soup cannot be None")
    
    mini_map_src = soup.find("a", {"class" : "js-ga-minimap"}).img['src']
    longitude = re.search('longitude=([^&]*)', mini_map_src).group(1)
    latitude = re.search('latitude=([^&]*)', mini_map_src).group(1)
    return geo_coords(latitude, longitude)

def get_street_name_old(rightmove_property):
    if rightmove_property == None: 
        raise Exception("rightmove_property cannot be None")
    
    geo_coords = rightmove_property.geo_coords
    if geo_coords == None: 
        raise Exception("geo_coords cannot be None")
    
    data = None
    route = None
    with open('data.json') as data_file: 
        data = json.load(data_file)
        addresses = data['results']
        for address in addresses:
            address_parts = address['address_components']
            for address_part in address_parts:
                if 'route' in address_part['types']:
                    route = address_part['long_name']
                    print(route)
        
            if route in rightmove_property.address:
                print("{} is in {}".format(route, rightmove_property.address))
                break
    return route

def get_rightmove_property(url):
    """
    Pase html of the given URL to get a property
    """
    response = simple_get(url)
    if response is None:
        raise Exception('Error retrieving content at {}'.format(url))
    soup = BeautifulSoup(response, 'html.parser')
    address = soup.find(itemprop = 'streetAddress')['content']
    geo_coords = get_lat_long(soup)
    rm_property = rightmove_property(url, address, geo_coords)
    street_name = get_street_name(rm_property.geo_coords.latitude, rm_property.geo_coords.longitude, rm_property.address)
    rm_property.street_name = street_name

    
    
    return rm_property