#!/usr/bin/env python3
""" Redis Module """

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis(host='localhost', port=6379, db=0)


def count_requests(method: Callable) -> Callable:
    """ Decorator for counting """
    @wraps(method)
    def wrapper(url):  
        """ Wrapper for decorator """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        try:
            html = method(url)
            redis_.setex(f"cached:{url}", 10, html.encode('utf-8'))
            return html
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    return wrapper


def get_page_without_cache(url: str) -> str:
    """ Obtain the HTML content of a  URL without caching """
    req = requests.get(url)
    req.raise_for_status()  # Raise an exception for bad status codes
    return req.text


get_page = count_requests(get_page_without_cache)
