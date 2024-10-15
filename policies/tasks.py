"""
tasks.py handles all communication between the frontend and the backend using api calls
and any additional logic as required.
"""
from datetime import datetime, timedelta
from pymongo import MongoClient
from services import *
from routes import *
from flask import make_response, jsonify, request
from application import app
from bson.objectid import ObjectId
from flask_cors import CORS
from controllers import query_task_time

# Allow CORS (temporarily allow all origins)
CORS(app, origins="*")

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

# Add an entry to the collection
@app.route(tasks_routes_public.TASKS, methods=['POST'])
def tasks_add():
    """
    tasks_add requests a task in the form of a json/dict from the front end and runs a function to add it to the database

    Inputs -
        None

    Returns -
        Returns a 200 response if adding was successful, 400 if the data could not be added.
    """
    member_id = request.args.get("memberID")
    task = request.json
    result, insertedTask = add.add_one("tasks", task, member_id)

    if result == 200:

        # convert creationDate and _id to string
        insertedTask["creationDate"] = insertedTask["creationDate"].strftime("%d-%m-%Y")
        insertedTask["_id"] = str(insertedTask["_id"])

        ret = make_response(insertedTask)

    else:
        ret = make_response(f"400 - Insertion operation failed.\nReason: {insertedTask}")

    ret.status_code = result
    return ret


# Delete an entry from the collection
@app.route(tasks_routes_public.TASKS, methods=['DELETE'])
def tasks_delete():
    """
    tasks_delete requests a a task in the form of a json/dict from the front end and runs a function to delete the matching data from the database

    Inputs -
        None

    Returns -
        Returns a 200 response if deletion is successful, 404 if the data entry could not be found.
    """
    requestItem = request.get_json()
    oid: ObjectId = ObjectId(requestItem["_id"])
    result = delete.delete_one("tasks", oid)
    if result == 200:
        ret = make_response(f"200 - Entry with oid: {str(oid)} in tasks table deleted.")
    else:
        ret = make_response(f"404 - Entry not found.")
    ret.status_code = result
    return ret

@app.route(tasks_routes_public.TASKS, methods=['GET'])
def get_sorted_tasks():
    try:
        # Get query parameters
        tableName = request.args.get('tableName', 'tasks')
        keyName = request.args.get('keyName', "creationDate")
        reverse = request.args.get('reverse', 'false').lower() == 'true'

        # Validate input
        if keyName not in ['creationDate', 'priority']:
            return jsonify({"error": keyName}), 400

        # Call the sorting function
        sorted_tasks = sorting.get_sorted(tableName, keyName, reverse)
        for task in sorted_tasks:
            if "_id" in task and isinstance(task["_id"], ObjectId):
                task["_id"] = str(task["_id"])
            if "sprint" in task and isinstance(task["sprint"], ObjectId):
                task["sprint"] = str(task["sprint"])

        return jsonify(sorted_tasks), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(tasks_routes_public.TASKS, methods=['PATCH'])
def modify_tasks():
    """
    modify_tasks modifies a list of tasks in the tasks table in the database
    """

    request_data = request.json
    member_id = request.args.get("memberId")

    if not member_id:
        return jsonify({"error": "Member id not provided"}), 400

    modified_tasks = []

    # modify each task in the list and append the result to a list
    for task in request_data:

        result = modify_task.modify_task(task["_id"], task, member_id)
        modified_tasks.append(result)

    return make_response(jsonify({"message": "All tasks modified successfully", "modified_tasks": modified_tasks}), 200)

@app.route(tasks_routes_public.LOG_TIME, methods=['POST'])
def log_time_spent():
    """
    Logs the time spent by a member on a task.
    Request Body:
        taskID (string): The ID of the task.
        memberID (string): The ID of the member logging time.
        hours (int): The number of hours worked.
        minutes (int, optional): The number of additional minutes worked (default is 0).
    Response:
        200: If the time log was successfully added.
        400: If there was an issue with the input or task lookup.
        500: For any server-side errors.
    """
    data = request.json

    # Get required fields from request body
    taskID = data.get("taskID")
    memberID = data.get("memberID")
    hours = data.get("hours")
 
    # Validate the input
    if not taskID or not memberID or not hours:
        return jsonify({"error": "Invalid input"}), 400

    ret = modify.add_log_time(memberID, taskID, hours)

    if ret == True:
        return make_response(jsonify({"message": "OK"}), 200)


@app.route(tasks_routes_public.LOG_TIME, methods=['GET'])
def get_total_time():
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
    try:
        # Get query parameters
        taskID = request.args.get('taskID')
        memberID = request.args.get('memberID', None)
        

        # Process query
        code, result = query_task_time.get_total_time(taskID, memberID)

        # Return either the required response of an error message
        if code == 200:
            return make_response(jsonify({"message": result}), 200)
        else:
            return jsonify({"error": result}, code)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
