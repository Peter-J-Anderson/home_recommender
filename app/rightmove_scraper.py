#!/usr/bin/env python
from sentry import setup_sentry
setup_sentry()

import logging
import re
import json

from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pprint import pprint 

from basic_request import *
from rightmove import *
from police import *
from land_registry import *
from samknows_ofcom import *


#logging.basicConfig(filename='output.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

places_of_interest = [{
    "Name": "Peter's Work",
    "Location": "Guildford, UK"
},
{
    "Name": "Laura's Work",
    "Location": "Havant, UK"
}]

houses = ['https://www.rightmove.co.uk/property-for-sale/property-75778964.html']
padding = "-"*6

for house in houses:
    prices_paid = None
    mobile_coverage = None
    rm_property = get_rightmove_property(house)
    if (rm_property.rough_address is not None):
        prices_paid = get_additional_prices_paid(rm_property.rough_address.street_name, rm_property.rough_address.postal_town) 
        mobile_coverage = get_mobile_coverage(rm_property.rough_address.postal_code)

    print("{} Distance to places of interest {}").format(padding, padding)
    from_location = rm_property.rough_address.postal_code
    for poi in places_of_interest:
        to_location = poi['Location']
        travel_time = get_travel_time(from_location, to_location)
        print("{} --> {} : {}".format(from_location.ljust(10), to_location.ljust(10), travel_time))

    crime_stats = get_crime_stats(float(rm_property.geo_coords.latitude), float(rm_property.geo_coords.longitude))
    
    print("{} Property Details {}".format(padding, padding))
    rm_property.output()
    
    #print(prices_paid)
    print("{} Prices Paid {}".format(padding, padding))
    for price in prices_paid:
        price.output()

    #print(crime_stats)
    print("{} Crime Stats {}".format(padding, padding))
    for stat in crime_stats:
        stat.output()
    
    #print(mobile_coverage)
    print("{} Mobile Coverage {}".format(padding, padding))
    output_mobile_coverage(mobile_coverage)
    