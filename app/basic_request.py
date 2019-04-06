#!/usr/bin/env python
"""
basic request helper module
"""

from __future__ import print_function
from contextlib import closing
from requests import get
from requests.exceptions import RequestException

def simple_get(url):
    """
    Attempts to get the content at 'url' by making a HTTP GET request
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    result = None
    try:
        # pylint: disable=no-member
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                result = resp.content
    except RequestException as exc:
        log_error('Error during request to {0} : {1}'.format(url, str(exc)))
    return result


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise
    """
    content_types = ("html", "json", "csv")
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and any(ct in content_type for ct in content_types))

def log_error(exc):
    """
    It is always a good idea to log errors
    This function just prints them, but you can
    make it do anything
    """
    print(exc)
