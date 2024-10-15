from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]

def validate_login(username: str, password: str):
    members_collection = db["members"]  # Assuming you have a 'members' collection

    member = members_collection.find_one({"memberName": username})

    print(f"Query result: {member}")
    
    if not member:
        return 404, {"message": "Username not found"}  # Return 404 for missing username
    
    print(member['password'])
    print(password)
    if member['password'] == password:
        # Authentication successful
        return 200, {
            "message": "Login successful",
            "_id": str(member['_id']),
            "memberName": member['memberName']
        }
    else:
        # Authentication failed
        return 401, {"message": "Invalid username or password"}

    
def validate_member_credentials(username: str, password: str):
    """Helper function to validate member credentials."""
    members_collection = db["members"]
    
    # Debugging: print the query
    print(f"Searching for username: {username}")
    
    member = members_collection.find_one({"memberName": username})
    
    # Debugging: print the result of the query
    print(f"Query result: {member}")
    
    # Check if the username exists in the database
    if not member:
        return 404, {"error": "Username not found"}
    
    # Check if the provided password matches the one in the database
    if member['password'] != password:
        return 401, {"error": "Incorrect password"}
    
    # If the validation is successful, return member ID
    return 200, {"message": "Login successful", "memberID": str(member['_id'])}
