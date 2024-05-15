#!/usr/bin/env python3
"""
Web cache and tracker module
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """Decorator to count how many times a URL is requested"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function that increments the request count for a URL"""
        redis_client.incr(f"count:{url}")
        return method(url)
    return wrapper

def cache_result(method: Callable) -> Callable:
    """Decorator to cache the result of a URL request"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function that caches the result of the URL request"""
        cached_result = redis_client.get(url)
        if cached_result:
            return cached_result.decode('utf-8')
        
        result = method(url)
        redis_client.setex(url, 10, result)
        return result
    return wrapper

@count_requests
@cache_result
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL

    Args:
        url (str): The URL to fetch the HTML content from

    Returns:
        str: The HTML content of the URL
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    print(get_page(url))
    print(f"Access count: {redis_client.get(f'count:{url}').decode('utf-8')}")
