#!/usr/bin/env python3
"""
This script implements a cache and tracker function using Redis.
"""

import requests
import redis
import time
from functools import wraps

# Initialize the Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_page(expiration=10):
    """
    Decorator to cache the result of get_page function and track access count.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Check if the URL is in the cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                print("Cache hit")
                redis_client.incr(count_key)
                return cached_result.decode('utf-8')
            
            # Fetch the page and cache it
            print("Cache miss")
            result = func(url)
            redis_client.setex(cache_key, expiration, result)
            redis_client.incr(count_key)
            return result
        
        return wrapper
    return decorator

@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of the given URL.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(test_url))  # First call, should fetch and cache
    time.sleep(1)
    print(get_page(test_url))  # Subsequent call within 10 seconds, should use cache
    time.sleep(11)
    print(get_page(test_url))  # After 11 seconds, should fetch again and cache
