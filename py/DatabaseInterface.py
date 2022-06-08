import sqlite3
from DatabaseManager import CreateQuerys, RunQuery
from TableVisualiser import *

class _TerminalMessages:
    @staticmethod
    def Log(msg, funcName = "Unknown Function"):
        print(f"--> {funcName}: {msg}")

#
# Adding Data
#

def AddUser(connection, cursor, data : dict):

    # Check the user isn't already in the database
    query = "SELECT * FROM Users WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [data["Name"]])

    if result: # If the user is already in the database
        _TerminalMessages.Log(f"Adding User Failed: User '{data['Name']}' Already Exists", "AddUser")
        return
    else: # If the user is not already in the database
        query = CreateQuerys.CreateRecord("Users", ["Name"])
        RunQuery(connection, cursor, query, [data["Name"]])

def AddCharacter(connection, cursor, data : dict):

    # Checks if the character already exists in the database
    query = "SELECT * FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [data["Name"]])

    if result: # If the character already exists in the database
        _TerminalMessages.Log(f"Adding Character Failed: Character '{data['Name']}' Already Exists", "AddCharacter")
        return
    else: # If the character dosen't already exist in the database
        query = CreateQuerys.CreateRecord("Characters", ["Name", "FileName"])
        RunQuery(connection, cursor, query, [data["Name"], data["FileName"]])

def AddCharacterTag(connection, cursor, data : dict):
    
    # Checks if the character tag already exists in the database
    query = "SELECT * FROM CharacterTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [data["TagName"]])

    if result: # If the character tag already exists in the database
        _TerminalMessages.Log(f"Adding Character Tag Failed: Tag '{data['TagName']}' Already Exists", "AddCharacterTags")
        return
    else: # If the character tag dosen't already exist in the database
        query = CreateQuerys.CreateRecord("CharacterTags", ["TagName"])
        RunQuery(connection, cursor, query, [data["TagName"]])

def AddSet(connection, cursor, data : dict):
    
    # Check if the set already exists in the database
    query = "SELECT * FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [data["SetName"]])

    if result: # If the set already exists in the database
        _TerminalMessages.Log(f"Adding Set Failed: Set '{data['SetName']}' Already Exists", "AddSet")
        return
    else: # If the set dosen't already exist in the database
        query = CreateQuerys.CreateRecord("Sets", ["SetName", "FileName"])
        RunQuery(connection, cursor, query, [data["SetName"], data["FileName"]])

def AddSetTag(connection, cursor, data : dict):
    
    # Check if the set tag already exists in the database
    query = "SELECT * FROM SetTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [data["TagName"]])

    if result: # If the set tag already exists in the database
        _TerminalMessages.Log(f"Adding Set Tag Failed: Set Tag '{data['TagName']}' Already Exists", "AddSetTag")
        return
    else: # If the set tag dosen't already exist in the database
        query = CreateQuerys.CreateRecord("SetTags", ["TagName"])
        RunQuery(connection, cursor, query, [data["TagName"]])


def CharacterTagsLink(connection, cursor, character, tag):
    
    #Check character exists
    query = f"SELECT CharacterID FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [character])

    if not result: #If the character dosent exist, cancel linking
        _TerminalMessages.Log(f"Linking Failed: Character '{character}' not found", "CharacterTagsLink")
        return
    else:
        characterID = result[0][0]

    #Make sure tag exists
    query = f"SELECT TagID FROM CharacterTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [tag])

    if not result: #If the tag dosen't exist, create it
        _TerminalMessages.Log(f"Tag '{tag}' does not exist, creating Tag: '{tag}'", "CharacterTagsLink")
        
        AddCharacterTag(connection, cursor, {"TagName" : tag})

        query = f"SELECT TagID FROM CharacterTags WHERE TagName = ?"
        result = RunQuery(connection, cursor, query, [tag])

    tagID = result[0][0]

    #Check if link already exists

    query = "SELECT * FROM CharacterTagsLink WHERE CharacterID = ? AND TagID = ?"
    result = RunQuery(connection, cursor, query, [characterID, tagID])

    if result: #If the link already exists, cencel linking
        _TerminalMessages.Log(f"Linking failed: Link already exists between '{character}' and '{tag}'", "CharacterTagsLink")
        return

    #Create link if all tests passed
    query = CreateQuerys.CreateRecord("CharacterTagsLink", ["CharacterID", "TagID"])
    result = RunQuery(connection, cursor, query, [characterID, tagID])

