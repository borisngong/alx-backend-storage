#!/usr/bin/env python3
"""
Module that Initializes the Redis client and flushes the database
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Count the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the call count for the method's qualified name
        key = f"{method.__qualname__}"
        self._redis.incr(key)  # Increment in Redis
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Store the history of inputs and outputs for a function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments as a string
        self._redis.rpush(input_key, str(args))

        # Call the original method and get the result
        result = method(self, *args, **kwargs)

        # Store the output
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
        input_data = input_data.decode('utf-8')
        output_data = output_data.decode('utf-8')
        print(f"{key}(*{input_data}) -> {output_data}")


class Cache:
    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key and return the key.
        """
        key = str(uuid.uuid4())  # Generate a random UUID key
        self._redis.set(key, data)  # Store data in Redis
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieve data from Redis and apply an optional conversion function.
        """
        value = self._redis.get(key)
        if value and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves a string from Redis.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis.
        """
        return self.get(key, int)
