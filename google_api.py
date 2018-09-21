#!/usr/bin/env python
import logging
from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json
import os
from pprint import pprint 
from basic_request import *
from location import *

class property_rough_address(object):
    street_name = ""
    postal_town = ""
    county = ""
    country = ""
    postal_code = ""

    def __init__(self, street_name, postal_town, county, country, postal_code):
        self.street_name = street_name
        self.postal_town = postal_town
        self.county = county
        self.coutry = country
        self.postal_code = postal_code

def get_rough_address_from_lat_long(latitude, longitude, scraped_address):
    geoencoding_api_key = os.environ['GOOGLE_GEOCODING_API_KEY']
    geoencoding_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(latitude, longitude,geoencoding_api_key)
    json_data = simple_get(geoencoding_url)
    data = json.loads(json_data)

    google_premis_address = None

    addresses = data['results']
    for address in addresses:
        address_parts = address['address_components']
        for address_part in address_parts:
            if 'route' in address_part['types']:
                route = address_part['long_name']
    
        if route in scraped_address:
            google_premis_address = address
            break

    address_components = google_premis_address['address_components'] 
    street_name = [part for part in address_components if 'route' in part['types']][0]['long_name'] 
    postal_town = [part for part in address_components if 'postal_town' in part['types']][0]['long_name'] 
    county = [part for part in address_components if 'administrative_area_level_2' in part['types']][0]['long_name']  
    country = [part for part in address_components if 'country' in part['types']][0]['long_name'] 
    postal_code = [part for part in address_components if 'postal_code' in part['types']][0]['long_name'] 
    rough_address = property_rough_address(street_name, postal_town, county, country, postal_code)

    return rough_address
