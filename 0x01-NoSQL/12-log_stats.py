#!/usr/bin/env python3
'''rovides some stats about Nginx
logs stored in MongoDB
'''
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs.nginx

    num_logs = db.count_documents({})
    print(f"{num_logs} logs")

    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(db.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_count))

    status = db.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status} status check")
