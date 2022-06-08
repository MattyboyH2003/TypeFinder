import JSONInterfacing
from DatabaseInterface import *

# ------- #
# Queries #
# ------- #

tableQueries = """
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

query1 = """
    SELECT Users.Name, Characters.Name, Sets.SetName, UserVotes.Position FROM UserVotes 
        JOIN Users ON UserVotes.UserID = Users.UserID
        JOIN Characters ON UserVotes.CharacterID = Characters.CharacterID
        JOIN Sets ON UserVotes.SetID = Sets.SetID
    ORDER BY Uservotes.Position, Users.Name
"""

query2 = """
    SELECT Users.Name, Characters.Name, UserVotes.Position FROM UserVotes
        JOIN Users ON UserVotes.UserID = Users.UserID
        JOIN Characters ON UserVotes.CharacterID = Characters.CharacterID
    ORDER BY Users.Name, UserVotes.Position
"""

query3 = """
    SELECT Characters.Name FROM Sets
        JOIN CharacterSetsLink ON Sets.SetID = CharacterSetsLink.SetID
        JOIN Characters ON CharacterSetsLink.CharacterID = Characters.CharacterID
    WHERE Sets.SetName = ?
"""


# -------------- #
# Code and Stuff #
# -------------- #

DATABASE = "test.db"
DATAFILE = "Data.json"

connectionSQL = sqlite3.connect(DATABASE)
cursorSQL = connectionSQL.cursor()


#cursorSQL.executescript(tableQueries)
#connectionSQL.commit()


#AddUser(connectionSQL, cursorSQL, {"Name" : "Travis"})
#AddCharacter(connectionSQL, cursorSQL, {"Name" : "Hachi", "FileName" : ""})
#AddSet(connectionSQL, cursorSQL, {"SetName" : "DARLING in the FRANXX", "FileName" : "DARLING in the FRANXX characters.png"})

#CharacterTagsLink(connectionSQL, cursorSQL, "Zero Two", "HairColour:Pink")
#SetTagsLink(connectionSQL, cursorSQL, "DARLING in the FRANXX", "Genre:Anime")
#CharacterSetsLink(connectionSQL, cursorSQL, "Hachi", "DARLING in the FRANXX")

#CharactersAndTags(connectionSQL, cursorSQL, scope = "Characters.Name, CharacterTags.TagName", visualise = True)
#SetsAndTags(connectionSQL, cursorSQL, scope = "Sets.SetName, SetTags.TagName", visualise = True)
#UsersAndVotes(connectionSQL, cursorSQL, visualise = True, order = "Users.UserID, UserVotes.Position")
#SetsAndCharacters(connectionSQL, cursorSQL, scope = "Sets.SetName, Characters.Name" , visualise = True)


#print(tableVisualise(connectionSQL, "Users"))
#print(tableVisualise(connectionSQL, "UserVotes"))
#print(tableVisualise(connectionSQL, "Characters"))
#print(tableVisualise(connectionSQL, "CharacterTagsLink"))
#print(tableVisualise(connectionSQL, "CharacterTags"))
#print(tableVisualise(connectionSQL, "Sets"))
#print(tableVisualise(connectionSQL, "SetTagsLink"))
#print(tableVisualise(connectionSQL, "SetTags"))
#print(tableVisualise(connectionSQL, "CharacterSetsLink"))
