#!/usr/bin/env python3
"""A pythin func that change school topics"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based on the name """
    return mongo_collection.update_many({ "name": name }, { "$set": { "topics": topics } })
