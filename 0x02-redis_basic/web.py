#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""

import redis
import requests
from datetime import timedelta
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis connection configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 127001
REDIS_DB = 0
CACHE_TTL = 10  # Cache time-to-live in seconds

# Connect to Redis
redis_store = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_page(url: str) -> Optional[str]:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request.

    Args:
        url (str): The URL to fetch.

    Returns:
        Optional[str]: The content of the URL or None if an error occurs.
    """
    if not url:
        logger.warning("Invalid URL provided.")
        return None

    res_key = f'result:{url}'
    req_key = f'count:{url}'

    try:
        # Check cache
        result = redis_store.get(res_key)
        if result is not None:
            redis_store.incr(req_key)
            logger.info(f"Cache hit for URL: {url}")
            return result.decode('utf-8')

        # Make HTTP request
        response = requests.get(url)
        response.raise_for_status()
        result = response.content.decode('utf-8')

        # Cache the result
        redis_store.setex(res_key, timedelta(seconds=CACHE_TTL), result)
        redis_store.incr(req_key)
        logger.info(f"Cache miss for URL: {url}. Content fetched and cached.")
        return result
    except requests.RequestException as e:
        logger.error(f"Error fetching URL: {url} - {e}")
        return None
    except redis.RedisError as e:
        logger.error(f"Error interacting with Redis: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    url = "http://example.com"
    content = get_page(url)
    if content:
        print(content)
    else:
        print("Failed to retrieve the content.")
