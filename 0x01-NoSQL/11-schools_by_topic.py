#!/usr/bin/env python3
"""
Checks for topic
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Checks for topic
    """
    return mongo_collection.find({"topics": topic})
