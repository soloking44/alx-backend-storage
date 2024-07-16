#!/usr/bin/env python3
"""
This script has a tool process to add documents
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Add into school
    """
    return mongo_collection.insert_one(kwargs).inserted_id
