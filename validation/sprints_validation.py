from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from services import getter
import bson

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def validate_sprint_data(data: dict) -> str | bool:
    """
    Validates sprints to be added to ensure it conforms to the required attributes and data types.

    Parameters:
    - data (dict): The sprint data to validate.

    Returns:
    - True if the data is valid.
    - A string containing the validation error message if the data is invalid.
    """
    # Required fields for the sprint table
    requiredFields = {
        "sprintName": str,
        "status": str,
        "tasks": list,
        "startDate": datetime,
        "endDate": datetime,
        "totalSprintPoints": int
    }

    # Used for checks in status values
    validStatus = ["Not Started", "In Progress", "Completed"]

    # Checks each item for data type
    for field, fieldType in requiredFields.items():
        if field not in data:
            return f"Missing required field: {field}"
        if not isinstance(data[field], fieldType):
            return f"Incorrect type for field '{field} - {type(data[field]).__name__}'."

    # Checks for extra fields
    for field, _ in data.items():
        if field not in requiredFields:
            return f"Unallowed field created: {field}."

    # Checks for tasks ids to all be strings
    for task in data["tasks"]:
        if not isinstance(task, str):
            return f"Incorrect type for task id '{task} - {type(task).__name__}'"

    # Checking status value
    if data["status"] not in validStatus:
        return f"Invalid status value: {data['status']}."

    # If a sprint trying to activate during creation, check if no other sprints are active.
    if data["status"] == "In Progress":
        item = getter.get_one_query("sprints", {"status": "In Progress"})
        if item != None:
            return f"Cannot activate sprint while there is another sprint active: {str(item['_id'])}"

    # Return true if all items are validated.
    return True

def validate_modified_sprint(id: str, data: dict) -> str | bool:
    """
    Validates data in sprints to be modified to ensure it conforms to the required attributes and data types.

    Parameters:
    - id (str): The id of the sprint to modify.
    - data (dict): The modified data to validate.

    Returns:
    - True if the modification is valid.
    - A string containing the validation error message if the modification is invalid.
    """
    # Checking if the id exists, and is not completed.
    modifyingSprint = getter.get_one_query("sprints", {"_id": ObjectId(id)})
    if modifyingSprint == None:
        return f"Sprint with id: {id} does not exist."
    elif modifyingSprint["status"] == "Completed":
        return f"Completed sprints cannot be modified."

    # Possible modified fields
    validFields = {
        "_id": str,
        "sprintName": str,
        "status": str,
        "tasks": list,
        "startDate": datetime,
        "endDate": datetime,
        "totalSprintPoints" : int
    }

    # Used for checks in status values
    validStatus = ["Not Started", "In Progress", "Completed"]

    # Checking if the modified field is valid, and has the correct data type.
    for field, item in data.items():
        if not isinstance(item, validFields[field]):
            return f"Modified data does not adhere to the correct field type: '{field} - {type(item).__name__}'"

    # If the status is being modified
    if "status" in data:
        # Checking if the status is a valid value
        if data["status"] not in validStatus:
            return f"Invalid status value: {data['status']}."

        # If a sprint trying to activate, check if no other sprints are active.
        if data["status"] == "In Progress":
            activeSprint = getter.get_one_query("sprints", {"status": "In Progress"})
            if activeSprint != None:
                return f"Cannot activate sprint while there is another sprint active: {str(activeSprint['_id'])}"

    # Return True if all items are validated.
    return True



def is_sprint_date_valid(_id: str, start_date: str, end_date: str, force_start: bool) -> bool:
    """
    Validate if the new sprint's startDate and endDate do not overlap with any other active sprints.

    Inputs:
    - start_date: Start date of the new sprint (string in 'DD/MM/YYYY' format).
    - end_date: End date of the new sprint (string in 'DD/MM/YYYY' format).
    - current_sprint_id: Optional, exclude the current sprint (for sprint updates).

    Returns:
    - Boolean: True if no overlap is found, False if there's a conflict.
    """

    # Convert date strings to datetime objects for comparison
    new_start = datetime.strptime(start_date, "%d-%m-%Y") if isinstance(start_date, str) else start_date
    new_end = datetime.strptime(end_date, "%d-%m-%Y") if isinstance(end_date, str) else end_date

    # checks against active sprints only
    if force_start:

        # query to find any active sprints
        active_sprints_count = db["sprints"].count_documents({"status": "In Progress"})

        # if an active sprint exists, disallow the user to force start
        if active_sprints_count > 0:
            return False

    # checks agaisnt all sprints that isn't the current sprint
    else:

        try:
            sprints = db["sprints"].find({"_id": {"$ne": ObjectId(_id)}})
        except bson.errors.InvalidId:
            sprints = db["sprints"].find()

        for sprint in sprints:

            sprint_start = sprint["startDate"]
            sprint_end = sprint["endDate"]

            # case 1: new sprint starts and ends within the current sprint
            if sprint_start < new_start < sprint_end or sprint_start < new_end < sprint_end:
                # If the new sprint starts and ends within the current sprint, there's a conflict
                return False

            # case 2: current sprint starts and ends within the new sprint
            if new_start < sprint_start < new_end or new_start < sprint_end < new_end:
                # If the current sprint starts and ends within the new sprint, there's a conflict
                return False

    # No conflicts found
    return True
