#!/usr/bin/env python3
"""
Function for getting list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
     returns list of school having a specific topic(s)

    :param mongo_collection
    :param topic
    :return: []
    """
    return mongo_collection.find({"topics": topic})
