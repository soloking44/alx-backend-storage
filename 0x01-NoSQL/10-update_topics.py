#!/usr/bin/env python3
"""
Replace school topic
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Modify several rows
    """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
