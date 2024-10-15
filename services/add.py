"""
add.py
Add an entry to the table
"""
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from validation import *

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def add_one(tableName: str, item: dict, memberID: str=None) -> tuple[bool,str]:
    """
    """
    if not isinstance(item, dict):
        return 400, "Invalid input: item must be a dictionary."

    table = db[tableName]
    if tableName == "tasks":

        # conversions and additions of fields
        item["storyPoints"] = int(item["storyPoints"])


        # validate the task data
        check = tasks_validation.validate_task_data(item)
        if check != True:
            return 400, check

        # Get the member name by finding the id from the item["assignee"]
        members_table = db["members"]
        member = members_table.find_one({"_id": ObjectId(memberID)})

        if member is None:
            return 400, f"Assignee with ID {item['assignee']} not found."

        member_name = member["memberName"]

        # Add creation details and history
        item["creationDate"] = datetime.now()
        item["completionDate"] = None
        item["sprint"] = None
        item["logs"] = []
        item["history"] = [{"description": f"Created by {member_name}.", "date": datetime.now()}]

    elif tableName == "sprints":
        item["status"] = "Not Started"
        item["startDate"] = datetime.strptime(item["startDate"],"%d-%m-%Y")
        item["endDate"] = datetime.strptime(item["endDate"],"%d-%m-%Y")
        item["tasks"] = []

        # Validate the sprint data
        check = sprints_validation.validate_sprint_data(item)  # Make sure to implement this validation
        if check != True:
            return 400, check

    elif tableName == "members":
        print("1")
        item["joinDate"] = datetime.now()

        # Validate the member data
        check = members_validation.validate_member_data(item)  # Make sure to implement this validation
        if check != True:
            return 400, check

    # insert the item to the database
    result = table.insert_one(item)


    if result.acknowledged:
        status = 200
        return status, table.find_one({"_id": result.inserted_id})
    else:
        status = 400
        return status, "Database insertion not acknowledged."

