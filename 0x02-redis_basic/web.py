#!/usr/bin/env python3
""" Implementing a funcion that obtains the HTML content of...
    ...a particular URL and returns it """
import redis
import requests
r = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """ This func tracks how many times a particular URL was accessed...
        and caches the result with an expiration time of 10 secs """
    r.set(f"cached:{url}", count)
    resp = requests.get(url)
    r.incr(f"count:{url}")
    r.setex(f"cached:{url}", 10, r.get(f"cached:{url}"))
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
