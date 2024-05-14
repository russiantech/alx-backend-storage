#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB:
Database: logs
Collection: nginx
"""
from pymongo import MongoClient

def log_stats():
    client = MongoClient()
    collection = client.logs.nginx

    # Total number of documents
    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    # Count documents with each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    # Count documents with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
