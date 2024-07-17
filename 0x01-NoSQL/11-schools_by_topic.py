#!/usr/bin/env python3
"""returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """A function that returns the list of
    school having a specific topic:"""
    documents = mongo_collection.find({
        "topics": {
            "$eleMatch": {
                "$eq": topic
            }
        }
    })
    return documents
