"""
members.py handles all communication between the frontend and the backend using api calls
and any additional logic as required for the members.
"""

from pymongo import MongoClient
from services import *
from routes import *
from flask import make_response, jsonify, request
from application import app
from bson.objectid import ObjectId
from flask_cors import CORS
from controllers import *

#Allow CORS (temporarily allow all origins)
CORS(app, origins="*")

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

# Get entire collection
@app.route(tasks_routes_private.MEMBERS, methods=['GET'])
def get_members():
    """
    get_all_members connects the get_all method to the api by providing the logic required to convert the collection of members to a json file.

    Inputs -
        None

    Returns -
        A response with either a jsonified table, or 404 if the table isn't found.
    """

    member_id = request.args.get("memberId")
    memberName = request.args.get("memberName")

    # if member _id is provided, query for that specific member
    if member_id:
        table = getter.get_one_query("members", {"_id": ObjectId(member_id)})
        if table == None:
            return make_response(jsonify({"error": "Member not found."}), 404)
        else:
            table["_id"] = str(table["_id"])

            return make_response(jsonify(table), 200)

    elif memberName:
        table = getter.get_one_query("members", {"memberName": memberName})
        if table == None:
            return make_response(jsonify({"error": "Member not found."}), 404)
        else:
            table["_id"] = str(table["_id"])

            return make_response(jsonify(table), 200)

    # else, get all members
    table = getter.get_all("members")

    # parse datetime object to only include date
    for member in table:
        member["joinDate"] = member["joinDate"].strftime("%Y-%m-%d")

    # if no member_id is provided, return all members
    if table == None:
        return make_response(jsonify({"error": "No members found."}), 404)
    else:
        return make_response(jsonify(table), 200)

@app.route(tasks_routes_private.MEMBERS, methods=['POST'])
def members_add():
    """
    members_add requests member details in the form of a json/dict from the front end and runs a function to add it to the database

    Inputs -
        None

    Returns -
        Returns a 200 response if adding was successful, 400 if the data could not be added.
    """
    request_data = request.get_json()
    print(request_data)

    # if securityQuestions is not provided, set it to None
    if "securityQuestions" not in request_data:
        request_data["securityQuestions"] = None

    try:
        # call the add_one function to add the member into the members table
        status_code, result = add.add_one("members", request_data, "")

        if status_code == 200:

            # convert _id and joinDate to string
            result["_id"] = str(result["_id"])
            result["joinDate"] = result["joinDate"].strftime("%d-%m-%Y")
            return make_response(jsonify({"message": "Member added successfully.",
                                          "memberId": result["_id"],
                                          "member": result}), status_code)

        else:
            return make_response(jsonify({"error": result}, status_code))

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

# Delete a member from the collection
@app.route(tasks_routes_private.MEMBERS, methods=['DELETE'])
def members_delete():
    """
    members_delete requests a member in the form of a json/dict from the front end and runs a function to delete the member from the database

    Inputs -
        None

    Returns -
        Returns a 200 response if deletion is successful, 404 if the data entry could not be found.
    """
    member_id = request.args.get("memberId")
    oid: ObjectId = ObjectId(member_id)

    # Calls the delete_one function to delete a member in the members table
    result = delete.delete_one("members", oid)

    if result == 200:
        return make_response(jsonify(message=f"Member with oid: {str(oid)} in members table deleted."), 200)
    else:
        return make_response(jsonify(message="Member not found."), 404)

@app.route(tasks_routes_public.MEMBER_TASK, methods=['GET'])
def get_tasks_by_member():
    member_id = request.args.get("memberID")

    # Call the helper function to get the tasks
    task_list = getter.get_tasks_for_member(str(member_id))

    print(f"{task_list} meow")

    print(len(task_list))

    # Correctly construct the response
    return jsonify({"tasks": task_list}), 200

@app.route(tasks_routes_public.MEMBER_HOURS, methods=['GET'])
def get_member_hours():
    """
    API Endpoint to retrieve the hours worked by a member between two dates.
    Request parameters:
        startDate (string): Start date in the format dd/mm/yyyy
        endDate (string): End date in the format dd/mm/yyyy
    Path parameter:
        memberID (string): ID of the member whose work logs are to be retrieved
    Response:
        200: Successful query with date range and hours worked.
        400: Invalid date format or start date later than end date.
        404: Member ID not found.
        500: Internal error related to data integrity.
    """
    # Get startDate and endDate from query parameters
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    memberID = request.args.get("memberID")

    # Validate that startDate and endDate are provided
    if not startDate or not endDate:
        return jsonify({"error": "Both startDate and endDate parameters are required"}), 400

    # Call the get_hours function
    code, result = query_member_hours.get_hours(startDate, endDate, memberID)

    # Handle the different response codes
    if code == 200:
        return jsonify(result), 200
    elif code == 400:
        return jsonify({"error": result}), 400
    elif code == 404:
        return jsonify({"error": result}), 404
    else:
        return jsonify({"error": result}), 500

@app.route(tasks_routes_public.ALL_MEMBER_HOURS, methods=['GET'])
def get_all_members_hours():
    """
    API Endpoint to retrieve the hours worked by all members between two dates.
    Request parameters:
        startDate (string): Start date in the format dd/mm/yyyy
        endDate (string): End date in the format dd/mm/yyyy
    Response:
        200: Successful query with date range and hours worked for each member.
        400: Invalid date format or start date later than end date.
        500: Internal error related to data integrity.
    """
    # Get startDate and endDate from query parameters
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")

    # Validate that startDate and endDate are provided
    if not startDate or not endDate:
        return jsonify({"error": "Both startDate and endDate parameters are required"}), 400

    # Get all members from the members collection
    members_table = db["members"]
    all_members = members_table.find()  # Fetch all members from the database

    # Prepare an array to hold the hours worked for each member
    all_members_hours = []

    # Loop through each member and get the hours worked
    for member in all_members:
        memberID = str(member["_id"])  # Convert ObjectId to string

        # Call the get_hours function for the member
        code, result = query_member_hours.get_hours(startDate, endDate, memberID)

        # Check if the code is successful or handle errors
        if code == 200:
            result["_id"] = memberID
            # Append member's hours to the array
            all_members_hours.append(result)
        elif code == 400:
            # Handle invalid date range error, return it early for user to fix
            return jsonify({"error": f"Invalid date range for member {member['memberName']}: {result}"}), 400
        elif code == 500:
            # Handle internal data error for this member
            return jsonify({"error": f"Data error for member {member['memberName']}: {result}"}), 500

    # If all members were processed successfully, return the results
    return jsonify(all_members_hours), 200

@app.route(tasks_routes_public.MEMBERS, methods=['PATCH'])
def member_modify():

    request_data = request.json
    member_id = request.args.get("memberId")

    if not member_id:
        return jsonify({"error": "Member id not provided"}), 400

    # Call the modify function to modify the member
    result = modify_member.modify_member(member_id, request_data)

    return make_response(jsonify({"message": result}), 200)

@app.route(tasks_routes_public.REMAINING_MEMBERS, methods=['GET'])
def get_remaining_members():

    member_to_be_deleted = request.args.get("memberId")
    table = getter.get_all("members")

    # filter out the member to be deleted
    table = [member for member in table if str(member["_id"]) != member_to_be_deleted]

    # only return the member name and id
    table = [{"_id": str(member["_id"]), "memberName": member["memberName"]} for member in table]

    return make_response(jsonify(table), 200)
