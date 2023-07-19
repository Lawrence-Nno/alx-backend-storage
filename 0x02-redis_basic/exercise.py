#!/usr/bin/env python3
""" Module for Redis database."""
import redis
import uuid
from functools import wraps
from sys import byteorder
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """ Method that counts num of times cache class are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **keywords):
        """ A wrapper func for call_calls method """
        self._redis.incr(key)
        return method(self, *args, **keywords)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Stores a particular func's history of input and outputs """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args):
        """ A wrapper function for call_history method """
        self._redis.rpush("{}:inputs".format(key), str(args))
        history = method(self, *args)
        self._redis.rpush("{}:outputs".format(key),
                          str(history))
        return history
    return wrapper


def replay(method: Callable):
    """ Displays the history of calls of a particular function """
    r = method.__self__._redis
    keys = method.__qualname__
    inputs = r.lrange("{}:inputs".format(keys), 0, -1)
    outputs = r.lrange("{}:outputs".format(keys), 0, -1)
    print("{} was called {} times:".format(keys,
                                           r.get(keys).decode("utf-8")))
    for i, j in list(zip(inputs, outputs)):
        print("{}(*{}) -> {}".format(keys, i.decode("utf-8"),
                                     j.decode("utf-8")))


class Cache:
    """ Class for methods that operate a caching system """
    def __init__(self):
        """ Instance of Redis db"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Method takes a data argument and returns a string
            Generate a random key (e.g. using uuid), store the 
            input data in Redis using the random key and return the key 
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """ This callable will be used to convert
            the data back to the desired format.
            Args:
                key: string type.
                fn: Optional[Callable].
            Return:
                The convert data.
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, data: bytes) -> str:
        """ Method that get a string from bytes.
        """
        return data.decode("utf-8")

    def get_int(self, data: bytes) -> int:
        """ Method that get a int from bytes.
        """
        return int.from_bytes(data, byteorder)
