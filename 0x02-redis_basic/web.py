#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from datetime import timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis connection configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_TTL = 10  # Cache time-to-live in seconds

# Connect to Redis
redis_store = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    if url is None or len(url.strip()) == 0:
        logger.warning("Invalid URL provided.")
        return ''

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
        setex_response = redis_store.setex(res_key, timedelta(seconds=CACHE_TTL), result)
        if setex_response:
            redis_store.set(req_key, 1)
        else:
            logger.error(f"Failed to set cache for URL: {url}")
        
        logger.info(f"Cache miss for URL: {url}. Content fetched and cached.")
        return result
    except requests.RequestException as e:
        logger.error(f"Error fetching URL: {url} - {e}")
        return ''
    except redis.RedisError as e:
        logger.error(f"Error interacting with Redis: {e}")
        return ''

if __name__ == "__main__":
    # Example usage
    url = "http://google.com"
    content = get_page(url)
    print(content)
