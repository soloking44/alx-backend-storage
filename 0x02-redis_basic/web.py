#!/usr/bin/env python3
"""
A module with tools for caching HTTP requests and tracking access counts.
"""

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis connection
r = redis.Redis()

def count_requests(method: Callable[[str], str]) -> Callable[[str], str]:
    """Decorator that counts the number of requests to a URL and caches the response.
    
    Args:
        method (Callable[[str], str]): The method to be decorated.
    
    Returns:
        Callable[[str], str]: The decorated method.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function that implements the caching and counting logic.
        
        Args:
            url (str): The URL to fetch.
        
        Returns:
            str: The content of the URL.
        """
        # Increment the request count
        r.incr(f"count:{url}")
        
        # Check if the URL content is already cached
        cached_html = r.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        
        # Fetch the content and cache it
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return wrapper

@count_requests
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL.
    
    Args:
        url (str): The URL to fetch.
    
    Returns:
        str: The HTML content of the URL.
    """
    req = requests.get(url)
    return req.text

if __name__ == "__main__":
    # Example usage
    url = "http://google.com"
    content = get_page(url)
    print(content)
