from pymongo import MongoClient
from services import *
from services import incomplete
from controllers import *
from routes import *
from validation import *
from flask import make_response, jsonify, request
from application import app
from bson.objectid import ObjectId
from flask_cors import CORS

#Allow CORS (temporarily allow all origins)
CORS(app, origins="*")

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

@app.route(tasks_routes_public.LOGIN, methods=['POST'])
def login():
    data = request.json

    # Debugging: print the incoming data
    print(f"Received data: {data}")

    # Check if data contains 'memberName' and 'password'
    if not data or 'memberName' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data['memberName']
    password = data['password']

    # Call the validation function
    status, result = login_validation.validate_login(username, password)

    return jsonify(result), status


@app.route(tasks_routes_public.LOGIN, methods=['PATCH'])
def password_change():
    data = request.json

    username = data['_id']
    new_password = data['password']

    members_collection = db["members"]  # Assuming you have a 'members' collection


    # Update the password for the found member
    result = members_collection.update_one(
        {"_id": ObjectId(username)},
        {"$set": {"password": new_password}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"error": "No changes were made to the password."}), 400

@app.route(tasks_routes_public.SECURITY_CHECK, methods=['POST'])
def verify_security_answers():
    data = request.json

    # Ensure the data contains the memberName
    if not data or '_id' not in data:
        return jsonify({"error": "Missing memberName"}), 400

    username = data.pop('_id')  # Remove memberName from data to leave only question-answer pairs

    # Fetch the member from the database
    members_collection = db["members"]
    member = members_collection.find_one({"_id": ObjectId(username)})

    if not member:
        return jsonify({"error": "Member not found"}), 404

    # Retrieve stored security answers from the member's record
    stored_security_answers = member.get('securityQuestions', {})

    # Initialize a variable to track if all answers match
    all_answers_match = True

    # Iterate through the provided question-answer pairs
    for question_num, provided_answer in data.items():
        stored_answer = stored_security_answers.get(str(question_num))

        if not stored_answer:
            return jsonify({"error": f"Question {question_num} is not valid."}), 400

        # Compare the provided answer to the stored answer
        if stored_answer != provided_answer:
            all_answers_match = False
            break  # If any answer doesn't match, we can stop checking

    # If all answers matched, return success; otherwise, return an error
    if all_answers_match:
        return jsonify({"message": "Security answers verified successfully."}), 200
    else:
        return jsonify({"error": "One or more answers are incorrect."}), 401

@app.route(tasks_routes_public.SECURITY_CHECK, methods=['PATCH'])
def reset_password():

    member_id = request.args.get('memberID')
    print(member_id)

    # Ensure the request contains the memberName
    if not member_id:
        return jsonify({"error": "Missing id"}), 400

    # default password (all lowercase + "123")
    default_password = "password12345"

    members_collection = db["members"]
    member = members_collection.find_one({"_id": ObjectId(member_id)})

    print(member)

    if not member:
        return jsonify({"error": "Member not found"}), 404

    # Update the member's password to the default password
    result = members_collection.update_one(
        {"_id": member["_id"]},
        {"$set": {"password": default_password}}
    )

    if result.modified_count > 0:
        return jsonify({"message": f"Password reset successfully to {default_password}"}), 200
    else:
        return jsonify({"error": "No changes were made to the password."}), 400


@app.route(tasks_routes_public.SECURITY_CHECK, methods=['GET'])
def is_admin():
    """
    API endpoint to check if there is an admin in the system.
    Response:
        200: If the request was successful.
        500: If an internal server error occurred.
    """
    members_table = db["members"]
    admin_exists = members_table.find_one({"access": "Admin"})

    if admin_exists == None:
        return jsonify(False), 200
    elif admin_exists != None:
        return jsonify(True), 200