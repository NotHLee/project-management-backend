from pymongo import MongoClient
from bson.objectid import ObjectId

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def into_sprint(tasks : dict):
    """
    into_sprint moves the task from the product backlog to the sprint backlog
    
    Inputs -
        tasks - A dictionary with the task card details to move the task into the sprint

    Returns -
        Returns an int, 200 when moving task succeded, 404 if the entry could not be found.
    """

    table = db["tasks"]
    sprints = db["sprints"]
    
    for task in tasks:
        update = False
        original_sprint = task["originalSprint"]
        original_sprint_str = str(original_sprint)
        task_id = task["_id"]
        task_id_str = str(task_id)
        sprint_id = task["sprint"]
        sprint_id_str = str(sprint_id)

        if task_id_str != None and sprint_id_str != None:
            if original_sprint_str == sprint_id_str:
                table.update_one({"_id": task_id}, {"$set": {"sprint": sprint_id}})
                # current_sprint = sprints.find_one({"_id": sprint_id})
                sprints.update_one({"_id": sprint_id}, {"$push": {"tasks": task_id}})              
                update = True
                print("task_id_str and sprint_id_str")
            else:
                table.update_one({"_id": task_id}, {"$set": {"sprint": None}})
                sprints.update_one({"_id": sprint_id}, {"$pull": {"tasks": task_id}})
                update = True
                print("No task_id_str and sprint_id_str")
                
        if update == False:
            return 400, "Failed update"
        else:
            continue
    
    return 200, "Sucess"
    
# def out_of_sprint(tableName: str, sprint: str, id: ObjectId):
#     """
#     out_of_sprint moves the task from the product backlog back to the sprint board
    
#     Inputs -
#         sprintName:  A string representing the sprint name to move from
#         sprint: A string representing whether the task is in a sprint
#         id: An ObjectId representing the object id of the item to be moved

#     Returns -
#         Returns an int, 200 when moving task succeded, 404 if the entry could not be found.
#     """
#     tasks = db[tableName]
#     table = list(sprint.find({"sprint": sprint}))
#     task = tasks.find_one({"_id": id})
#     # table.update_one({"_id": id}, {"$set": {"sprint": sprint}})

#     if task:
#         tasks.update_one({"_id": id}, {"$set": {"sprint": sprint}})
#         return 200, table
#     else:
#         return 400, "This task is not found in the sprint"