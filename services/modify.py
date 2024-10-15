from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from validation import *

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def modify(tableName: str, itemID: str, modifications: dict):
    table = db[tableName]

    # Check if tasks is being modified
    if tableName == "tasks":

        # Validating the tasks, with the given ID and task modifications
        check = tasks_validation.validate_modified_data(itemID, modifications)
        if check != True:
            return 400, check

        result = table.update_one({"_id": ObjectId(itemID)}, {"$set": modifications})

        if result.modified_count > 0:

            updatedTask = table.find_one({"_id": ObjectId(itemID)})
            updatedTask["_id"] = str(updatedTask["_id"])
            return 200, updatedTask
        else:
            return 400, "No changes were made to the task."

    elif tableName == 'sprints':
        
        if "startDate" in modifications:
            modifications["startDate"] = datetime.strptime(modifications["startDate"], "%d-%m-%Y")
        if "endDate" in modifications:
            modifications["endDate"] = datetime.strptime(modifications["endDate"], "%d-%m-%Y")

       #Validate the sprint modifications
        check = sprints_validation.validate_modified_sprint(itemID, modifications)
        if check != True:
            return 400, check

        result = table.update_one({"_id": ObjectId(itemID)}, {"$set": modifications})

        if result.modified_count > 0:
            
            updated_sprint = table.find_one({"_id": ObjectId(itemID)})
            updated_sprint["_id"] = str(updated_sprint["_id"])
            if "start_date" in updated_sprint:
                updated_sprint["start_date"] = updated_sprint["start_date"].strftime("%d-%m-%Y")
            if "end_date" in updated_sprint:
                updated_sprint["end_date"] = updated_sprint["end_date"].strftime("%d-%m-%Y")
            return 200, updated_sprint
        else:
            return 400, "No changes were made to the sprint."
        
def add_log_time(memberID, taskID, time_str):
    """
    Logs the time spent by a member on a task.
    
    Args:
        memberID (str): The ID of the member logging time.
        taskID (str): The ID of the task.
        time_str (str): Time spent in 'HH:MM' format.
    
    Returns:
        tuple: Status message and HTTP status code.
    """
    # Query the task using taskID
    tasks_table = db["tasks"]
    task = tasks_table.find_one({"_id": ObjectId(taskID)})

    if not task:
        return ({"error": "Task not found"}), 404

    # Create a new log entry
    log_entry = {
        "member": memberID,
        "date": datetime.now(),
        "hours" : time_str
    }

    # Append the new log entry to the logs array
    tasks_table.update_one(
        {"_id": ObjectId(taskID)},
        {"$push": {"logs": log_entry}}
    )
    
    return True

# Example usage
#print(add_log_time("670cd33423657e3796f4d44d", "670cd583f796d8d31df82e34", "04:48"))
