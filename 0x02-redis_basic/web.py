#!/usr/bin/env python3
"""
Module that fetches HTML content from a URL and caches the result.
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()

def cache_page(method: Callable) -> Callable:
    """
    Decorator that caches the result of the get_page function.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # Check if the URL result is already cached
        cached_result = redis_client.get(url)
        if cached_result:
            return cached_result.decode('utf-8')

        # If not cached, call the original method
        result = method(url)

        # Cache the result with an expiration time of 10 seconds
        redis_client.setex(url, 10, result)

        # Increment the access count
        redis_client.incr(f"count:{url}")

        return result

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.
    """
    response = requests.get(url)
    return response.text
