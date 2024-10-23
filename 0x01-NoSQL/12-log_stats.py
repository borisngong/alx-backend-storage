#!/usr/bin/env python3
"""
A cript that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_logs(mongo_collection):
    """
    Function responsible is to display statistics about the Nginx logs
    """
    total_logs = mongo_collection.count_documents({})
    print("{} logs".format(total_logs))

    # The Http methods we want to check
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("methods:")
    for method in methods:
        method_count = mongo_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))
    # Count the number of GET requests specifically for the `/status` path
    status_requests = mongo_collection.count_documents({
        "method": "GET", "path": "/status"})
    print("{} status check".format(status_requests))


def app_run():
    """
    Connect to MongoDB and call the function to display Nginx log stats
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    # Access the 'nginx' collection within the 'logs' database
    mongo_collection = client.logs.nginx
    # call function above that prints nginx logs
    nginx_logs(mongo_collection)


if __name__ == '__main__':
    app_run()
