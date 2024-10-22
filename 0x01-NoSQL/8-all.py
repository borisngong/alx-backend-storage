#!/usr/bin/env python3
"""
Module list all documents in a MongoDB collection
"""


def list_all(mongo_collection):
    """
    Function to list all documents in a MongoDB collection
    """
    pym_documents = list(mongo_collection.find())
    if len(pym_documents) == 0:
        return []
    return pym_documents
