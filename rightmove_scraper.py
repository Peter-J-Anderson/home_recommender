#!/usr/bin/env pythoni
import logging
from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint 

class geo_coords(object):
    latitude = ""
    longitude = ""

    def __init__(self, latitude, longitude):
        self.latitude = latitude 
        self.longitude = longitude

class rightmove_property(object):
    url = ""
    address = ""
    geo_coords = None
    def __init__(self, url, address, geo_coords):
        self.url = url
        self.address = address
        self.geo_coords = geo_coords

def simple_get(url):
    """
    Attempts to get the content at 'url' by making a HTTP GET request. 
    If the content-type of response is some kind of HTML/XML, return the 
    text content, otherwise return None. 
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during request to {0} : {1}'.format(url,str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors
    This function just prints them, but you can 
    make it do anything.
    """
    print(e)

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

def get_street_name(rightmove_property):
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
    print(request_url)
    response = simple_get(request_url)
    return response

def get_additional_prices_paid(street_name, town):
    """
    hit landregistry to see what prices houses sold for in the same area (road)
    """
    url_template = 'http://landregistry.data.gov.uk/app/ppd/ppd_data.csv?et%5B%5D=lrcommon%3Afreehold&et%5B%5D=lrcommon%3Aleasehold&limit=all&min_date=1+June+2000&nb%5B%5D=true&nb%5B%5D=false&ptype%5B%5D=lrcommon%3Adetached&ptype%5B%5D=lrcommon%3Asemi-detached&ptype%5B%5D=lrcommon%3Aterraced&street={street}&tc%5B%5D=ppd%3AstandardPricePaidTransaction&tc%5B%5D=ppd%3AadditionalPricePaidTransaction&town={town}'
    url = url_template.replace('{town}', town)
    url = url.replace('{street}', street_name.replace(' ', '+'))
    print(url)

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
    street_name = get_street_name(rm_property)
    get_additional_prices_paid(street_name, 'bordon') 
    return rm_property



#logging.basicConfig(filename='output.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
houses = ['https://www.rightmove.co.uk/property-for-sale/property-73000526.html']

for house in houses:
    rm_property = get_rightmove_property(house)
    get_crime_stats(float(rm_property.geo_coords.latitude), float(rm_property.geo_coords.longitude))
    rm_property.geo_coords.latitude

