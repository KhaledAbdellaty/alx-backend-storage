#!/usr/bin/env python3
"""A Cache class"""
import redis
import uuid


class Cache:
    """Represents an object for storing data
    in a Redis data storage."""
    def __init__(self):
        """Store an instance of the Redis client
        as a private variable named _redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """A function that generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and
        return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
