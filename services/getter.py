"""
getter.py
Gets tables/entries from the database as needed.
"""
from pymongo import MongoClient
from datetime import datetime

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def get_all(tableName: str):
    """
    get_all returns a table with the given table name

    Inputs -
        tableName:  A string representing the table name to get from

    Returns -
        Returns a list of entries from the given table.
    """
    table = list(db[tableName].find())
    for task in table:
        task['_id'] = str(task['_id'])
    return table

def get_query(tableName: str, query: dict):
    """

    """
    table = list(db[tableName].find(query))
    return table

def get_one_query(tableName: str, query: dict):
    """

    """
    item = db[tableName].find_one(query)
    return item

def get_tasks_for_member(member_id: str):
    """
    Helper function to retrieve tasks assigned to a specific member.
    :param member_id: The ID of the member.
    :return: A list of tasks assigned to the member.
    """
    tasks_collection = db["tasks"]  # Assuming you have a 'tasks' collection
    
    # Find tasks where the assignee matches the member_id
    tasks_cursor = tasks_collection.find({"assignee": member_id})
    
    # Convert the cursor to a list and prepare the tasks
    task_list = []
    for task in tasks_cursor:
        task["_id"] = str(task["_id"])  # Convert ObjectId to string
        task_list.append(task)

    return task_list

