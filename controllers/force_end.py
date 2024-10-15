"""
force_end.py
Contains the helper function to forcefully end a sprint.
"""
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
tasks = client[db_name]["tasks"]
sprints = client[db_name]["sprints"]

def force_end(sprintID: str) -> tuple[int, str | dict]:
    """
    force_end is the helper function to forcefully end a sprint by its id

    Inputs:
        sprintID - The ID of the sprint to end.

    Returns:
        If an error occurs, it returns a tuple with an error status code, along with a string describing the error
        Else, it returns a 200 status code and the entry of the sprint that ended in the form of a dictionary.
    """
    sprint: dict = sprints.find_one({"_id": ObjectId(sprintID)})
    print(sprint)

    # Check if the ID correlates to a sprint
    if sprint == None:
        return 404, f"Sprint does not exist."
    elif sprint["status"] == "Not Started" or sprint["status"] == "Not Started":
        return 400, f"Sprint is not active."

    sprintTasks: list[str] = sprint["tasks"]
    print(sprintTasks)

    i = 0
    while i < len(sprintTasks):
        task = tasks.find_one({"_id": ObjectId(sprintTasks[i])})
        if task["status"] != "Completed":
            tasks.update_one({"_id": ObjectId(sprintTasks[i])}, {"$set": {"sprint": None}})
            sprintTasks.pop(i)
            i -= 1
        i += 1

    updates = {
        "endDate": datetime.now(),
        "status": "Completed",
        "tasks": sprintTasks
    }
    print(updates)

    result = sprints.update_one({"_id": ObjectId(sprintID)}, {"$set":updates})
    sprint = sprints.find_one({"_id": ObjectId(sprintID)})

    if result.modified_count > 0:
        return 200, sprint
    else:
        return 500, f"Force end unsuccessful, no fields are modified."