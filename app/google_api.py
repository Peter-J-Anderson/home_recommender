#!/usr/bin/env python
"""
Module for interacting with the google apis
"""

from __future__ import print_function
import json
import os
from basic_request import simple_get

class PropertyRoughAddress(object):
    """
    Class for holding the rough address of a property
    """
    street_name = ""
    postal_town = ""
    county = ""
    country = ""
    postal_code = ""

    #pylint: disable-msg=too-many-arguments
    def __init__(self, street_name, postal_town, county,
                 country, postal_code):
        self.street_name = street_name
        self.postal_town = postal_town
        self.county = county
        self.country = country
        self.postal_code = postal_code

    def output(self):
        """
        Output the class details to the console for debugging
        """
        print("{}".format(self.street_name))
        print("{}".format(self.postal_code))
        print("{}".format(self.county))

    @staticmethod
    def get_property_rough_address(address_components):
        """
        Convert address compoents for a PropertyRoughAddress
        """
        street_name = [
            part for part in address_components if 'route' in part['types']
        ][0]['long_name']

        postal_town = [
            part for part in address_components if 'postal_town' in part['types']
        ][0]['long_name']

        county = [
            part for part in address_components if 'administrative_area_level_2' in part['types']
        ][0]['long_name']

        country = [
            part for part in address_components if 'country' in part['types']
        ][0]['long_name']

        postal_code = [
            part for part in address_components if 'postal_code' in part['types']
        ][0]['long_name']

        rough_address = PropertyRoughAddress(street_name, postal_town, county, country, postal_code)
        return rough_address

def get_rough_address_from_lat_long(latitude, longitude, scraped_address):
    """
    Helper function to get the rough address from a lat+long and street name address
    """
    geoencoding_api_key = os.environ['GOOGLE_MAPS_API_KEY']
    geoencoding_base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geoencoding_url = "{}?latlng={},{}&key={}".format(
        geoencoding_base_url, latitude, longitude, geoencoding_api_key)

    json_data = simple_get(geoencoding_url)
    data = json.loads(json_data)
    matching_address = find_best_match_address(data, scraped_address)
    return matching_address


def find_best_match_address(data, partial_address):
    """
    Find the best matching address from the list of addresses
    returned by good
    """
    google_premis_address = None
    addresses = data['results']
    for address in addresses:
        address_parts = address['address_components']
        for address_part in address_parts:
            if 'route' in address_part['types']:
                route = address_part['long_name']
                break

        if route in partial_address:
            google_premis_address = address
            break

    if google_premis_address is None:
        return None

    address_components = google_premis_address['address_components']
    property_rough_address = PropertyRoughAddress.get_property_rough_address(address_components)
    return property_rough_address

def get_travel_time(from_location, to_location):
    """
    Helper fuctino to get travel time between two locations using the google api
    """
    google_maps_api_key = os.environ['GOOGLE_MAPS_API_KEY']
    distance_matrix_base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    distance_matrix_url = "{}?units=imperial&origins={}&destinations={}&key={}".format(
        distance_matrix_base_url, from_location, to_location, google_maps_api_key)
    json_data = simple_get(distance_matrix_url)
    data = json.loads(json_data)
    travel_time = data["rows"][0]["elements"][0]["duration"]["text"]
    return travel_time
