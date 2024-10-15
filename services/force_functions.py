from bson import ObjectId
from flask import make_response, jsonify, request
from application import app
from pymongo import MongoClient
from datetime import datetime

from backend.routes import tasks_routes_public
from backend.validation.sprints_validation import validate_sprint_data
#from validation import *  # Assuming you have relevant validation functions

# Connecting to the db
CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

@app.route(tasks_routes_public.SPRINTS, methods=['PATCH'])
def force_start_sprint():
    try:
        # Get the sprint to be force-started
        sprintId = request.args.get("sprintID")
        if not sprintId:
            return make_response(jsonify({"error": "Sprint ID not provided"}), 400)


        sprint = db.sprints.find_one({"_id": ObjectId(sprintId)})
        if not sprint:
            return make_response(jsonify({"error": "Sprint not found"}), 404)

        # Change status and startDate
        sprint_data = {
            "sprintName": sprint.get("sprintName"),
            "status": "In Progress",  
            "tasks": sprint.get("tasks", []),
            "startDate": datetime.now(), 
            "endDate": sprint.get("endDate")
        }

        # Check if there are any other sprints active
        validation_result = validate_sprint_data(sprint_data)
        if validation_result is not True:
            return make_response(jsonify({"error": validation_result}), 400)

        # Update the sprint
        result = db.sprints.update_one(
            {"_id": ObjectId(sprint_id)},
            {"$set": {"status": "In Progress", "startDate": datetime.now()}}  # Update startDate to now
        )

        if result.modified_count > 0:
            return make_response(jsonify({"message": "Sprint force-started successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Failed to update the sprint"}), 500)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)