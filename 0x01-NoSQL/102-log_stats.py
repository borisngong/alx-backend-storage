#!/usr/bin/env python3
"""
A script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_logs(mongo_collection):
    """
    Function to display statistics about the Nginx logs stored in MongoDB
    and  count unique IPs and sort by frequency
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

    # IPs
    print("IPs:")
    ip_count = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    for ip in ip_count:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    # Connect to the MongoDB database and collection
    client = MongoClient("mongodb://localhost:27017/")
    db = client.logs
    collection = db.nginx

    nginx_logs(collection)
