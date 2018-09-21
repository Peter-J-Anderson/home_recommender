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
from rightmove import *
from police import *
from land_registry import *
from samknows_ofcom import *


#logging.basicConfig(filename='output.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
houses = ['https://www.rightmove.co.uk/property-for-sale/property-73000526.html']

for house in houses:
    rm_property = get_rightmove_property(house)
    prices_paid = get_additional_prices_paid(rm_property.rough_address.street_name, rm_property.rough_address.postal_town) 
    crime_stats = get_crime_stats(float(rm_property.geo_coords.latitude), float(rm_property.geo_coords.longitude))
    mobile_coverage = get_mobile_coverage(rm_property.rough_address.postal_code)
    



