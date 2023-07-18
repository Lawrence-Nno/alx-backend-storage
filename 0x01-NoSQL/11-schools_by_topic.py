#!/usr/bin/env python3
"""A Python func that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """ Returns list of schools """
    return mongo_collection.find({ "topics": topic })
