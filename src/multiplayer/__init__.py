"""
Currently working on still a work in progress
"""

from . import client
from . import server
import functools

inited = False

def choose_one(func):
    def wrapper(*args, **kwargs):
        global inited
        if inited:
            raise EnvironmentError("Already initiatlzed")
        inited = True
        return func(*args, **kwargs)
    return wrapper

init_server = choose_one(server.init)
init_client = choose_one(client.init)