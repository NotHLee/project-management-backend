"""
create_data.py creates dummy data to be used in the database.
"""
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]
members = db["members"]
tasks = db["tasks"]
sprints = db["sprints"]


membersList = [
   {
      "memberName": "Alice",
      "password": "alice123",
      "access": "Admin",
      "email": "alice@email.com",
      "joinDate": datetime.now() - timedelta(days=14, hours=21),
      "securityQuestions": {
         "Example Question 1": "Answer 1", 
         "Example Question 2": "Answer 2", 
         "Example Question 3": "Answer 3"
      }
   },
   {
      "memberName": "John",
      "password": "john123",
      "access": "User",
      "email": "john@email.com",
      "joinDate": datetime.now() - timedelta(days=14, hours=20),
      "securityQuestions": None
   },
   {
      "memberName": "Martha",
      "password": "martha234",
      "access": "User",
      "email": "martha@email.com",
      "joinDate": datetime.now() - timedelta(days=14, hours=20),
      "securityQuestions": None
   },
   {
      "memberName": "Nolan",
      "password": "nolan234",
      "access": "User",
      "email": "nolan@email.com",
      "joinDate": datetime.now() - timedelta(days=14, hours=15),
      "securityQuestions": None
   }
]

members.insert_many(membersList)


itemsMT = list(members.find())
idsMT = []

for i in itemsMT:
   idsMT.append(str(i["_id"]))

