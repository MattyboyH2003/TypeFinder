import sqlite3
from TableVisualiser import *

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

