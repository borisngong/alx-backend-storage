#!/usr/bin/env python3
"""
Module for working with pymongo
"""


def schools_by_topic(mongo_collection, topic):
    """
    Responsible for returning a list of schools having a specific topic
    """
    searched_topic = mongo_collection.find({"topics": topic})
    return list(searched_topic)
