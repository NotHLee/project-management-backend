"""
Imports
"""
from pymongo import MongoClient
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from bson.objectid import ObjectId
from datetime import datetime

"""
Flask CORS connection
"""
# Enable CORS for all routes
app = Flask(__name__)
CORS(app, origin='*') 


"""
Database connection, to be used in services
"""
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]


"""
Global variables
"""
# Example description for myVar
myVar: str = "Global Variable" # Camel case for variables #
# Example description for STATIC_VAR
STATIC_VAR: str = "Static variable" # Full caps for static variables #


class MyClass(): # Classes should have its initials capitalized #
    """
    Description for MyClass
    """

    # Example description for classVar
    classVar: str = "Class Variables"

    # Function Template
    def my_func(funcArg: int, funcArg2: str) -> int: # Snake case for functions #
        """
        Description for my_func

        Inputs -
            funcArg:    An integer argument.
            funcArg2:   A string argument.

        Returns -
            The given integer argument
        """
        arrVar1: list = []
        arrVar2: list = []
        arrVar3: list = []

        # Use ijk for nested loops #
        for i in arrVar1:
            for j in arrVar2:
                for k in arrVar3:
                    break
                break
            break

        return funcArg

"""
Flask Routing
"""
# Sample GET Route Calling Method
@app.route('/api/tasks', methods=['GET'])
def call_func():
    tasks = list(db.tasks.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return make_response(jsonify(tasks), 200)

# Sample POST Route Calling Method
@app.route('/api/tasks', methods=['POST'])
def add_task():
    task = request.json
    result = db.tasks.insert_one(task)
    task['_id'] = str(result.inserted_id)
    return make_response(jsonify(task), 201)


"""
Datetime<->String conversions
"""
datetime.strptime("28/05/2024", "%d/%m/%Y") # Conv string to datettime    
datetime.strftime("%d,%m,%Y") # Conv datetime to string