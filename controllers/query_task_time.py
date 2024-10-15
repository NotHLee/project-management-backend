"""
task_log_time.py
A controller used specifically to get the total hours worked on a task, with a member filter being optional
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]
members = db["members"]
tasks = db["tasks"]

def get_total_time(taskID: str, memberID:str=None) -> tuple[int, str]:
    """
    get_total_time gets to total log time recorded on a given task, with an optional member filter

    Inputs -
        taskID (string): The queried task ID
        memberID (string): The optionally queried member ID, defaults to None

    Returns -
        404, and an error message if either the provided task or member id is not found
        500, and an error message if there is a data integrity error within the database
        200, and the queried log hours and minutes if all runs successfully
    """
    # Check if task exists
    task = tasks.find_one({"_id": ObjectId(taskID)})
    if task == None:
        return 404, f"Task with _id {taskID} not found."
    
    
    # Logs
    logs: list[dict] = list(task["logs"])

    # Match logs with member id if it exists
    newLogs = []
    if memberID != None:

        # Checking if the member exists in the database
        member = members.find_one({"_id": ObjectId(memberID)})
        if member == None:
            return 404, f"Member with _id {memberID} does not exist."

        # Getting all logs that match the member and replacing the logs variable for use
        for i in logs:
            if memberID == i["member"]:
                newLogs.append(i)
        logs = newLogs

    try:
        # Setting timedelta sum
        totalLogTime = timedelta(0)
        for i in logs:
            timeSpent: str = i["hours"]
            hours, minutes = timeSpent.split(":")
            totalLogTime += timedelta(hours=int(hours), minutes=int(minutes))
    except:
        return 500, "Internal database error"

    # Creating return value
    ret = f"{str((totalLogTime.days*24) + (totalLogTime.seconds//3600)).zfill(2)} hours {str((totalLogTime.seconds//60)%60).zfill(2)} minutes"

    return 200, ret

# Testing
if __name__ == "__main__":
    code, res = get_total_time("670d5ee6e9a1238ae12f9cd8", "670d5ee6e9a1238ae12f9cd5")
    print(res)