#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from functools import wraps
import redis
import requests
from typing import Callable

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
