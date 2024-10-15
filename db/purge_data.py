"""
purge_data.py purges all data from the database.
"""

from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

members = db["members"]
tasks = db["tasks"]
sprints = db["sprints"]

def purge():
    members.delete_many({})
    tasks.delete_many({})
    sprints.delete_many({})

if __name__ == "__main__":
    purge()