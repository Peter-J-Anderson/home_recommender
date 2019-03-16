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
#houses = ['https://www.rightmove.co.uk/property-for-sale/property-58097316.html']
houses = ['https://www.rightmove.co.uk/property-for-sale/property-75778964.html']

for house in houses:
    prices_paid = None
    mobile_coverage = None
    rm_property = get_rightmove_property(house)
    if (rm_property.rough_address is not None):
        prices_paid = get_additional_prices_paid(rm_property.rough_address.street_name, rm_property.rough_address.postal_town) 
        mobile_coverage = get_mobile_coverage(rm_property.rough_address.postal_code)

    crime_stats = get_crime_stats(float(rm_property.geo_coords.latitude), float(rm_property.geo_coords.longitude))
    

    rm_property.output()
    
    #print(prices_paid)
    for price in prices_paid:
        price.output()

    #print(crime_stats)
    for stat in crime_stats:
        stat.output()
    #print(mobile_coverage)

    output_mobile_coverage(mobile_coverage)
    
    



