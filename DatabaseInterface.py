import sqlite3
from DatabaseManager import CreateQuerys, RunQuery, ListTables, DeletingRecords
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
        TerminalMessages.Log(f"Linking Failed: Character {character} not found", "CharacterTagsLink")
        return
    else:
        characterID = result[0][0]

    #Check tag exists
    query = f"SELECT TagID FROM CharacterTags WHERE TagName = ?"
    result = RunQuery(connection, cursor, query, [tag])

    if not result: #If the tag dosen't exist, create it
        TerminalMessages.Log(f"Tag '{tag}' does not exist, creating Tag: '{tag}'", "CharacterTagsLink")
        query = CreateQuerys.CreateRecord("CharacterTags", ["TagName"])
        RunQuery(connection, cursor, query, [tag])

        query = f"SELECT TagID FROM CharacterTags WHERE TagName = ?"
        result = RunQuery(connection, cursor, query, [tag])

    tagID = result[0][0]

    #Check if link already exists

    query = "SELECT * FROM CharacterTagsLink WHERE CharacterID = ? AND TagID = ?"
    result = RunQuery(connection, cursor, query, [characterID, tagID])

    if result: #If the link already exists, cencel linking
        TerminalMessages.Log(f"Linking failed: Link already exists between {character} and {tag}", "CharacterTagsLink")
        return

    #Create link if all tests passed
    query = CreateQuerys.CreateRecord("CharacterTagsLink", ["CharacterID", "TagID"])
    result = RunQuery(connection, cursor, query, [characterID, tagID])


connectionSQL = sqlite3.connect("TypeFinder.db")
cursorSQL = connectionSQL.cursor()

#ListTables(connectionSQL, cursorSQL)
CharacterTagsLink(connectionSQL, cursorSQL, "Zero Two", "Gender:Female")

query = """
    SELECT Characters.Name, CharacterTags.TagName
        FROM Characters JOIN (
            CharacterTagsLink JOIN CharacterTags
            ON CharacterTagsLink.TagID = CharacterTags.TagID
        )
    ON Characters.CharacterID = CharacterTagsLink.CharacterID
"""

print(queryVisualise(cursorSQL, query))
