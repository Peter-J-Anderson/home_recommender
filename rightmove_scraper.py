#!/usr/bin/env pythoni
import logging
from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from itertools import imap

class Post(object):
    image_url = ""
    url = ""
    full_desc = ""
    title = ""
    post_id = ""
    location = ""
    date = ""

    def __init__(self, url, title, post_id, location, date, full_desc, image_url):
        self.url = url
        self.title = title
        self.post_id = post_id
        self.location = location
        self.date = date
        self.full_desc = full_desc
        self.image_url = image_url



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

def get_post_date(html):
    """
    get the date value from a given offer
    """
    if html is None: 
        raise Exception('html cannot be null')
    
    date = ""
    post_details_divs = html.find(id='post_details').find_all('div')
    if len(post_details_divs) == 1:
        date = post_details_divs[0].text.strip("Date : ")

    if len(post_details_divs) == 2:
        date = post_details_divs[1].text.strip("Date : ")

    return date

def get_post_image_url(html):
    if html is None:
        raise Exception('html cannot be null')
    image_element = html.find(id='post_thumbnail')
    image_url = "NO IMAGE"
    if image_element is not None:
        image_url = image_element['src']

    return image_url
    

def get_offer(url):
    """
    Get the full description for a given post
    """
    response = simple_get(url)
    if response is None:
        raise Exception('Error retrieving content at {}'.format(url))
    html = BeautifulSoup(response, 'html.parser')
    post_id = html.find(id='group_post').find('header').find_all('h2')[0].text.replace("Post ID: ", "")
    title = getattr(html.find(id="group_post").find('header').find_all('h2')[1], 'text', '').replace("OFFER: ", "")
    location = html.find(id='post_details').find_all('div')[0].text.replace("Location :", "")
    date = get_post_date(html) 
    full_desc = html.find(id='group_post').find("p").text.lower()   
    image_element = html.find(id='post_thumbnail')
    image_url = get_post_image_url(html)
    offer = Post(url, title, post_id, location, date, full_desc, image_url)
    return offer

def get_offers(url):
    """
    Get all offers on the page
    """
    response = simple_get(url)
    if response is None:
        raise Exception('Error retrieving content at {}'.format(url))
    html = BeautifulSoup(response, 'html.parser')
    offers = set()
    for tr in html.select('tr'):
        tds =  tr.select('td')
        if 'OFFER' in tds[0].text:
            for td in tr.select('td')[1:2]:
                href = td.a['href']
		short_desc = td.a.text
                offer = get_offer(href)
                offers.add(offer)
    return offers


#logging.basicConfig(filename='output.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
boards = [
    'https://groups.freecycle.org/group/BordonAltonPetersfieldUK/posts/offer',
    'https://groups.freecycle.org/group/Farnborough_AldershotUK/posts/offer',
    'https://groups.freecycle.org/group/godalmingUK/posts/offer',
    'https://groups.freecycle.org/group/GosportUK/posts/offer',
    'https://groups.freecycle.org/group/GuildfordUK/posts/offer',
    'https://groups.freecycle.org/group/HavantUK/posts/offer',
    'https://groups.freecycle.org/group/PortsmouthUK/posts/offer',
    'https://groups.freecycle.org/group/Farnham/posts/offer',
    'https://groups.freecycle.org/group/FarehamUK/posts/offer',
    'https://groups.freecycle.org/group/WokingUK/posts/offer']

keywords = ['printer','drill','tool','dewalt', 'saw', 'driver','router', 'hub', 'computer']


for board in boards:
    print("###############################################################")
    print("###############################################################")
    print(board)
    print("###############################################################")
    print("###############################################################")
    offers = get_offers('{}?resultsperpage=100'.format(board))
    for offer in offers:
        if any(imap(offer.full_desc.__contains__, keywords) or imap(offer.short_desc.__contains__, keywords)):
            print(offer.title)
            print(offer.post_id)
            print(offer.location)
            print(offer.date)
            print(offer.image_url)
            print(offer.full_desc)
            print(offer.url)
            print('---------------------------------------')
