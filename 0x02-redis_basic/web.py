#!/usr/bin/env python3
"""
This script implements a cache and tracker function using Redis.
"""

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize the Redis client
r = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """Decorator to track the number of times a URL is accessed and cache the result."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function to manage caching and request counting."""
        try:
            # Initialize the request count if it doesn't exist
            if not r.exists(f"count:{url}"):
                r.set(f"count:{url}", 0)

            # Increment the request count for the URL
            r.incr(f"count:{url}")
            
            # Check if the URL content is already cached
            cached_html = r.get(f"cached:{url}")
            if cached_html:
                return cached_html.decode('utf-8')
            
            # Fetch the URL content and cache it
            html = method(url)
            response = r.setex(f"cached:{url}", 10, html)
            if not response:
                print("Failed to set cache")
            return html
        except redis.RedisError as e:
            print(f"Redis error: {e}")
            return method(url)
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return ""
        
    return wrapper

@count_requests
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL using requests.
    """
    req = requests.get(url)
    return req.text

if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    
    # Clear previous counts and cache for testing
    r.delete(f"count:{test_url}")
    r.delete(f"cached:{test_url}")

    # First call, should fetch and cache
    print("First call (should fetch):")
    print(get_page(test_url))
    print(f"Count: {r.get(f'count:{test_url}').decode('utf-8')}")  # Should be 1

    # Subsequent call within 10 seconds, should use cache
    print("\nSecond call (should use cache):")
    print(get_page(test_url))
    print(f"Count: {r.get(f'count:{test_url}').decode('utf-8')}")  # Should be 2

    # Wait for cache to expire and call again
    import time
    time.sleep(10)
    print("\nThird call after cache expiration (should fetch again):")
    print(get_page(test_url))
    print(f"Count: {r.get(f'count:{test_url}').decode('utf-8')}")  # Should be 3
