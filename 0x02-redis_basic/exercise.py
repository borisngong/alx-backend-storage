#!/usr/bin/env python3
"""
Module that Initializes the Redis client and flushes the database
"""

import redis
import uuid
from typing import Union


# exercise.py
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key and return the key.
        """
        key = str(uuid.uuid4())  # Generate a random UUID key
        self._redis.set(key, data)  # Store data in Redis
        return key
