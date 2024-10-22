#!/usr/bin/env python3
"""
A script for inserting a document into a MongoDB collection
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document (school) into a MongoDB collection
    """

    insert_new = mongo_collection.insert_one(kwargs)

    return insert_new.inserted_id
