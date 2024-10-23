#!/usr/bin/env python3
"""
Module that initializes the Redis client and provides caching functionality
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the call count for the method's qualified name in Redis
        key = f"{method.__qualname__}"
        self._redis.incr(key)  # Increment the call count
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments as a string in Redis
        self._redis.rpush(input_key, str(args))

        # Call the original method and get the result
        result = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable):
    """
    Display the history of inputs and outputs for a method.
    """
    redis_client = method.__self__._redis
    key = method.__qualname__

    inputs = redis_client.lrange(f"{key}:inputs", 0, -1)
    outputs = redis_client.lrange(f"{key}:outputs", 0, -1)

    print(f"{key} was called {len(inputs)} times:")

    for input_data, output_data in zip(inputs, outputs):
        # Decode input and output data for display
        input_data = input_data.decode('utf-8')
        output_data = output_data.decode('utf-8')
        print(f"{key}(*{input_data}) -> {output_data}")


class Cache:
    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()  # Connect to Redis server
        self._redis.flushdb()  # Clear the database

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key and return the key.
        """
        key = str(uuid.uuid4())  # Generate a unique UUID as the key
        self._redis.set(key, data)  # Store the data in Redis
        return key  # Return the generated key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Responsible for retrieving data from Redis and apply an
        optional conversion function
        """
        value = self._redis.get(key)  # Get the value from Redis
        if value and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve a string value from Redis.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer value from Redis.
        """
        return self.get(key, int)
