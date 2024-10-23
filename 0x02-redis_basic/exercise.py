#!/usr/bin/env python3
"""
Module that Initializes the Redis client and flushes the databas
"""


import redis
import uuid
from typing import Union
from typing import Callable, Optional


class Cache:
    def __init__(self):
        """
        Initialize the Redis client and flush the database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    # Increment
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key and return the key
        """
        key = str(uuid.uuid4())  # Generate a random UUID key
        self._redis.set(key, data)  # Store data in Redis
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieve data from Redis and apply an optional conversion function
        """
        value = self._redis.get(key)
        if value and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves a string from Redis
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis
        """
        return self.get(key, int)
