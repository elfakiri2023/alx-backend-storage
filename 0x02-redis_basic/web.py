#!/usr/bin/env python3
""" Requests caching and tracking """

import redis
from typing import Callable
from functools import wraps
import requests

redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """ Caches the output of fetched data """
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """ The wrapper function for caching the output """
        redis_store.incr(f"count:{url}")
        res = redis_store.get(f"cached:{url}")
        if res:
            return res.decode("utf-8")
        html = method(url)
        redis_store.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request.
    """
    return requests.get(url).text