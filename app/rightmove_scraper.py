#!/usr/bin/env python
"""
Script for getting property data based on a Rightmove url
"""
from __future__ import print_function

from samknows_ofcom import get_mobile_coverage, output_mobile_coverage
from rightmove import get_rightmove_property
from police import get_crime_stats
from land_registry import get_additional_prices_paid
from google_api import get_travel_time

from sentry import setup_sentry
setup_sentry()



if __name__ == "__main__":
    PLACES_OF_INTEREST = [{
        "Name": "Peter's Work",
        "Location": "Guildford, UK"
    }, {
        "Name": "Laura's Work",
        "Location": "Havant, UK"
    }]

    HOUSES = ['https://www.rightmove.co.uk/property-for-sale/property-61390665.html']
    PADDING = "-"*6

    for i in range(1, 5):
        print("-----------------------------------------------------------------------")


    for house in HOUSES:
        prices_paid = None
        mobile_coverage = None
        rm_property = get_rightmove_property(house)
        if rm_property.rough_address is not None:
            prices_paid = get_additional_prices_paid(rm_property.rough_address.street_name,
                                                     rm_property.rough_address.postal_town)
            mobile_coverage = get_mobile_coverage(rm_property.rough_address.postal_code)

        crime_stats = get_crime_stats(float(rm_property.geo_coords.latitude),
                                      float(rm_property.geo_coords.longitude))

        print("{} Property Details {}".format(PADDING, PADDING))
        rm_property.output()

        print("{} Distance to places of interest {}".format(PADDING, PADDING))
        from_location = rm_property.rough_address.postal_code
        for poi in PLACES_OF_INTEREST:
            to_location = poi['Location']
            to_location_name = poi['Name']
            travel_time = get_travel_time(from_location, to_location)
            print("{} --> {} : {}".format(from_location.ljust(10),
                                          to_location_name.ljust(10), travel_time))

        #print(prices_paid)
        print("{} Prices Paid {}".format(PADDING, PADDING))
        for price in prices_paid:
            price.output()

        #print(crime_stats)
        print("{} Crime Stats {}".format(PADDING, PADDING))
        for stat in crime_stats:
            stat.output()

        #print(mobile_coverage)
        print("{} Mobile Coverage {}".format(PADDING, PADDING))
        output_mobile_coverage(mobile_coverage)
