from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from validation.sprints_validation import *
#from validation import *  # Assuming you have relevant validation functions

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
tasks_db = client[db_name]["tasks"]
sprints = client[db_name]["sprints"]



def force_start(sprintID: str) -> tuple[int, str | dict]:
    # Check if the sprint exists
    sprint = sprints.find_one({"_id": ObjectId(sprintID)})
    if sprint == None:
        return 404, f"Sprint with id {sprintID} not found."

    # Change status and startDate
    sprintModifications = {
        "status": "In Progress",
        "startDate": datetime.now()
    }

    
    #Check if there are any other sprints active
    result = validate_modified_sprint(sprintID, sprintModifications)
    if result != True:
        return 400, f"Force start failed: {result}"
    
        # Update the sprint with the given modifications
    result = sprints.update_one(
        {"_id": ObjectId(sprintID)},
        {"$set": sprintModifications}
    )
    
    # Now we need to calculate the total story points for the sprint
    tasks = tasks_db.find({"sprint": sprintID})  # Use the tasks_collection reference

    total_story_points = 0
    for task in tasks:
        if "storyPoints" in task and isinstance(task["storyPoints"], (int, float)):
            total_story_points += task["storyPoints"]

    # Update the sprint with the total story points
    sprints.update_one(
        {"_id": ObjectId(sprintID)},
        {"$set": {"totalSprintPoints": total_story_points}}
    )

    sprint = sprints.find_one({"_id": ObjectId(sprintID)})

    # Return the sprint if force start is successful
    if result.modified_count > 0:
        return 200, sprint
    else:
        return 500, f"Force start unsuccessful, no fields are modified."

