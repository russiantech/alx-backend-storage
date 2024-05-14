#!/usr/bin/env python3
"""
Changes * topics of a `school` document based on the name
Prototype: def update_topics(mongo_collection, name, topics):
mongo_collection will be the pymongo object
name will be the school name to update as a str
topics will be the list of topics(str) approached in the school
"""


def update_topics(mongo_collection, name, topics):
    """
    Prototype: def update_topics(mongo_collection, name, topics):
    Changes * topics of a school document
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
