#!/usr/bin/env python3
"""inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """A function that inserts a new document
    in a collection based on kwargs"""
    obj = mongo_collection.insert_one(kwargs)
    return obj.inserted_id