tasksList = [
    {
        "taskName": "Example Task 1",
        "storyType": "Story",
        "storyPoints": 9,
        "tags": ["Frontend"],
        "priority": "Low",
        "assignee": idsMT[0],
        "status": "Completed",
        "description": "Example desc for task 1",
        "progress": "Planning",
        "creationDate": datetime.now() - timedelta(days=11, hours=5),
        "completionDate": datetime.now() - timedelta(days=3, hours=19),
        "sprint": None,
        "logs": [
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=6, hours=22),
               "hours": "03:12"
            },
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=4, hours=17),
               "hours": "06:00"
            },
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=4, hours=3),
               "hours": "04:15"
            },
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=3, hours=8),
               "hours": "01:24"
            },
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=2, hours=17),
               "hours": "02:41"
            },
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=2, hours=4),
               "hours": "05:02"
            },
         ],
        "history": [
            {
               "description": "Created by Alice.", 
               "date": datetime.now() - timedelta(days=11, hours=5)
            }, 
            {
               "description": "Added to Sprint 1.", 
               "date": datetime.now()- timedelta(days=8)
            }, 
            {
               "description": "Field: 'status', 'progress' updated by Alice.", 
               "date": datetime.now() - timedelta(days=7)
            }, 
            {
               "description": "Field: 'progress' updated by Alice.", 
               "date": datetime.now() - timedelta(days=3, hours=19)
            },
            {
               "description": "Field: 'progress' updated by Alice.", 
               "date": datetime.now() - timedelta(days=2, hours=15)
            },
            {
               "description": "Field: 'status', 'progress' updated by Alice.", 
               "date": datetime.now() - timedelta(days=1, hours=23)
            }
        ]
     },
     {
        "taskName": "Example Task 2",
        "storyType": "Bug",
        "storyPoints": 2,
        "tags": ["Backend"],
        "priority": "Medium",
        "assignee": idsMT[2],
        "status": "Completed",
        "description": "Example desc for task 2",
        "progress": "Development",
        "creationDate": datetime.now() - timedelta(days=11),
        "completionDate": datetime.now() - timedelta(days=4, hours=22),
        "sprint": None,
        "logs": [
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=6, hours=5),
               "hours": "06:16"
            },
            {
               "member": idsMT[0],
               "date": datetime.now() - timedelta(days=5, hours=19),
               "hours": "04:05"
            },
            {
               "member": idsMT[2],
               "date": datetime.now() - timedelta(days=5, hours=12),
               "hours": "03:05"
            },
            {
               "member": idsMT[2],
               "date": datetime.now() - timedelta(days=5, hours=3),
               "hours": "05:02"
            },
            {
               "member": idsMT[2],
               "date": datetime.now() - timedelta(days=4, hours=2),
               "hours": "02:07"
            },
            {
               "member": idsMT[2],
               "date": datetime.now() - timedelta(days=2, hours=17),
               "hours": "03:41"
            },
            {
               "member": idsMT[2],
               "date": datetime.now() - timedelta(days=1, hours=15),
               "hours": "07:00"
            }
        ],
        "history": [
            {
               "description": "Created by Alice.", 
               "date": datetime.now() - timedelta(days=11)
            },
            {
               "description": "Added to Sprint 1.", 
               "date": datetime.now()- timedelta(days=8)
            },
            {
               "description": "Field 'status', 'progress' updated by Alice.", 
               "date": datetime.now() - timedelta(days=6, hours=5)
            },
            {
               "description": "Assignee changed from Alice to Martha.", 
               "date": datetime.now() - timedelta(days=5, hours=14)
            },
            {
               "description": "Field 'progress' updated by Martha.", 
               "date": datetime.now() - timedelta(days=5, hours=9)
            },
            {
               "description": "Field 'progress' updated by Martha.", 
               "date": datetime.now() - timedelta(days=4)
            },
            {
               "description": "Field 'status', 'progress' updated by Martha.", 
               "date": datetime.now() - timedelta(days=1, hours=8)
            }
        ]
     },
     {
        "taskName": "Example Task 3",
        "storyType": "Story",
        "storyPoints": 5,
        "tags": ["Backend"],
        "priority": "Important",
        "assignee": idsMT[1],
        "status": "Not Started",
        "description": "Example desc for task 3",
        "progress": "Integration",
        "creationDate": datetime.now() - timedelta(days=10, hours=4),
        "completionDate": None,
        "sprint": None,
        "logs": [],
        "history": [
            {
               "description": "Created by Alice.", 
               "date": datetime.now() - timedelta(days=10, hours=4)
            },
            {
               "description": "Added to Sprint 2", 
               "date": datetime.now() + timedelta(hours=3)
            }
        ]
     },
     {
        "taskName": "Example Task 4",
        "storyType": "Story",
        "storyPoints": 3,
        "tags": ["Backend", "Framework"],
        "priority": "Urgent",
        "assignee": idsMT[1],
        "status": "Not Started",
        "description": "Example desc for task 4",
        "progress": "Integration",
        "creationDate": datetime.now() - timedelta(days=9, hours=1),
        "completionDate": None,
        "sprint": None,
        "logs": [],
        "history": [
            {
               "description": "Created by John.",
               "date": datetime.now() - timedelta(days=10, hours=4)
            },
            {
               "description": "Added to Sprint 2", 
               "date": datetime.now() + timedelta(hours=3)
            }
        ]
     },
     {
        "taskName": "Example Task 5",
        "storyType": "Story",
        "storyPoints": 2,
        "tags": ["Frontend"],
        "priority": "Urgent",
        "assignee": idsMT[3],
        "status": "Not Started",
        "description": "Example desc for task 5",
        "progress": "Planning",
        "creationDate": datetime.now() - timedelta(days=7, hours=15),
        "completionDate": None,
        "sprint": None,
        "logs": [],
        "history": [
            {
               "description": "Created by Nolan.", 
               "date": datetime.now() - timedelta(days=7, hours=15)
            },
            {
               "description": "Added to Sprint 4.", 
               "date": datetime.now() + timedelta(days=3)
            }
        ]
     },
     {
        "taskName": "Example Task 6",
        "storyType": "Bug",
        "storyPoints": 2,
        "tags": ["Backend", "Database"],
        "priority": "Urgent",
        "assignee": idsMT[0],
        "status": "Not Started",
        "description": "Example desc for task 6",
        "progress": "Planning",
        "creationDate": datetime.now() - timedelta(days=7, hours=15),
        "completionDate": None,
        "sprint": None,
        "logs": [],
        "history": [
            {
               "description": "Created by Alice.", 
               "date": datetime.now() - timedelta(days=7, hours=15)
            },
            {
               "description": "Added to Sprint 3.", 
               "date": datetime.now() + timedelta(days=6)
            }
        ]
     },
     {
        "taskName": "Example Task 7",
        "storyType": "Story",
        "storyPoints": 10,
        "tags": ["Frontend", "UI/UX"],
        "priority": "Urgent",
        "assignee": idsMT[2],
        "status": "In Progress",
        "description": "Example desc for task 7",
        "progress": "Planning",
        "creationDate": datetime.now() - timedelta(days=7, hours=15),
        "completionDate": None,
        "sprint": None,
        "logs": [
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=5, hours=17),
               "hours": "03:01"
            },
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=5, hours=12),
               "hours": "04:05"
            },
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=4, hours=9),
               "hours": "07:06"
            },
            {
               "member": idsMT[2],
               "date": datetime.now() - timedelta(days=3, hours=10),
               "hours": "05:07"
            },
            {
               "member": idsMT[2],
               "date": datetime.now() - timedelta(days=1, hours=5),
               "hours": "04:09"
            },
        ],
        "history": [
            {
               "description": "Created by Nolan.", 
               "date": datetime.now() - timedelta(days=7, hours=15)
            },
            {
               "description": "Field 'priority' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=7, hours=11)
            },
            {
               "description": "Field 'taskName', 'storyPoints' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=7, hours=10)
            },
            {
               "description": "Added to Sprint 1.", 
               "date": datetime.now() - timedelta(days=7, hours=9)
            },
            {
               "description": "Field 'status', 'progress' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=5, hours=17)
            },
            {
               "description": "Field 'progress' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=4, hours=2)
            },
            {
               "description": "Assignee changed from Nolan to Martha.", 
               "date": datetime.now() - timedelta(days=4, hours=2)
            },
            {
               "description": "Field 'progress' updated by Martha.", 
               "date": datetime.now() - timedelta(days=3, hours=5)
            },
            {
               "description": "Removed from Sprint 1.", 
               "date": datetime.now() - timedelta(days=1)
            }
        ]
     },
     {
        "taskName": "Example Task 8",
        "storyType": "Story",
        "storyPoints": 4,
        "tags": ["Backend", "Framework", "API"],
        "priority": "Urgent",
        "assignee": idsMT[3],
        "status": "Completed",
        "description": "Example desc for task 8",
        "progress": "Planning",
        "creationDate": datetime.now() - timedelta(days=7, hours=10),
        "completionDate": datetime.now() - timedelta(days=6, hours=23),
        "sprint": None,
        "logs": [
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=7, hours=3),
               "hours": "04:12"
            },
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=4, hours=2),
               "hours": "05:14"
            },
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=3, hours=15),
               "hours": "02:15"
            },
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=3, hours=6),
               "hours": "03:15"
            },
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=2, hours=20),
               "hours": "01:15"
            },
            {
               "member": idsMT[3],
               "date": datetime.now() - timedelta(days=2, hours=2),
               "hours": "04:15"
            }
        ],
        "history": [
            {
               "description": "Created by Alice.", 
               "date": datetime.now() - timedelta(days=7, hours=10)
            },
            {
               "description": "Field: 'status', 'progress' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=7, hours=3)
            },
            {
               "description": "Field: 'progress' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=3, hours=3)
            },
            {
               "description": "Field: 'progress' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=2, hours=19)
            },
            {
               "description": "Field: 'status', 'progress' updated by Nolan.", 
               "date": datetime.now() - timedelta(days=1, hours=22)
            }
        ]
     }
]

