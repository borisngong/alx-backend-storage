#!/usr/bin/env python3
"""
A script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_logs(mongo_collection):
    """
    Provides statistics about the Nginx logs in MongoDB.
    """
    # Total number of logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # HTTP methods and their count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count GET requests to `/status` path
    status_check = mongo_collection.count_documents({
        "method": "GET", "path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    # Connect to the MongoDB database and collection
    client = MongoClient("mongodb://localhost:27017/")
    db = client.logs
    collection = db.nginx

    # Call the function to display statistics
    nginx_logs(collection)
