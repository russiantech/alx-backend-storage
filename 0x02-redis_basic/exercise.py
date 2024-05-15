#!/usr/bin/env python3
"""
Cache module
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments the call count"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of\
            inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that stores call history"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store inputs
        self._redis.rpush(input_key, str(args))

        # Call the original method and get the result
        result = method(self, *args, **kwargs)

        # Store output
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


def replay(method: Callable):
    """Displays the history of calls of a particular function"""
    r = redis.Redis()
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    input_list = r.lrange(input_key, 0, -1)
    output_list = r.lrange(output_key, 0, -1)

    call_count = len(input_list)
    print(f"{method.__qualname__} was called {call_count} times:")

    for input_data, output_data in zip(input_list, output_list):
        print(f"{method.__qualname__}(*{input_data.decode('utf-8')})\
                -> {output_data.decode('utf-8')}")


class Cache:
    """ Cache class to interact with Redis """

    def __init__(self):
        """ Initialize Redis client and flush the database """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a random key and return the key

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis

        Returns:
            str: The generated key for the stored data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, 
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a transformation function

        Args:
            key (str): The key to look up in Redis
            fn (Optional[Callable]): A function to apply to the data

        Returns:
            Union[str, bytes, int, float, None]:\
                    The retrieved data or None if key does not exist
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis

        Args:
            key (str): The key to look up in Redis

        Returns:
            Optional[str]: The retrieved string or None if key does not exist
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis

        Args:
            key (str): The key to look up in Redis

        Returns:
            Optional[int]: The retrieved integer or None if key does not exist
        """
        return self.get(key, lambda d: int(d))


# Main function for testing the replay functionality
if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    replay(cache.store)
