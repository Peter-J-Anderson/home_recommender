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

class land_registry_entry:
    transaction_id = ""
    price_paid = ""
    transaction_date = ""
    postcode = ""
    property_type = ""
    new_build = ""
    estate_type = ""
    saon = ""
    paon = ""
    street = ""
    locality = ""
    town = ""
    district = ""
    county = ""
    record_status = ""
    item_url = ""

    def __init__(self, transaction_id, item_url):
        self.transaction_id = transaction_id
        self.item_url = item_url

def get_additional_prices_paid(street_name, town):
    """
    hit landregistry to see what prices houses sold for in the same area (road)
    """
    url_template = 'http://landregistry.data.gov.uk/app/ppd/ppd_data.csv?et%5B%5D=lrcommon%3Afreehold&et%5B%5D=lrcommon%3Aleasehold&limit=all&min_date=1+June+2000&nb%5B%5D=true&nb%5B%5D=false&ptype%5B%5D=lrcommon%3Adetached&ptype%5B%5D=lrcommon%3Asemi-detached&ptype%5B%5D=lrcommon%3Aterraced&street={street}&tc%5B%5D=ppd%3AstandardPricePaidTransaction&tc%5B%5D=ppd%3AadditionalPricePaidTransaction&town={town}'
    lr_url = url_template.replace('{town}', town)
    lr_url = lr_url.replace('{street}', street_name.replace(' ', '+'))
    csv_data = simple_get(lr_url).decode('utf-8')


    transations = list()
    for entry in csv_data.splitlines():
        parts = entry.split(',')
        transaction_id = parts[0]
        item_url = parts[15]
        lr_entry = land_registry_entry(transaction_id, item_url)
        lr_entry.price_paid = parts[1]
        lr_entry.transaction_date = parts[2]
        lr_entry.postcode = parts[3]
        lr_entry.property_type = parts[4]
        lr_entry.new_build = parts[5]
        lr_entry.estate_type = parts[6]
        lr_entry.saon = parts[7]
        lr_entry.paon = parts[8]
        lr_entry.street = parts[9]
        lr_entry.locality = parts[10]
        lr_entry.town = parts[11]
        lr_entry.district = parts[12]
        lr_entry.county = parts[13]
        lr_entry.record_status = parts[14]

        transations.append(lr_entry)

    return transations
