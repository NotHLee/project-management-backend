from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from services import getter

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def validate_member_data(data: dict) -> str | bool:
    """
    Validates members to be added to ensure it conforms to the required attributes and data types.

    Parameters:
    - data (dict): The member data to validate.

    Returns:
    - True if the data is valid.
    - A string containing the validation error message if the data is invalid.
    """
    # Required fields for the sprint table
    requiredFields = {
        "memberName": str,
        "password": str,
        "access": str,
        "email": str,
        "joinDate": datetime,
        "securityQuestions": dict | None
    }

    # Used for checks in access values
    validAccess = ["User", "Admin"]

    # Checks each item for data type and missing fields
    for field, fieldType in requiredFields.items():
        if field not in data:
            return f"Missing required field: {field}"
        if not isinstance(data[field], fieldType):
            return f"Incorrect type for field '{field} - {type(data[field]).__name__}'."

    # Checks for extra fields
    for field, _ in data.items():
        if field not in requiredFields:
            return f"Unallowed field created: {field}."

    # Checking access value for correct values
    if data["access"] not in validAccess:
        return f"Invalid access value: {data['access']}."

    # Return true if all items are validated.
    return True

def validate_modified_data(id: str, data: dict) -> str | bool:
    """
    Validates data in members to be modified to ensure it conforms to the required attributes and data types.

    Parameters:
    - id (str): The id of the member to modify.
    - data (dict): The modified data to validate.

    Returns:
    - True if the modification is valid.
    - A string containing the validation error message if the modification is invalid.
    """
    modifyingTask = getter.get_one_query("members", {"_id": ObjectId(id)})
    if modifyingTask == None:
        return f"Member with id: {id} does not exist."

    # Possible modified fields
    validFields = {
        "memberName": str,
        "password": str,
        "access": str,
        "email": str,
        "joinDate": datetime
    }

    # Write the valid options for Access variable
    validAccess = ["User", "Admin"]

    # Checking if the modified field is valid, and has the correct data type.
    for field, item in data.items():
        if field not in validFields:
            return f"Modified data contains a field that is not modifiable/doesn't exist: {field}"
        if not isinstance(item, validFields[field]):
            return f"Modified data does not adhere to the correct field type: '{field} - {type(item).__name__}'"

    # Check specific existing fields for correct values
    if "access" in data:
        if data["access"] not in validAccess:
            return f"Invalid priority value: {data['access']}."

    # Return True if all items are validated.
    return True