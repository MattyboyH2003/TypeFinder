import sqlite3
from TableVisualiser import *

if __name__ == "__main__":
    connectionSQL = sqlite3.connect("TypeFinder.db")
    cursorSQL = connectionSQL.cursor()

# ------------------- #
# Functions and stuff #
# ------------------- #

def DeletingRecords(cursorSQL, connectionSQL, table, userID): #This function deletes the record with the specified userID in the specified table
    delete = "DELETE FROM {} WHERE TagID={}".format(table, userID)
    cursorSQL.execute(delete)
    connectionSQL.commit()
    print("Record(s) Deleted")

def FindingData(cursorSQL, table): #This function is used to find all data in the specified table
    query = "SELECT * FROM {}".format(table)
    cursorSQL.execute(query)
    rows = cursorSQL.fetchall()
    return rows

def TestExistance(cursorSQL, table, userID): #This function checks if the specified user exists in the specified table
    cursorSQL.execute("SELECT userID FROM {}".format(table)) #This is the query
    userIDs = cursorSQL.fetchall()
    exist = False
    for row in userIDs: #This loop checks to see if the user exists
        temp = row
        if temp[0] == userID:
            exist = True
    
    if exist == True:
        print("This user exists in the specified table")
    elif exist == False:
        print("This user doesn't in the specified table")
    else:
        print("An error has occured")


class CreateQuerys:
    @staticmethod
    def CreateRecord(table : str, fieldNames : list):

        query = "INSERT INTO {} (".format(table)
        query += ("".join([str(fieldname) + ", " for fieldname in fieldNames]))[:-2] + ")"
        query += " VALUES ("
        query += ("".join(["?, " for _ in fieldNames]))[:-2] + ");"

        return query
    

def RunQuery(connection, cursor, query, *args):
    cursor.execute(query, *args)
    result = cursor.fetchall()
    connection.commit()
    return result

def ListTables(connection, cursor):
        
    query = "SELECT * FROM sqlite_master WHERE type='table'"

    result = RunQuery(connection, cursor, query)

    for i in result:
        print (i)

# -------------- #
# Code and stuff #
# -------------- #

if __name__ == "__main__":
    query = CreateQuerys.CreateRecord("Characters", ["Name", "FileName"])
    #RunQuery(connectionSQL, cursorSQL, query, ["Zero Two", ""])

    query = CreateQuerys.CreateRecord("CharacterTags", ["TagName"])
    #RunQuery(connectionSQL, cursorSQL, query, ["Age:14"])

    query = CreateQuerys.CreateRecord("CharacterTagsLink", ["CharacterID", "TagID"])
    #RunQuery(connectionSQL, cursorSQL, query, [1, 1])

    # Query to get all characters and tag links
    query = """
    SELECT * 
        FROM Characters JOIN (
            CharacterTagsLink JOIN CharacterTags
            ON CharacterTagsLink.TagID = CharacterTags.TagID
        )
    ON Characters.CharacterID = CharacterTagsLink.CharacterID
    """

    #print(queryVisualise(cursorSQL, query))

#print(tableVisualise(connectionSQL, "Characters"))
#print(advancedVisualise(
#    connectionSQL, 
#    ["Characters.CharacterID", "Characters.Name", "Characters.FileName", "CharacterTagsLink.LinkID", "CharacterTagsLink.CharacterID", "CharacterTagsLink.TagID", "CharacterTags.TagID", "CharacterTags.TagName"], 
#    result)
#)



# ----------------------- #
# Table Creation Commands #
# ----------------------- #

"""
CREATE TABLE UserVotes (
    VoteID INTEGER PRIMARY KEY,
    UserID INTEGER NOT NULL,
    CharacterID INTEGER NOT NULL,
    SetID INTEGER NOT NULL,
    Position INTEGER NOT NULL
);

CREATE TABLE Sets (
    SetID INTEGER PRIMARY KEY,
    SetName TEXT NOT NULL,
    FileName TEXT NOT NULL
);

CREATE TABLE SetTagsLink (
    LinkID INTEGER PRIMARY KEY,
    SetID INTEGER NOT NULL,
    TagID INTEGER NOT NULL
);

CREATE TABLE SetTags (
    TagID INTEGER PRIMARY KEY,
    TagName TEXT NOT NULL
);

CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);

CREATE TABLE Characters (
    CharacterID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    FileName TEXT NOT NULL
);

CREATE TABLE CharacterTagsLink (
    LinkID INTEGER PRIMARY KEY,
    CharacterID INTEGER NOT NULL,
    TagID INTEGER NOT NULL
);

CREATE TABLE CharacterTags (
    TagID INTEGER PRIMARY KEY,
    TagName TEXT NOT NULL
);

CREATE TABLE CharacterSetsLink (
    LinkID INTEGER PRIMARY KEY,
    CharacterID INTEGER NOT NULL,
    SetID INTEGER NOT NULL
)
"""

if __name__ == "__main__":
    connectionSQL.close()
    print("Completed all Tasks")
