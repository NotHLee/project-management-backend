from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def modify_task(task_id: str, new_task: dict, member_id: str):
    """
    modify_task updates a task in the tasks table in the database
    """
    table_tasks = db["tasks"]
    members_table = db["members"]

    # remove the _id field from the new_task dictionary
    new_task.pop("_id", None)

    # remove creationDate field from the new_task dictionary
    new_task.pop("creationDate", None)

    # update the task in the tasks table only
    result = table_tasks.update_one({"_id": ObjectId(task_id)}, {"$set": new_task})

    if result.modified_count == 1:
        # find the member from the members table using the id
        member = members_table.find_one({"_id": ObjectId(member_id)})

        # creating the history entry to be added to the tasks history
        history_entry = {
            "description": f"Updated by {member['memberName']}.",
            "date": datetime.now()
        }

        # adding the history entry to the tasks history
        table_tasks.update_one({"_id": ObjectId(task_id)}, {"$push": {"history": history_entry}})

        return 200, "Task updated successfully"
    else:
        return 404, "Task not found"

# task = {
#         "taskName": "Example Task 3",
#         "storyType": "Story",
#         "storyPoints": 9,
#         "tags": ["Backend"],
#         "priority": "Low",
#         "assignee": "670b69d5e0c7c0785a145b68",
#         "status": "Not Started",
#         "description": "Description changed",
#         "progress": "Integration",
#         "creationDate": "10/10/2024",
#         "completionDate": None,
#         "sprint": None,
#         "logs": [],
#         "history": [
#             {
#                "description": "Created by Alice.", 
#                "date": "10/10/2024"
#             }
#         ]
#      }

# status_code = modify_task("670b69d5e0c7c0785a145b6d", task, "670b69d5e0c7c0785a145b67")

# print(f"Status Code: {status_code}")

# updated_tasks = db["tasks"].find_one({"_id": ObjectId("670b69d5e0c7c0785a145b6d")})

# print("Updated Tasks:", updated_tasks) 






