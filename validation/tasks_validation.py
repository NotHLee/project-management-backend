from datetime import datetime
from bson.objectid import ObjectId
from services import getter
from pymongo import MongoClient

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]
members = db["members"]
sprints = db["sprints"]

def validate_task_data(data: dict) -> str | bool:
    """
    Validates the incoming task data to ensure it conforms to the required attributes.

    Parameters:
    - data (dict): The task data to validate.

    Returns:
    - True if the data is valid.
    - A string containing the validation error message if the data is invalid.
    """

    # Write the required attributes and their expected types
    requiredFields = {
        "taskName": str,
        "storyType": str,
        "storyPoints": int,
        "tags": list,
        "priority": str,
        "assignee": str,
        "status": str,
        "description": str,
        "progress": str
    }

    # Write the valid options for each variable
    validPriorities = ["Low", "Medium", "Important", "Urgent"]
    validTypes = ["Bug", "Story"]
    validStatuses = ["Not Started", "In Progress", "Complete"]
    validProgresses = ["Planning", "Development", "Testing", "Integration"]

    # Check for missing fields and incorrect types
    for field, field_type in requiredFields.items():
        if field not in data:
            return f"Missing required field: {field}"
        if not isinstance(data[field], field_type):
            return f"Incorrect type for field '{field} - {type(data[field]).__name__}'."

    # Check for extra fields
    for field, _ in data.items():
        if field not in requiredFields:
            return f"Unknown field created: {field}."

    # Check for tags types
    for tag in data["tags"]:
        if not isinstance(tag, str):
            return f"Incorrect data type for tag '{tag} - {type(tag).__name__}'."

    # Check every specific fields for correct values
    if data["priority"] not in validPriorities:
        return f"Invalid priority value: {data['priority']}."
    if data["storyType"] not in validTypes:
         return f"Invalid type value: {data['type']}."
    if data["status"] not in validStatuses:
        return f"Invalid status value: {data['status']}."
    if data["progress"] not in validProgresses:
        return f"Invalid progress value: {data['progress']}."
    if data["storyPoints"] > 10 or data["storyPoints"] < 1:
        return f"Invalid story points value: {data['storyPoints']}."
    if members.find_one(ObjectId(data["assignee"])) == False:
        return f"Assignee Member ID doesn't exist. {ObjectId(data['assignee'])}"

    # Return True if validation passes
    return True

def validate_modified_data(id: str, data: dict) -> str | bool:
    """
    Validates data in tasks to be modified to ensure it conforms to the required attributes and data types.

    Parameters:
    - id (str): The id of the task to modify.
    - data (dict): The modified data to validate.

    Returns:
    - True if the modification is valid.
    - A string containing the validation error message if the modification is invalid.
    """
    modifyingTask = getter.get_one_query("tasks", {"_id": ObjectId(id)})
    if modifyingTask == None:
        return f"Task with id: {id} does not exist."
    elif modifyingTask["status"] == "Completed":
        return f"Completed tasks cannot be modified."

    validFields = {
        "taskName": str,
        "storyType": str,
        "storyPoints": int,
        "tags": list,
        "priority": str,
        "assignee": str,
        "status": str,
        "description": str,
        "progress": str,
        "creationDate": datetime,
        "completionDate": datetime,
        "sprint": str,
        "logs": list,
        "history": list
    }

    # Write the valid options for each variable
    validPriorities = ["Low", "Medium", "Important", "Urgent"]
    validTypes = ["Bug", "Story"]
    validStatuses = ["Not Started", "In Progress", "Complete"]
    validProgresses = ["Planning", "Development", "Testing", "Integration"]

    # Checking if the modified field is valid, and has the correct data type.
    for field, item in data.items():
        if field not in validFields:
            return f"Modified data contains a field that is not modifiable/doesn't exist: {field}"
        if not isinstance(item, validFields[field]):
            return f"Modified data does not adhere to the correct field type: '{field} - {type(item).__name__}'"


    # Check specific existing fields for correct values
    if "priority" in data:
        if data["priority"] not in validPriorities:
            return f"Invalid priority value: {data['priority']}."
    if "storyType" in data:
        if data["storyType"] not in validTypes:
            return f"Invalid type value: {data['type']}."
    if "status" in data:
        if data["status"] not in validStatuses:
            return f"Invalid status value: {data['status']}."
    if "progress" in data:
        if data["progress"] not in validProgresses:
            return f"Invalid progress value: {data['progress']}."
    if "storyPoints" in data:
        if data["storyPoints"] > 10 or data["storyPoints"] < 1:
            return f"Invalid story points value: {data['storyPoints']}."
    if "assignee" in data:
        if members.find_one(ObjectId(data["assignee"])) != None:
            return f"Assignee Member ID doesn't exist."
    if "sprint" in data:
        if sprints.find_one(ObjectId(data["sprint"])) != None:
            return f"Sprint ID doesn't exist."

    # Return True if all items are validated.
    return True