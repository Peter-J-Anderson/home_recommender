#!/usr/bin/env python
"""
Holds location geo coord object
"""
#pylint: disable=too-few-public-methods
class GeoCoords(object):
    """
    Location object
    """
    latitude = ""
    longitude = ""

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
