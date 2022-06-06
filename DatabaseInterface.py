import sqlite3
from DatabaseManager import CreateQuerys, RunQuery
from TableVisualiser import *

class TerminalMessages:
    @staticmethod
    def Log(msg, funcName = "Unknown Function"):
        print(f"--> {funcName}: {msg}")

def CharacterTagsLink(connection, cursor, character, tag):
    
    #Check character exists
    query = f"SELECT CharacterID FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [character])

    if not result: #If the character dosent exist, cancel linking
        TerminalMessages.Log(f"Linking Failed: Character '{character}' not found", "CharacterTagsLink")
        return
    else:
        characterID = result[0][0]

    #Make sure tag exists
    query = f"SELECT TagID FROM CharacterTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [tag])

    if not result: #If the tag dosen't exist, create it
        TerminalMessages.Log(f"Tag '{tag}' does not exist, creating Tag: '{tag}'", "CharacterTagsLink")
        
        AddCharacterTag(connection, cursor, {"TagName" : tag})

        query = f"SELECT TagID FROM CharacterTags WHERE TagName = ?"
        result = RunQuery(connection, cursor, query, [tag])

    tagID = result[0][0]

    #Check if link already exists

    query = "SELECT * FROM CharacterTagsLink WHERE CharacterID = ? AND TagID = ?"
    result = RunQuery(connection, cursor, query, [characterID, tagID])

    if result: #If the link already exists, cencel linking
        TerminalMessages.Log(f"Linking failed: Link already exists between '{character}' and '{tag}'", "CharacterTagsLink")
        return

    #Create link if all tests passed
    query = CreateQuerys.CreateRecord("CharacterTagsLink", ["CharacterID", "TagID"])
    result = RunQuery(connection, cursor, query, [characterID, tagID])

def SetTagsLink(connection, cursor, set, tag):
    
    #Check set exists
    query = f"SELECT SetID FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [set])

    if not result: #If the set dosent exist, cancel linking
        TerminalMessages.Log(f"Linking Failed: Set '{set}' not found", "SetTagsLink")
        return
    else:
        setID = result[0][0]

    #Check tag exists
    query = f"SELECT TagID FROM SetTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [tag])

    if not result: #If the tag dosen't exist, create it
        TerminalMessages.Log(f"Tag '{tag}' does not exist, creating Tag: '{tag}'", "SetTagsLink")
        query = CreateQuerys.CreateRecord("SetTags", ["TagName"])
        RunQuery(connection, cursor, query, [tag])

        query = f"SELECT TagID FROM SetTags WHERE TagName = ?"
        result = RunQuery(connection, cursor, query, [tag])

    tagID = result[0][0]

    #Check if link already exists

    query = "SELECT * FROM SetTagsLink WHERE SetID = ? AND TagID = ?"
    result = RunQuery(connection, cursor, query, [setID, tagID])

    if result: #If the link already exists, cencel linking
        TerminalMessages.Log(f"Linking failed: Link already exists between '{set}' and '{tag}'", "SetTagsLink")
        return

    #Create link if all tests passed
    query = CreateQuerys.CreateRecord("SetTagsLink", ["SetID", "TagID"])
    result = RunQuery(connection, cursor, query, [setID, tagID])

def CharacterSetsLink(connection, cursor, character, set):

    #Check character exists
    query = f"SELECT CharacterID FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [character])

    if not result: #If the character dosen't exist, cancel linking
        TerminalMessages.Log(f"Linking Failed: Character '{character}' not found", "CharacterSetsLink")
        return
    else:
        characterID = result[0][0]

    #Check set exists
    query = f"SELECT SetID FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [set])

    if not result: #If the set dosent exist, cancel linking
        TerminalMessages.Log(f"Linking Failed: Set '{set}' not found", "CharacterSetsLink")
        return
    else:
        setID = result[0][0]

    #Check if link already exists
    query = "SELECT * FROM CharacterSetsLink WHERE CharacterID = ? AND SetID = ?"
    result = RunQuery(connection, cursor, query, [characterID, setID])

    if result: #If the link already exists, cencel linking
        TerminalMessages.Log(f"Linking failed: Link already exists between '{character}' and '{set}'", "CharacterSetsLink")
        return

    #Create link if all tests passed
    query = CreateQuerys.CreateRecord("CharacterSetsLink", ["CharacterID", "SetID"])
    result = RunQuery(connection, cursor, query, [characterID, setID])

