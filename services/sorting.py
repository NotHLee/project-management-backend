from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

# Mapping priority to numerical values for sorting
PRIORITY_ORDER = {
    "Low": 0,
    "Medium": 1,
    "Important": 2,
    "Urgent": 3
}

def get_sorted(tableName: str, keyName: str, reverseBool: bool):
    # Retrieve the data from the database
    table = list(db[tableName].find())

    # Sort by creationDate if that is the key
    if keyName == "creationDate":
        for item in table:
            # Convert date strings to datetime for sorting if needed
            if isinstance(item[keyName], str):
                item[keyName] = datetime.strptime(item[keyName], "%d/%m/%Y")

        # Sort the table by date and reverse if reverseBool is True
        table.sort(key=lambda item: item[keyName], reverse=reverseBool)

        # Convert datetime objects back to strings after sorting
        for item in table:
            if isinstance(item[keyName], datetime):
                item[keyName] = item[keyName].strftime("%d/%m/%Y")

    # Sort by priority if that is the key
    elif keyName == "priority":
        table.sort(key=lambda item: PRIORITY_ORDER[item[keyName]], reverse=reverseBool)

    return table

def date_key(item: dict):
    return item["creationDate"]

def priority_key(item: dict):
    return PRIORITY_ORDER[item["priority"]]

