import sqlite3
import json
from DatabaseInterface import *
from DatabaseManager import RunQuery, CreateQuerys

"""
JSON Format:

[
    {
        meta :  {
            name : str,
            fields : [
                fieldname1,
                fieldname2,
                etc
            ]
        },
        data : [
            [
                field1,
                field2,
                etc.
            ],
            etc.
        ]
    },
    etc.
]

"""

def Import(databaseName, dataFile, order = None):
    # Create connection and cursor for the database
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    # Export the json file into a variable
    with open(dataFile, "r") as file:
        jsonData = json.loads(file.read())

    # Get a list of all tables in the database
    query = "SELECT * FROM sqlite_master WHERE type='table'"

    databaseTables = [table[1] for table in RunQuery(connection, cursor, query)]
    dataTables = [table["meta"]["name"] for table in jsonData]

    # Check all the tables in the json file match the database
    invalidTables = [table for table in dataTables if table not in databaseTables]

    if invalidTables:
        print(invalidTables)
        return

    # Check all table fields match the ones in the database
    for table in jsonData:
        query = f"PRAGMA table_info({table['meta']['name']})"
        tableFields = [field[1] for field in RunQuery(connection, cursor, query)]

        if list(tableFields) != table['meta']['fields']:
            print(list(tableFields))
            print(table['meta']['fields'])
            return
    
    # Check the data is in order if necesarry
    orderedData = []
    if order:
        for tableName in order:
            for table in jsonData:
                if table['meta']['name'] == tableName:
                    orderedData.append(table)
    else:
        orderedData = jsonData
    
    # Import the data into the database
    for table in orderedData:
        query = CreateQuerys.CreateRecord(table['meta']['name'], table['meta']['fields'])
        tableData = table['data']
        for data in tableData:
            print(f"Importing Data {data} into {table['meta']['name']}")
            RunQuery(connection, cursor, query, data)

def ExportData(databaseName, tables = None, file = "Data.json"):
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    jsonData = []

    query = "SELECT * FROM sqlite_master WHERE type='table'"
    if not tables:
        tables = [table[1] for table in RunQuery(connection, cursor, query)]

    for table in tables:
        query = f"SELECT * FROM {table}"
        tableData = [list(record) for record in RunQuery(connection, cursor, query)]

        query = f"PRAGMA table_info({table})"
        tableFields = [field[1] for field in RunQuery(connection, cursor, query)]

        jsonData.append({
            "meta" : {
                "name" : table,
                "fields" : list(tableFields)
            },
            "data" : tableData
        })

    with open(file, "w") as jsonFile:
        jsonFile.write(json.dumps(jsonData))

def ExportTemplate(databaseName, tables = None, file = "Data.json"):
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    jsonData = []

    query = "SELECT * FROM sqlite_master WHERE type='table'"

    if not tables:
        tables = [table[1] for table in RunQuery(connection, cursor, query)]

    for table in tables:
        query = f"SELECT * FROM {table}"
        tableData = [list(record) for record in RunQuery(connection, cursor, query)]

        query = f"PRAGMA table_info({table})"
        tableFields = [field[1] for field in RunQuery(connection, cursor, query)]

        jsonData.append({
            "meta" : {
                "name" : table,
                "fields" : list(tableFields)
            },
            "data" : []
        })

    with open(file, "w") as jsonFile:
        jsonFile.write(json.dumps(jsonData))
