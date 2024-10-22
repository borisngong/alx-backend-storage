#!/usr/bin/env python3
"""
A module for updating the topics of document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Update the topics of a school document based on the name
    """
    updated_collection = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
        )
    return updated_collection