def SetTagsLink(connection, cursor, set, tag):
    
    #Check set exists
    query = f"SELECT SetID FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [set])

    if not result: #If the set dosent exist, cancel linking
        _TerminalMessages.Log(f"Linking Failed: Set '{set}' not found", "SetTagsLink")
        return
    else:
        setID = result[0][0]

    #Check tag exists
    query = f"SELECT TagID FROM SetTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [tag])

    if not result: #If the tag dosen't exist, create it
        _TerminalMessages.Log(f"Tag '{tag}' does not exist, creating Tag: '{tag}'", "SetTagsLink")
        query = CreateQuerys.CreateRecord("SetTags", ["TagName"])
        RunQuery(connection, cursor, query, [tag])

        query = f"SELECT TagID FROM SetTags WHERE TagName = ?"
        result = RunQuery(connection, cursor, query, [tag])

    tagID = result[0][0]

    #Check if link already exists

    query = "SELECT * FROM SetTagsLink WHERE SetID = ? AND TagID = ?"
    result = RunQuery(connection, cursor, query, [setID, tagID])

    if result: #If the link already exists, cencel linking
        _TerminalMessages.Log(f"Linking failed: Link already exists between '{set}' and '{tag}'", "SetTagsLink")
        return

    #Create link if all tests passed
    query = CreateQuerys.CreateRecord("SetTagsLink", ["SetID", "TagID"])
    result = RunQuery(connection, cursor, query, [setID, tagID])

def CharacterSetsLink(connection, cursor, character, set):

    #Check character exists
    query = f"SELECT CharacterID FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [character])

    if not result: #If the character dosen't exist, cancel linking
        _TerminalMessages.Log(f"Linking Failed: Character '{character}' not found", "CharacterSetsLink")
        return
    else:
        characterID = result[0][0]

    #Check set exists
    query = f"SELECT SetID FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [set])

    if not result: #If the set dosent exist, cancel linking
        _TerminalMessages.Log(f"Linking Failed: Set '{set}' not found", "CharacterSetsLink")
        return
    else:
        setID = result[0][0]

    #Check if link already exists
    query = "SELECT * FROM CharacterSetsLink WHERE CharacterID = ? AND SetID = ?"
    result = RunQuery(connection, cursor, query, [characterID, setID])

    if result: #If the link already exists, cencel linking
        _TerminalMessages.Log(f"Linking failed: Link already exists between '{character}' and '{set}'", "CharacterSetsLink")
        return

    #Create link if all tests passed
    query = CreateQuerys.CreateRecord("CharacterSetsLink", ["CharacterID", "SetID"])
    result = RunQuery(connection, cursor, query, [characterID, setID])


def AddVote(connection, cursor, user, character, position, set):
    #Check User Exists
    query = "SELECT UserID FROM Users WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [user])

    if not result:
        _TerminalMessages.Log(f"Adding Vote Failed: User '{user}' not found", "AddVote")
        return
    else:
        userID = result[0][0]

    #Check Character Exists
    query = "SELECT CharacterID FROM Characters WHERE Name = ?"
    result = RunQuery(connection, cursor, query, [character])

    if not result:
        _TerminalMessages.Log(f"Adding Vote Failed: Character '{character}' not found", "AddVote")
        return
    else:
        characterID = result[0][0]

    #Check Set Exists
    query = "SELECT SetID FROM Sets WHERE SetName = ?"
    result = RunQuery(connection, cursor, query, [set])

    if not result:
        _TerminalMessages.Log(f"Adding Vote Failed: Set '{set}' not found", "AddVote")
        return
    else:
        setID = result[0][0]

    #Check Character is part of Set

    query = "SELECT LinkID FROM CharacterSetsLink WHERE CharacterID = ? AND SetID = ?"
    result = RunQuery(connection, cursor, query, [characterID, setID])

    if not result:
        _TerminalMessages.Log(f"Adding Vote Failed: Character '{character}' not in Set '{set}'", "AddVote")
        return

    #Check Position is in range

    query = "SELECT COUNT(*) FROM CharacterSetsLink WHERE SetID = ?"
    result = RunQuery(connection, cursor, query, [setID])

    if position > result[0][0] or position <= 0:
        _TerminalMessages.Log(f"Adding Vote Failed: position '{position}' out of range", "AddVote")
        return

    #Check Position isnt already taken

    query = "SELECT VoteID FROM UserVotes WHERE UserID = ? AND SetID = ? AND Position = ?"
    result = RunQuery(connection, cursor, query, [userID, setID, position])

    if result:
        _TerminalMessages.Log(f"Adding Vote Failed: position '{position}' already has vote registered", "AddVote")
        return

    #Add User Vote if all checks passed
    query = CreateQuerys.CreateRecord("UserVotes", ["UserID", "CharacterID", "Position", "SetID"])
    result = RunQuery(connection, cursor, query, [userID, characterID, position, setID])



