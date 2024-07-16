#!/usr/bin/env python3
"""
This script have a tool process to show all document
"""
import pymongo


def list_all(mongo_collection):
    """
    Show all collections
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
