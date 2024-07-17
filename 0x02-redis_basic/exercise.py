#!/usr/bin/env python3
"""A Cache class"""
import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """a count_calls decorator that takes a single
    method Callable argument and returns a Callable"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A function that increments the count
        for that key every time the method."""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """Represents an object for storing data
    in a Redis data storage."""
    def __init__(self):
        """Store an instance of the Redis client
        as a private variable named _redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data):
        """A function that generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and
        return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Get a value from a Redis data storage.'''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Get a value as String from a Redis data storage.'''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Get a value as Int from a Redis data storage.'''
        return self.get(key, lambda x: int(x))
