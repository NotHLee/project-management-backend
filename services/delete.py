"""
delete.py
Removes entry/entries from the database as needed.
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
from validation import *

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def delete_one(tableName: str, id: ObjectId):
    """
    delete_one deletes an entry from a given table with the matching id.

    Inputs -
        tableName:  A string representing the table name to delete from
        id:         An ObjectId representing the object id of the item to be deleted

    Returns -
        Returns an int, 200 when deletion succeded, 404 if the entry could not be found.
    """
    table = db[tableName]
    query = {"_id": ObjectId(id)}
    result = table.delete_one(query)
    if result.deleted_count != 0:
        return 200
    else:
        return 404
    
    
def delete_sprint(sprint_id: ObjectId):
    """
    delete_sprint deletes a sprint entry from the 'sprints' table with the matching id.
    Before deletion, it sets the sprint attribute to None for all tasks that are assigned to this sprint.
    
    Inputs -
        sprint_id: An ObjectId representing the id of the sprint to be deleted.

    Returns -
        Returns an int, 200 when deletion succeeded, 404 if the entry could not be found.
    """
    # # Verify if the sprint exists before attempting to delete
    if not sprint_existence_verification.verify_existing_sprints(sprint_id):
        return 404  # Sprint does not exist

    sprint = db["sprints"].find_one({"_id": sprint_id})
    if not sprint:
        return 404, "Sprint not found"
    
    # Access the list of tasks directly from the sprint object
    task_ids = sprint.get("tasks", [])  # Assuming 'tasks' is a list of task IDs

    change_counter = 0
    task_counter = 0

    # Update each task to set 'sprint' field to None
    for task_id in task_ids:
        # Use the correct collection name: "tasks"
        task_data = db["tasks"].find_one({"_id": ObjectId(task_id)})
        
        if task_data:
            task_counter += 1
            # Update the sprint field to None
            db["tasks"].update_one({"_id": ObjectId(task_id)}, {"$set": {"sprint": None}})
            
            # Fetch the updated task to verify
            updated_task_data = db["tasks"].find_one({"_id": ObjectId(task_id)})
            
            if updated_task_data.get("sprint") is None:
                change_counter += 1

    print(f"Tasks processed: {task_counter}, Tasks successfully updated: {change_counter}")
    
    if change_counter != task_counter:
        return 400, "Some tasks were not updated successfully"
    
    # Proceed with deleting the sprint
    return delete_one("sprints", sprint_id)

# Example call to test the function
#delete_sprint(ObjectId("66fbf1064697b9d535edd268"))
