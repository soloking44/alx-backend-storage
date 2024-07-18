#!/usr/bin/env python3
"""
this cache and tracker function.
"""

from functools import wraps
import redis
import requests
from typing import Callable
from datetime import timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_HOST = 'localhost'
REDIS_PORT = 127001
REDIS_DB = 0
CACHE_TTL = 10

redis_store = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ shows number of time request count
    is accessed """

    @wraps(method)
    def wrapper(url):
        """ a wrapper decorator process """
        r.incr(f"count:{url}")
        cached_html = r.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """it uses the requests file to get an HTML
    content of a URL and returns it.
    """
    req = requests.get(url)
    return req.text