def AddVote(connection, cursor, user, character, position, set):
    #Check User Exists
    query = "SELECT UserID FROM Users WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [user])

    if not result:
        TerminalMessages.Log(f"Adding Vote Failed: User '{user}' not found", "AddVote")
        return
    else:
        userID = result[0][0]

    #Check Character Exists
    query = "SELECT CharacterID FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [character])

    if not result:
        TerminalMessages.Log(f"Adding Vote Failed: Character '{character}' not found", "AddVote")
        return
    else:
        characterID = result[0][0]

    #Check Set Exists
    query = "SELECT SetID FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [set])

    if not result:
        TerminalMessages.Log(f"Adding Vote Failed: Set '{set}' not found", "AddVote")
        return
    else:
        setID = result[0][0]

    #Check Character is part of Set

    query = "SELECT LinkID FROM CharacterSetsLink WHERE CharacterID = ? AND SetID = ?"
    result = RunQuery(connection, cursor, query, [characterID, setID])

    if not result:
        TerminalMessages.Log(f"Adding Vote Failed: Character '{character}' not in Set '{set}'", "AddVote")
        return

    #Check Position is in range

    query = "SELECT COUNT(*) FROM CharacterSetsLink WHERE SetID = ?"
    result = RunQuery(connection, cursor, query, [setID])

    if position > result[0][0] or position <= 0:
        TerminalMessages.Log(f"Adding Vote Failed: position '{position}' out of range", "AddVote")
        return

    #Check Position isnt already taken

    query = "SELECT VoteID FROM UserVotes WHERE UserID = ? AND SetID = ? AND Position = ?"
    result = RunQuery(connection, cursor, query, [userID, setID, position])

    if result:
        TerminalMessages.Log(f"Adding Vote Failed: position '{position}' already has vote registered", "AddVote")
        return

    #Add User Vote if all checks passed
    query = CreateQuerys.CreateRecord("UserVotes", ["UserID", "CharacterID", "Position", "SetID"])
    result = RunQuery(connection, cursor, query, [userID, characterID, position, setID])

def AddUser(connection, cursor, data : dict):

    query = "SELECT * FROM Users WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [data["Name"]])

    if result:
        TerminalMessages.Log(f"Adding User Failed: User '{data['Name']}' Already Exists", "AddUser")
        return
    else:
        query = CreateQuerys.CreateRecord("Users", ["Name"])
        RunQuery(connection, cursor, query, [data["Name"]])

def AddCharacter(connection, cursor, data : dict):

    query = "SELECT * FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [data["Name"]])

    if result:
        TerminalMessages.Log(f"Adding Character Failed: Character '{data['Name']}' Already Exists", "AddCharacter")
        return
    else:
        query = CreateQuerys.CreateRecord("Characters", ["Name", "FileName"])
        RunQuery(connection, cursor, query, [data["Name"], data["FileName"]])

def AddCharacterTag(connection, cursor, data : dict):
    
    query = "SELECT * FROM CharacterTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [data["TagName"]])

    if result:
        TerminalMessages.Log(f"Adding Character Tag Failed: Tag '{data['TagName']}' Already Exists", "AddCharacterTags")
        return
    else:
        query = CreateQuerys.CreateRecord("CharacterTags", ["TagName"])
        RunQuery(connection, cursor, query, [data["TagName"]])

