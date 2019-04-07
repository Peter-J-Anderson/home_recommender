#!/usr/bin/env python
"""
Module for interacting with right move
"""
from __future__ import print_function
import re

from bs4 import BeautifulSoup
from location import GeoCoords

from basic_request import simple_get
from google_api import get_rough_address_from_lat_long

#pylint: disable=too-few-public-methods
class RightmoveProperty(object):
    """
    Right move property details
    """
    url = ""
    ad_address = ""
    geo_coords = None
    rough_address = None
    def __init__(self, url, ad_address, geo_coords):
        self.url = url
        self.ad_address = ad_address
        self.geo_coords = geo_coords

    def output(self):
        """
        Output information about the property
        """
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
    ad_address = soup.find(itemprop='streetAddress')['content']
    geo_coords = get_lat_long(soup)
    rm_property = RightmoveProperty(url, ad_address, geo_coords)
    rough_address = get_rough_address_from_lat_long(rm_property.geo_coords.latitude,
                                                    rm_property.geo_coords.longitude,
                                                    rm_property.ad_address)
    rm_property.rough_address = rough_address
    return rm_property
