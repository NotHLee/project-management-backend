from pymongo import MongoClient
from bson.objectid import ObjectId
from validation.tasks_validation import validate_task_data
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def modify_task_in_sprint(task_id: str, new_task: dict):

    table_tasks = db["tasks"]
    table_sprints = db["sprints"]

    # remove the _id field from the new_task dictionary
    new_task.pop("_id", None)

    # remove creationDate field from the new_task dictionary
    new_task.pop("creationDate", None)

    # remove the logs field from the new_task dictionary
    new_task.pop("logs", None)

    # if new task is modified to complete, set the completionDate as current date
    if new_task["status"] == "Completed":
        new_task["completionDate"] = datetime.now()
    else:
        new_task["completionDate"] = None

    # Find the task with the given id in the tasks table
    prev_task: dict = table_tasks.find_one({"_id": ObjectId(task_id)})

    # compare previous and new sprint id and check are they the same
    is_same_sprint = prev_task["sprint"] == new_task["sprint"]

    # case 1: prev_task and new_task are in the same sprint
    if is_same_sprint:
        # update the task in the tasks table only
        table_tasks.update_one({"_id": ObjectId(task_id)}, {"$set": new_task})

        return 200, "Tasks within the same sprint updated successfully"

    # case 2: prev_task and new_task are in different sprints
    else:

        # check whether it is sprint-to-backlog or sprint-to-sprint
        is_sprint_to_backlog = new_task["sprint"] == None

        # case 2.1: sprint-to-backlog
        if is_sprint_to_backlog:

            # update the task in the tasks table
            table_tasks.update_one({"_id": ObjectId(task_id)}, {"$set": new_task})

            # remove the task from the sprint in the sprints table
            table_sprints.update_one({"_id": ObjectId(prev_task["sprint"])}, {"$pull": {"tasks": task_id}})

            return 200, "Task moved from sprint to backlog successfully"

        # case 2.2: sprint-to-sprint
        else:

            # update the task in the tasks table
            table_tasks.update_one({"_id": ObjectId(task_id)}, {"$set": new_task})

            # remove the task from the previous sprint in the sprints table
            table_sprints.update_one({"_id": ObjectId(prev_task["sprint"])}, {"$pull": {"tasks": task_id}})

            # add the task to the new sprint in the sprints table
            table_sprints.update_one({"_id": ObjectId(new_task["sprint"])}, {"$push": {"tasks": task_id}})

            return 200, "Task moved from one sprint to another successfully"