def AddSet(connection, cursor, data : dict):
    
    query = "SELECT * FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [data["SetName"]])

    if result:
        TerminalMessages.Log(f"Adding Set Failed: Set '{data['SetName']}' Already Exists", "AddSet")
        return
    else:
        query = CreateQuerys.CreateRecord("Sets", ["SetName", "FileName"])
        RunQuery(connection, cursor, query, [data["SetName"], data["FileName"]])

def AddSetTag(connection, cursor, data : dict):
    
    query = "SELECT * FROM SetTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [data["TagName"]])

    if result:
        TerminalMessages.Log(f"Adding Set Tag Failed: Set Tag '{data['TagName']}' Already Exists", "AddSetTag")
        return
    else:
        query = CreateQuerys.CreateRecord("SetTags", ["TagName"])
        RunQuery(connection, cursor, query, [data["TagName"]])

connectionSQL = sqlite3.connect("TypeFinder.db")
cursorSQL = connectionSQL.cursor()

#AddUser(connectionSQL, cursorSQL, {"Name" : "Travis"})
#AddCharacter(connectionSQL, cursorSQL, {"Name" : "Hachi", "FileName" : ""})
#AddSet(connectionSQL, cursorSQL, {"SetName" : "DARLING in the FRANXX", "FileName" : "DARLING in the FRANXX characters.png"})

#CharacterTagsLink(connectionSQL, cursorSQL, "Zero Two", "HairColour:Pink")
#SetTagsLink(connectionSQL, cursorSQL, "DARLING in the FRANXX", "Genre:Anime")
#CharacterSetsLink(connectionSQL, cursorSQL, "Hachi", "DARLING in the FRANXX")

"""
AddVote(connectionSQL, cursorSQL, "Elissa", "Kokoro", 1, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Hiro", 2, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Miku", 3, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Naomi", 4, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Nana", 5, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Ichigo", 6, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Zero Two", 7, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Zorome", 8, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Ikuno", 9, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Goro", 10, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Mitsuru", 11, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Hachi", 12, "DARLING in the FRANXX")
AddVote(connectionSQL, cursorSQL, "Elissa", "Futoshi", 13, "DARLING in the FRANXX")
"""

query = """
    SELECT Sets.SetName, SetTags.TagName
        FROM Sets JOIN (
            SetTagsLink JOIN SetTags
            ON SetTagsLink.TagID = SetTags.TagID
        )
    ON Sets.SetID = SetTagsLink.SetID
"""

query = """
    SELECT Users.Name, Characters.Name, Sets.SetName, UserVotes.Position FROM UserVotes 
        JOIN Users ON UserVotes.UserID = Users.UserID
        JOIN Characters ON UserVotes.CharacterID = Characters.CharacterID
        JOIN Sets ON UserVotes.SetID = Sets.SetID
    ORDER BY Uservotes.Position, Users.Name
"""

query = """
    SELECT Users.Name, Characters.Name, UserVotes.Position FROM UserVotes
        JOIN Users ON UserVotes.UserID = Users.UserID
        JOIN Characters ON UserVotes.CharacterID = Characters.CharacterID
    ORDER BY Users.Name, UserVotes.Position
"""

query = """
    SELECT Characters.Name FROM Sets
        JOIN CharacterSetsLink ON Sets.SetID = CharacterSetsLink.SetID
        JOIN Characters ON CharacterSetsLink.CharacterID = Characters.CharacterID
    WHERE Sets.SetName = ?
"""

#print(queryVisualise(cursorSQL, query))

print(tableVisualise(connectionSQL, "Users"))
print(tableVisualise(connectionSQL, "UserVotes"))
print(tableVisualise(connectionSQL, "Characters"))
print(tableVisualise(connectionSQL, "CharacterTagsLink"))
print(tableVisualise(connectionSQL, "CharacterTags"))
print(tableVisualise(connectionSQL, "Sets"))
print(tableVisualise(connectionSQL, "SetTagsLink"))
print(tableVisualise(connectionSQL, "SetTags"))
print(tableVisualise(connectionSQL, "CharacterSetsLink"))

