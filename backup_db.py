# from db import purge_data
import bson.json_util
from pymongo import MongoClient
import os
import bson
import json
from datetime import datetime


CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
membersCol = client[db_name]["members"]
sprintsCol = client[db_name]["sprints"]
tasksCol = client[db_name]["tasks"]

backupPath = os.path.dirname(os.path.abspath(__file__)) + "\\backups"
MAX_BACKUPS = 4


# def list_backups(timeFlag: bool=False) -> list[str]:
#     # List all backup directories
#     if timeFlag:
#         ret = os.listdir(backupPath)
#         for i in range(len(ret)):
#             ret[i] = ret[i][19:]
#         return ret

#     else:
#         return os.listdir(backupPath)


def create_backup(name: str=None) -> str:
    # Default naming loop if name isn't provided

    print("Creating backup")

    counter = 0
    maxed = False
    if name == None:
        while True:
            name = "backup" + str(counter)
            nPath = backupPath + f"\\{name}"
            if not os.path.exists(nPath):
                break
            else:
                counter += 1

            if counter >= MAX_BACKUPS:
                maxed = True
                break

        if maxed:
            name = f"{'backup' + str(0)}"
            nPath = backupPath + f"\\{name}"
            with open(nPath + "\\date_updated.txt", "r") as file:
                earliest = datetime.strptime(file.read(), "%d/%m/%Y, %H:%M:%S")

            for i in range(1, MAX_BACKUPS):
                cName = f"{'backup' + str(i)}"
                checkPath = backupPath + f"\\{cName}"
                with open(checkPath + "\\date_updated.txt", 'r') as file:
                    cTime = file.read()
                    checkEarliest = datetime.strptime(cTime, "%d/%m/%Y, %H:%M:%S")


                if checkEarliest < earliest:
                    earliest = checkEarliest
                    name = cName
                    nPath = checkPath


    # Else, use the provided name to form a backup path
    else:
        nPath = backupPath + f"\\{name}"

    # Make a new directory if the given backup path doesn't exist
    if not os.path.exists(nPath):
        os.makedirs(nPath)

    # Backup data to the given path
    cursor = membersCol.find({})
    with open(nPath + "\\members.json", 'w') as file:
        # Write to the json file, with a bson string format.
        json.dump(json.loads(bson.json_util.dumps(cursor)), file, indent=4)

    cursor = sprintsCol.find({})
    with open(nPath + "\\sprints.json", 'w') as file:
        json.dump(json.loads(bson.json_util.dumps(cursor)), file, indent=4)

    cursor = tasksCol.find({})
    with open(nPath + "\\tasks.json", 'w') as file:
        json.dump(json.loads(bson.json_util.dumps(cursor)), file, indent=4)

    # Save the date created
    dateCreated = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    with open(nPath + "\\date_updated.txt", 'w') as file:
        file.write(dateCreated)

    return f"Backup {name} created on {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"





# def restore_backup(name: str=None):
#     if name == None:
#         rPath = backupPath + f"\\{list_backups()[-1]}"

#     # purge_data.purge()

#     with open(rPath + "\\members.json", 'r') as file:
#         data: list[dict] = json.load(file)
#         # for i in data:
#         #     print(f'\n{i}')
#             # membersCol.insert_one(bson.json_util.loads(str(i)))

#     with open(rPath + "\\sprints.json", 'r') as file:
#         data: list[dict] = json.load(file)
#         # for i in data:
#         #     print(f'\n{i}')
#             # sprintsCol.insert_one(bson.json_util.loads(str(i)))

#     with open(rPath + "\\tasks.json", 'r') as file:
#         data: list[dict] = json.load(file)
#         # for i in data:
#         #     print(f'\n{i}')
#             # tasksCol.insert_one(bson.json_util.loads(str(i)))

if __name__ == "__main__":
    print(create_backup())