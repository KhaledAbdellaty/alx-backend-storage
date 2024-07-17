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

def call_history(method: Callable) -> Callable:
    """A call_history decorator to store the history
    of inputs and outputs for a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Execute the wrapped function to retrieve the output.
        Store the output using rpush"""
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        data = str(args)
        self._redis.rpush(input_key, data)
        fn = method(self, *args, **kwds)
        self._redis.rpush(output_key, str(fn))
        return fn
    return wrapper

def replay(func: Callable):
    """A function to display the history of calls
    of a particular function."""
    redis_store = getattr(func.__self__, '_redis', None)
    func_name = func.__qualname__
    inp_m = redis_store.lrange("{}:inputs".format(func_name), 0, -1)
    outp_m = redis_store.lrange("{}:outputs".format(func_name), 0, -1)
    calls_count = len(inp_m)
    times_str = 'times'
    if calls_count == 1:
        times_str = 'time'
    fin = '{} was called {} {}:'.format(func_name, calls_count, times_str)
    print(fin)
    for k, v in zip(inp_m, outp_m):
        fin = '{}(*{}) -> {}'.format(
            func_name, k.decode('utf-8'), v.decode('utf-8'))
        print(fin)

class Cache:
    """Represents an object for storing data
    in a Redis data storage."""
    def __init__(self):
        """Store an instance of the Redis client
        as a private variable named _redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
