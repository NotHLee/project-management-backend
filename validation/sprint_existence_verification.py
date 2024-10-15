"""
validation.py
Contains functions for validating data.
"""
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def verify_existing_sprints(sprint_id: ObjectId) -> bool:
    """
    verify_sprint_exists checks if a sprint exists in the database.

    Inputs -
        sprint_id: An ObjectId representing the id of the sprint to check.

    Returns -
        True if the sprint exists, False otherwise.
    """
    sprint = db["sprints"].find_one({"_id": sprint_id})
    return sprint is not None  
