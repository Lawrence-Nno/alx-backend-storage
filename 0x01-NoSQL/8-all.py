#!/usr/bin/env python3
""" A python function that list all documents in a Collection """
import pymongo


def list_all(mongo_collection):
    """ lists all documents in a collection """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
