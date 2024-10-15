from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def modify_member(member_id: str, modifications: dict):

    members_table = db["members"]

    # update the member in the members table only
    result = members_table.update_one({"_id": ObjectId(member_id)}, {"$set": modifications})

    if result.modified_count == 1:
        return 200, "Member updated successfully"

    else:
        return 404, "Member not found"