from pymongo import MongoClient
from bson.objectid import ObjectId

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def move_incompleted_task(id : str):
    tasks = db["tasks"]
    sprints = db["sprints"]

    # find the sprint in the sprint table
    sprint = sprints.find_one({"_id": ObjectId(id)})

    if sprint == None:
        return 400, "Sprint not found."

    print(sprint["tasks"])
    # checking if the task is completed or uncompleted
    for task in sprint["tasks"]:
        task_in_tasks = tasks.find_one({"_id": ObjectId(task)})

        print(task_in_tasks)
        # check if the task is complete
        if task_in_tasks["status"] == "Completed":
            continue

        # check if the task is incomplete
        elif task_in_tasks["status"] == "Not Started" or task_in_tasks["status"] == "In Progress":
            sprints.update_one({"_id": id}, {"$pull": {"tasks": task["_id"]}})
            tasks.update_one({"_id": ObjectId(task["_id"])}, {"$set": {"sprint": None}})
    return 200

# status_code = move_incompleted_task("66fbd4363276cc95904dc69e")

# print(f"Status Code: {status_code}")

# updated_sprint = db["sprints"].find_one({"_id": "66fbd4363276cc95904dc69e"})
# updated_tasks = list(db["tasks"].find({"sprint": None}))

# print("Updated Sprint:", updated_sprint)
# print("Updated Tasks:", updated_tasks) 