#
# Advanced Data Retrieval
#

def CharactersAndTags(connection, cursor, character = "", scope = "*", order = "", visualise = False):

    if character:
        # Check the character exists
        query = "SELECT * FROM Characters WHERE Name = ?"
        result = RunQuery(connection, cursor, query, [character])

        if not result: # If the character already exists in the database
            _TerminalMessages.Log(f"Getting Character Tags Failed: Character '{character}' Does not Exist", "CharactersAndTags")
            return None

    # Query to get data
    query = f"""
    SELECT {scope} FROM Characters 
        JOIN CharacterTagsLink ON Characters.CharacterID = CharacterTagsLink.CharacterID
        JOIN CharacterTags ON CharacterTagsLink.TagID = CharacterTags.TagID
    """
    args = []
    
    # If a specific character is requested
    if character:
        query += " WHERE Characters.Name = ?"
        args = [character]

    if order:
        query += f" ORDER BY {order}"

    if visualise:
        print(queryVisualise(cursor, query, args))

    # Return the data
    return RunQuery(connection, cursor, query, args)

def SetsAndTags(connection, cursor, set = "", scope = "*", order = "", visualise = False):
    if set:
        # Check the set exists
        query = "SELECT * FROM Sets WHERE SetName = ?"
        result = RunQuery(connection, cursor, query, [set])

        if not result: # If the set already exists in the database
            _TerminalMessages.Log(f"Getting Set Tags Failed: Set '{set}' Does not Exist", "SetsAndTags")
            return None

    # Query to get data
    query = f"""
    SELECT {scope} FROM Sets 
        JOIN SetTagsLink ON Sets.SetID = SetTagsLink.SetID
        JOIN SetTags ON SetTagsLink.TagID = SetTags.TagID
    """
    args = []

    if set:
        query +=" WHERE Sets.SetName = ?"
        args = [set]
    
    if order:
        query += f" ORDER BY {order}"

    if visualise:
        print(queryVisualise(cursor, query, args))

    # Return the data
    return RunQuery(connection, cursor, query, args)

def UsersAndVotes(connection, cursor, user = "", scope = "*", order = "", visualise = False):
    if user:
        # Check the user exists
        query = "SELECT * FROM Users WHERE Name = ?"
        result = RunQuery(connection, cursor, query, [user])

        if not result: # If the character already exists in the database
            _TerminalMessages.Log(f"Getting User Votes Failed: User '{user}' Does not Exist", "UsersAndVotes")
            return None

    # Query to get data
    query = f"""
    SELECT {scope} FROM Users 
        JOIN UserVotes ON Users.UserID = UserVotes.UserID
    """
    args = []

    if user:
        query += " WHERE Users.Name = ?"
        args = [user]

    if order:
        query += f" ORDER BY {order}"

    print(query)

    if visualise:
        print(queryVisualise(cursor, query, args))

    # Return the result
    return RunQuery(connection, cursor, query, args)

def SetsAndCharacters(connection, cursor, set = "", scope = "*", order = "", visualise = False):
    if set:
        # Check the set exists
        query = "SELECT * FROM Sets WHERE Name = ?"
        result = RunQuery(connection, cursor, query, [set])

        if not result: # If the set already exists in the database
            _TerminalMessages.Log(f"Getting Set Characters Failed: Set '{set}' Does not Exist", "SetsAndCharacters")
            return None

    # Query to get data
    query = f"""
    SELECT {scope} FROM Sets 
        JOIN CharacterSetsLink ON Sets.SetID = CharacterSetsLink.SetID
        JOIN Characters ON CharacterSetsLink.CharacterID = Characters.CharacterID
    """
    args = []

    if set:
        query += " WHERE Sets.SetName = ?"
        args = [set]

    if order:
        query += f" ORDER BY {order}"

    print(query)

    if visualise:
        print(queryVisualise(cursor, query, args))

    # Return the result
    return RunQuery(connection, cursor, query, args)