tasks.insert_many(tasksList)


itemsTS = list(tasks.find())
idsTS = []
ptsTS = []
for i in itemsTS:
    idsTS.append(str(i["_id"]))
    ptsTS.append(int(i["storyPoints"]))

sprintsList = [
    {
      "sprintName": "Sprint 1",
      "status": "Completed",
      "tasks": [
          idsTS[0],
          idsTS[1],
          idsTS[7]
      ],
      "startDate": datetime.now() - timedelta(days=7, hours=4),
      "endDate": datetime.now() - timedelta(days=1),
      "totalSprintPoints": (ptsTS[0] + ptsTS[1] + ptsTS[7] + ptsTS[6])
    },
    {
      "sprintName": "Sprint 2",
      "status": "Not Started",
      "tasks": [
          idsTS[2],
          idsTS[3]
      ],
      "startDate": datetime.now() + timedelta(days=1),
      "endDate": datetime.now() + timedelta(days=10),
      "totalSprintPoints": (ptsTS[2] + ptsTS[3])
    },
    {
      "sprintName": "Sprint 3",
      "status": "Not Started",
      "tasks": [
         idsTS[5]
      ],
      "startDate": datetime.now() + timedelta(days=12),
      "endDate": datetime.now() + timedelta(days=18),
      "totalSprintPoints": (ptsTS[5])
    },
    {
      "sprintName": "Sprint 4",
      "status": "Not Started",
      "tasks": [
          idsTS[4]
      ],
      "startDate": datetime.now() + timedelta(days=19),
      "endDate": datetime.now() + timedelta(days=26),
      "totalSprintPoints": (ptsTS[4])
    }
]

sprints.insert_many(sprintsList)

for i in range(len(idsTS)):
    sprint = sprints.find_one({"tasks":{"$in":[idsTS[i]]}})
    updatingID = ObjectId(idsTS[i])
    if sprint != None:
      updating = tasks.update_one({"_id": updatingID}, {"$set": {"sprint":str(sprint["_id"])}})

