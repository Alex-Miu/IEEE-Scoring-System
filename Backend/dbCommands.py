# File that contains functions that interact with the Database
from GUIs import ErrorPopup
from Resources import pymysql as mysql
from Backend import FormatData
from GUIs import DisplayGUI


# Attempts to connect to and authenticate with the specified Database.
# TODO connect to server then look for databases and connect to the one with the save name OR provide a list to the user hand have them choose one to connect to.
# WORKS
def Connect(dbName, dbIP, dbUser, dbPass, Data, dbTable, titleLabel, day):
    if Data.connected is True:
        ErrorPopup.ErrorPopup("005")
        return -1

    #bSaves connection information (but not to file)
    Data.dbName = dbName
    Data.dbIP = dbIP
    Data.dbUser = dbUser
    Data.dbPass = dbPass
    Data.dbTable = "`" + dbTable + "`"
    Data.today = day

    # Attempts to connect to server
    print("Attempting to connect...")

    try:
        Data.connection = mysql.connect(dbIP, dbUser, dbPass, dbName)
        Data.connected = True
        print("Connected to " + dbName + " at " + dbIP + " as " + dbUser)
        CycleThrough(Data)
        startTimer(Data, titleLabel)
    except Exception as error:
        ErrorPopup.ErrorPopup("001")
        print(error)


# Disconnects from the database
# WORKS
def CloseConnection(Data):
    if Data.connected is True:
        Data.connection.close()
        Data.connection = None
        Data.connected = False
        print("Disconnected")

# Gets all teams from the database that match the inputted settings, that is not meant to hide from display
def FetchTeams(data, competition_type):
    data.counter = 0

    if data.today == "Saturday":
        dateOfC = "  Saturday  "
    else:
        dateOfC = "  Sunday  "

    sql = "SELECT * FROM " + data.dbTable + " WHERE hide_from_display = 0 AND competition_type = '" + competition_type \
          + "' AND competition_day = '" + dateOfC + "' LIMIT " + str(data.MAXheight) + " OFFSET " + str(data.offset)
    print(sql)
    try:
        # Executes SQL Query
        cursor = data.connection.cursor()
        data.connection.begin()
        cursor.execute(sql)
        dataDump = cursor.fetchall()
        cursor.close()

        # Tests to see if we got any extra things
    except Exception as e:
        print(e)
        ErrorPopup.ErrorPopup("014")
        return -1

    print("SELECTION RECEIVED")

    # Sends received data off to formatting
    FormatData.InsertToTable(data, dataDump)

# Checks to see if there is a final results table available
def CheckForWinners(data):
    print("Checking for winner's table...")

    # Checks to see if there is a table named final_results
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = " + "'final_results'"

    try:
        cursor = data.connection.cursor()
        data.connection.begin()
        cursor.execute(sql)
        cursor.close()
        if cursor.fetchone()[0] == 1:
            print("WINNING TABLE DETECTED")
            data.endOfGame = True
        else:
            data.endOfGame = False
    except Exception as e:
        print(e)


# Function that switches to the next winner table
def SwitchToFinal(data):
    print("Switching to results data")
    data.showWinners = True
    data.counter = data.delay


def CycleThrough(data):
    if data.offset == 0:
        print("Switching to next item")
        newType = data.getNextType()
        data.displayTitle.set(newType)
    else:
        print("Getting next batch of category")
        newType = data.Types[data.index]
    FetchTeams(data, newType)


# Fetches winning teams of the correct category
def FetchWinningTeams(data, newType):

    # Determines the competition type based upon the newType input
    if newType == "  4-leg manual   ":
        sql = "SELECT * FROM final_results WHERE competition_type = '" + newType \
              + "' ORDER BY place_total LIMIT " + str(data.MAXheight) + " OFFSET " + str(data.offset)
    elif newType == "  2-leg overall  ":
        sql = "SELECT * FROM final_results WHERE  competition_type = '" + newType \
              + "' ORDER BY place_total LIMIT " + str(data.MAXheight) + " OFFSET " + str(data.offset)
    elif newType == "  2-leg manual   ":
        sql = "SELECT * FROM final_results WHERE competition_type = '" + newType \
              + "' ORDER BY place_total LIMIT " + str(data.MAXheight) + " OFFSET " + str(data.offset)
    elif newType == "  4-leg overall  ":
        sql = "SELECT * FROM final_results WHERE competition_type = '" + newType \
              + "' ORDER BY place_total LIMIT " + str(data.MAXheight) + " OFFSET " + str(data.offset)
    elif newType == "  2-leg  ":
        sql = "SELECT * FROM final_results WHERE competition_type = '  2-leg manual   ' OR competition_type = '  2-leg overall  ' LIMIT " + str(data.MAXheight) + " OFFSET " + str(data.offset)
    elif newType == "  4-leg  ":
        sql = "SELECT * FROM final_results WHERE competition_type = '  4-leg manual   ' OR competition_type = '  4-leg overall  ' LIMIT " + str(data.MAXheight) + " OFFSET " + str(data.offset)
    else:
        return -1

    print(sql)
    try:
        # Executes SQL Query
        cursor = data.connection.cursor()
        data.connection.begin()
        cursor.execute(sql)
        dataDump = cursor.fetchall()
        cursor.close()

        # Tests to see if we got any extra things
    except Exception as e:
        print(e)
        ErrorPopup.ErrorPopup("014")
        return -1

    print("SELECTION RECEIVED")

    # Sends received data off to formatting
    if newType == "  4-leg manual   ":
        FormatData.InsertToTable(data, dataDump)
    elif newType == "  2-leg overall  ":
        FormatData.InsertToTable(data, dataDump)
    elif newType == "  2-leg manual   ":
        FormatData.InsertToTable(data, dataDump)
    elif newType == "  4-leg overall  ":
        FormatData.InsertToTable(data, dataDump)
    elif newType == "  2-leg  ":
        FormatData.InsertToWinningTable(data, dataDump)
    elif newType == "  4-leg  ":
        FormatData.InsertToWinningTable(data, dataDump)
    else:
        return -1


# Cycles through the winner options
def CycleWinner(data):
    print("Cycling winner")
    data.counter = 0

    if data.offset == 0:
        print("Switching to next item")
        newType = data.getNextWinningType()
        if newType == "  4-leg manual   ":
            data.width = 13
        elif newType == "  2-leg overall  ":
            data.width = 13
        elif newType == "  2-leg manual   ":
            data.width = 13
        elif newType == "  4-leg overall  ":
            data.width = 13
        elif newType == "  2-leg  ":
            data.width = 10
        elif newType == "  4-leg  ":
            data.width = 10
        DisplayGUI.DrawWinnerWindow(data, newType)
        data.displayTitle.set(newType)
    else:
        print("Getting next batch of category")
        newType = data.ResultsCycle[data.index]

    FetchWinningTeams(data, newType)


# Sets up a 1 second timer
def startTimer(data, titleLabel):
    if data.connected is True:
        # Cycles to the next team if the counter is correct
        if int(data.counter) >= int(data.delay):
            if data.showWinners is True:
                CycleWinner(data)
            else:
                CycleThrough(data)
        else:
            data.counter += 1

        # Checks for the winning table
        CheckForWinners(data)

        titleLabel.after(1000, startTimer, data, titleLabel)
