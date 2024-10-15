"""
query_member_hours.py
A controller used specifically to get the total hours worked per day of a member given a range of dates
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

CONNECTION_STRING = "mongodb+srv://admin:admin@fit2101-pandasoft.uothz.mongodb.net/"
db_name = "agile_management_project"
client = MongoClient(CONNECTION_STRING)
db = client[db_name]
members = db["members"]
tasks = db["tasks"]

def get_hours(startDate: str, endDate: str, memberID: str) -> tuple[int, str | dict]:
    """
    This function is used to get the work done of a member between two dates.

    Inputs -
        startDate: The start date of the range formatted dd/mm/yyyy
        endDate: The end date of the range formatted dd/mm/yyyy
        memberID: The string ID of the member to be queried

    Returns -
        Code 404 and an error message if the memberID is not found.
        Code 400 and an error message if the dates are invalid.
        Code 500 and an error messsage if data integrity within the database isn't maintained.
        Code 200, with a dictionary containing labels, storyPoints, average_effort, and total_effort.
    """
    
    # Check if member exists
    member = members.find_one({"_id": ObjectId(memberID)})
    if member is None:
        return 404, f"Member with _id {memberID} not found."
    
    # Get all logs date and hours that match the given member
    logs: list[tuple[datetime, str]] = [(j["date"], j["hours"]) for i in list(tasks.find()) for j in i["logs"] if j["member"] == memberID]

    # Create a dict and initialize variables required for the loop for all dates within the given start and end date range
    logsSums = {}
    increment = timedelta(days=1)
    try:
        startDT = datetime.strptime(startDate, "%d/%m/%Y")
        endDT = datetime.strptime(endDate, "%d/%m/%Y")
    except ValueError:
        return 400, f"Provided dates are in an incorrect format.\nExpected: dd/mm/yyyy\nGiven: {startDate}, {endDate}"

    if startDT > endDT:
        return 400, f"Start date cannot be later than end date: {startDate} > {endDate}"

    # Insert all values in the range of the start and end date into the dict initialized with 0
    while startDT <= endDT:
        logsSums[startDT.strftime("%d/%m/%Y")] = timedelta(0)
        startDT += increment

    # Check all logs with the given member, match the dates in the dict and add all worked hours to it.
    try:
        for date, time in logs:
            dateDT = date.strftime("%d/%m/%Y")
            if dateDT in logsSums:
                i = time.split(":")
                hours = int(i[0])
                minutes = int(i[1])
                logsSums[dateDT] += timedelta(hours=hours, minutes=minutes)
    except:
        return 500, f"Internal database error."

    
    # Turn all dates and hours worked in those dates into lists
    retDate: list[str] = list(logsSums.keys())
    retHours: list[timedelta] = list(logsSums.values())

    # Sum up total efforts
    totalEffort = timedelta(0)
    for i in retHours:
        totalEffort += i

    # Get average effort using seconds (no .days and .seconds needed in conversion to string)
    averageEffort = (totalEffort.seconds + (totalEffort.days*86400)) / len(retDate)

    # Conversion to string
    for i in range(len(retHours)):
        retHours[i] = (retHours[i].seconds/3600)

    totalEffort = f"{str((totalEffort.days*24) + (totalEffort.seconds//3600)).zfill(2)} hours {str((totalEffort.seconds//60)%60).zfill(2)} minutes"
    averageEffort = f"{str(int(averageEffort//3600)).zfill(2)} hours {str(int(averageEffort//60)%60).zfill(2)} minutes"

    # Return the resulting dictionary
    ret = {
        "dates": retDate,
        "timeSpent": retHours,
        "averageEffort": averageEffort,
        "totalEffort": totalEffort
    }

    return 200, ret

# Testing
# if __name__ == "__main__":
#     code, res = get_hours("07/10/2024", "14/10/2024", "670d505793dd6da976914b60")

#     # Printing output
#     ob = "{"
#     cb = "}"
#     print(res)
#     print(f"{ob}\ndates: {res['dates']}")
#     print(f"timeSpent: {res['timeSpent']}")
#     print(f"averageEffort: '{res['averageEffort']}'")
#     print(f"totalEffort: '{res['totalEffort']}'\n{cb}")