from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from .force_start import force_start
from .force_end import force_end

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
sprints = client[db_name]["sprints"]

def update_sprint():

    print("Sprints has been updated")

    sprintList = list(sprints.find())

    for sprint in sprintList:
        if sprint["status"] == "Not Started" and sprint["startDate"] > datetime.now():
            code, res = force_start(str(sprint["_id"]))

        elif sprint["status"] == "In Progress" and datetime.now() > sprint["endDate"]:
            code, res = force_end(str(sprint["_id"]))