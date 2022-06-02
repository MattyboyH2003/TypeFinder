
def _visualiseBase(fieldNames, resultData):

    #This section calculates the length of the longest piece of data in each field
    longestPieceOfData = []
    counter = 0
    for fieldName in fieldNames: 
        longestLength = len(fieldName)
        for record in resultData:
            if longestLength < len(str(record[counter])):
                longestLength = len(record[counter])
        longestPieceOfData.append(longestLength)
        counter += 1

    #This section constructs and outputs the table
    visualised = ""

    #This section outputs the upper line
    output = "╔═"
    for item in longestPieceOfData:
        for i in range(0,item):
            output += "═"
        output += "═╤═"
    output = output[0:(len(output)-3)]
    output += "═╗"
    visualised += output + "\n"

    #This section outputs the field names
    output = "║ "
    columnNum = 0
    for fieldName in fieldNames:
        spaces = ""
        if len(fieldName) < longestPieceOfData[columnNum]:
            addedSpaces = longestPieceOfData[columnNum] - len(fieldName)
            spaces = " "*addedSpaces
        output += fieldName + spaces + " │ "
        columnNum += 1
    output = output[0:(len(output)-2)]
    output += "║"
    visualised += output + "\n"

    #This section adds the divider between field names and the records
    output = "╠═"
    for item in longestPieceOfData:
        for i in range(0,item):
            output += "═"
        output += "═╪═"
    output = output[0:(len(output)-3)]
    output += "═╣"
    visualised += output + "\n"

    #This section outputs all the records in the table
    for item in resultData:
        record = item
        output = "║ "
        columnNum = 0
        for data in record:
            spaces = ""
            if len(str(data)) < longestPieceOfData[columnNum]:
                addedSpaces = longestPieceOfData[columnNum] - len(str(data))
                for i in range(0,addedSpaces):
                    spaces += " "
            output += str(data) + spaces + " │ "
            columnNum += 1
        output = output[0:(len(output)-2)]
        output += "║"
        visualised += output + "\n"

    #This section outputs the bottom line
    output = "╚═"
    for item in longestPieceOfData:
        for i in range(0,item):
            output += "═"
        output += "═╧═"
    output = output[0:(len(output)-3)]
    output += "═╝"
    visualised += output + "\n"

    return(visualised)

def tableVisualise(connectionSQL, table):
    
    cursorSQL = connectionSQL.cursor()
    
    #This section gets the names of all columns in a table
    query = ("PRAGMA table_info({})").format(table)
    cursorSQL.execute(query)
    result = cursorSQL.fetchall()
    fieldNames =  []
    for i in range(0, len(result)):
        fieldNames.append(result[i][1])

    #This section gets the number of records in a table
    query = ("SELECT * FROM {}").format(table)
    cursorSQL.execute(query)
    result = cursorSQL.fetchall()

    visualised = _visualiseBase(fieldNames, result)

    connectionSQL.close()

    return visualised

def advancedVisualise(connectionSQL, fieldNames, resultData):
    visualised = _visualiseBase(fieldNames, resultData)

    connectionSQL.close()

    return visualised

def queryVisualise(cursorSQL, query):

    frompos = -1
    for i in range(0, len(query) - 4):
        segment = query[i:i+4]
        if segment == "FROM":
            frompos = i
            break

    selectpos = -1
    for i in range(0, len(query) - 6):
        segment = query[i:i+6]
        if segment == "SELECT":
            selectpos = i+6
            break

    fields = query[selectpos:frompos]
    fields = fields.replace(" ", "")
    fields = fields.replace("\n", "")

    if fields == "*":
        BLACKLIST = ["", "JOIN", "SELECT", "ON", "="]
        querySegments = query[frompos+5:].split(" ")
        
        for i in range(0, len(querySegments)):
            querySegments[i] = querySegments[i].replace("\n", "")
            querySegments[i] = querySegments[i].replace(")", "")
            querySegments[i] = querySegments[i].replace("(", "")

        removedItems = 0
        for i in range(0, len(querySegments)):
            for item in BLACKLIST:
                if querySegments[i-removedItems] == item:
                    querySegments.remove(item)
                    removedItems += 1
                    break
        removedItems = 0
        for i in range(0, len(querySegments)):
            if '.' in querySegments[i-removedItems]:
                querySegments.remove(querySegments[i-removedItems])
                removedItems += 1

        fieldNames = []
        for table in querySegments:
            pragmaQuery = ("PRAGMA table_info({})").format(table)
            cursorSQL.execute(pragmaQuery)
            result = cursorSQL.fetchall()
            for i in range(0, len(result)):
                fieldNames.append(table + "." + result[i][1])

    else:
        fieldNames = fields.split(",")
    
    cursorSQL.execute(query)
    result = cursorSQL.fetchall()

    visualised = _visualiseBase(fieldNames, result)

    return visualised
