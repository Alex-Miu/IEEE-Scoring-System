from GUIs import ErrorPopup
from GUIs import SettingsGUI
from tkinter import *
import pymysql as mysql
from Backend import ExportManager
import time
# Small test used by search
# WORKS
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# Attempts to connect to and authenticate with the specified Database.
# TODO connect to server then look for databases and either make a new one or connect to the one with the save name
# TODO OR provide a list to the user hand have them choose one to connect to or to make a new one.
# WORKS
def Connect(dbName, dbIP, dbUser, dbPass, Data, dbTable, listBox):
    if Data.connected is True:
        ErrorPopup.ErrorPopup("005")
        return -1

    #Saves connection information (but not to file)
    Data.dbName = dbName
    Data.dbIP = dbIP
    Data.dbUser = dbUser
    Data.dbPass = dbPass
    Data.dbTable = "`" + dbTable + "`"

    # Attempts to connect to server
    Data.systemText.set("Attempting to connect...")
    Data.displayTimer = 0

    try:
        Data.connection = mysql.connect(dbIP, dbUser, dbPass, dbName)
        Data.connected = True
        UpdateList(Data, listBox)
        Data.systemText.set("Connected to " + dbName + " at " + dbIP + " as " + dbUser)
        Data.displayTimer = 0

    except Exception as error:
        ErrorPopup.ErrorPopup("001")
        Data.systemText.set(error)
        Data.displayTimer = 0


# Imports a bunch of data given the format and the file name.
# Format is either for the written report scores or the teams.
# Only imports utf8-csv files.
# WORKS
def ImportData(filename, dataformat, Data):
    print("Selection: " + dataformat)

    newTableName = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    if "Written Report Scores" in dataformat:
            print(">>>INITIATING IMPORT")
        # Get the formatted information
            listOfStrings = ExportManager.GenerateStringsReportStyle(filename, Data)
            if listOfStrings == -1:
                return -1

            print("LIST OF STRINGS")
            print(listOfStrings)
            print("\n")

            if Data.connected is False:
                ErrorPopup.ErrorPopup("010")
                Data.systemText.set("Failed to import data into database - no connection")
                Data.displayTimer = 0
                return -1

            try:
                print("Building Cursor...")
                # Execute the SQL command
                cursor = Data.connection.cursor()
                for insertCommand in listOfStrings:
                    sql = "UPDATE " + Data.dbTable + insertCommand
                    print(sql)
                    Data.systemText.set(sql)
                    Data.displayTimer = 0

                    cursor.execute(sql)

                # Commits all changes and closes connection
                print("Committing changes...")
                Data.connection.commit()
                cursor.close()

                # Relays success
                Data.systemText.set("Committed imported data to connected table")
                Data.displayTimer = 0
            except Exception as error:
                ErrorPopup.ErrorPopup("011")
                Data.systemText.set(error)
                Data.displayTimer = 0

    # handles other excel format.
    elif "Team Information" in dataformat:
            # Get the formatted information
            listOfInfo = ExportManager.GenerateListForImport(filename, Data)
            if listOfInfo == -1:
                return -1

            print("\n>>>INITIATING IMPORT")
            if Data.connected is False:
                ErrorPopup.ErrorPopup("010")
                Data.systemText.set("Failed to import data into database - no connection")
                Data.displayTimer = 0
                return -1

            try:
                # Execute the SQL command

                # Generates a new table TODO check to make sure table doesn't already exist
                cursor = Data.connection.cursor()
                sql = "CREATE TABLE `" + newTableName + "` (" + \
                        "`name` varchar(100) NOT NULL, " + \
                        "`number` int(11) NOT NULL, " + \
                        "`school` varchar(100) DEFAULT NULL, " + \
                        "`written_report_score` decimal(4,0) DEFAULT NULL, " + \
                        "`fabrication_score` decimal(4,0) DEFAULT NULL, " + \
                        "`track_run_1` varchar(10) DEFAULT NULL, " + \
                        "`track_run_2` varchar(10) DEFAULT NULL, " + \
                        "`track_run_3` varchar(10) DEFAULT NULL, " + \
                        "`track_run` decimal(4,0) DEFAULT NULL, " + \
                        "`competition_day` varchar(45) DEFAULT NULL, " + \
                        "`competition_type` varchar(45) DEFAULT NULL, " + \
                        "`oral_presentation_score` decimal(4,0) DEFAULT NULL, " + \
                        "`overall_score` decimal(4,0) DEFAULT NULL, " + \
                        "`comments` varchar(200) DEFAULT NULL, " + \
                        "`hide_from_display` int(11) DEFAULT NULL, " + \
                        "`hide_from_final_scores` int(11) DEFAULT NULL, " + \
                        "PRIMARY KEY (`number`), " + \
                        "UNIQUE KEY `name_UNIQUE` (`name`), " + \
                        "UNIQUE KEY `number_UNIQUE` (`number`)) ENGINE=InnoDB DEFAULT CHARSET=utf8"

                print("Creating new table...")
                cursor.execute(sql)
                Data.connection.commit()
                Data.dbTable = "`" + newTableName + "`"
                cursor.close()

                SettingsGUI.SaveData(Data.dbName, Data.dbIP, Data.dbUser, Data.dbPass, Data, Data.fontSize, Data.dbTable, Data.backup)
                for row in listOfInfo:
                    print("Adding team")
                    returnVal = AddTeam(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], Data)
                    if returnVal is -1:
                        Data.systemText.set("Error occured while adding team")
                        Data.displayTimer = 0
                        return -1

            except Exception as error:
                Data.systemText.set(error)
                ErrorPopup.ErrorPopup("011")
                Data.displayTimer = 0

    # Handles loading in an Excel Save
    # WORKS
    elif "Table Backup" in dataformat:
        # Get the formatted information
        listOfInfo = ExportManager.GenerateListForImportLoad(filename, Data)
        if listOfInfo == -1:
            return -1

        if Data.connected is False:
            ErrorPopup.ErrorPopup("010")
            Data.systemText.set("Failed to import data into database - no connection")
            Data.displayTimer = 0
            return -1

        try:
            # Execute the SQL command

            # Generates a new table TODO check to make sure table doesn't already exist
            cursor = Data.connection.cursor()
            sql = "CREATE TABLE `" + newTableName + "` (" + \
                  "`name` varchar(100) NOT NULL, " + \
                  "`number` int(11) NOT NULL, " + \
                  "`school` varchar(100) DEFAULT NULL, " + \
                  "`written_report_score` decimal(4,0) DEFAULT NULL, " + \
                  "`fabrication_score` decimal(4,0) DEFAULT NULL, " + \
                  "`track_run_1` varchar(10) DEFAULT NULL, " + \
                  "`track_run_2` varchar(10) DEFAULT NULL, " + \
                  "`track_run_3` varchar(10) DEFAULT NULL, " + \
                  "`track_run` decimal(4,0) DEFAULT NULL, " + \
                  "`competition_day` varchar(45) DEFAULT NULL, " + \
                  "`competition_type` varchar(45) DEFAULT NULL, " + \
                  "`oral_presentation_score` decimal(4,0) DEFAULT NULL, " + \
                  "`overall_score` decimal(4,0) DEFAULT NULL, " + \
                  "`comments` varchar(200) DEFAULT NULL, " + \
                  "`hide_from_display` int(11) DEFAULT NULL, " + \
                  "`hide_from_final_scores` int(11) DEFAULT NULL, " + \
                  "PRIMARY KEY (`number`), " + \
                  "UNIQUE KEY `name_UNIQUE` (`name`), " + \
                  "UNIQUE KEY `number_UNIQUE` (`number`)) ENGINE=InnoDB DEFAULT CHARSET=utf8"

            cursor.execute(sql)
            Data.connection.commit()
            Data.dbTable = "`" + newTableName + "`"
            cursor.close()
            SettingsGUI.SaveData(Data.dbName, Data.dbIP, Data.dbUser, Data.dbPass, Data, Data.fontSize, Data.dbTable,
                                 Data.backup)
            for row in listOfInfo:
                #TODO add skip if row is empty
                returnVal = AddTeam(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                    row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18],
                                    Data)
                if returnVal is -1:
                    Data.systemText.set("Error occured while adding team")
                    Data.displayTimer = 0
                    return -1

        except Exception as error:
            ErrorPopup.ErrorPopup("012")
            Data.systemText.set(error)
            Data.displayTimer = 0

    else:
        Data.systemText.set("No option select")
        Data.displayTimer = 0


# Exports all data in the database to an excel sheet, with/without hidden ones depending on input
# WORKS
def ExportData(filename, WorkData):
    if WorkData.connected is True:
        WorkData.systemText.set("Exporting Data to " + filename)
        WorkData.displayTimer = 0

        sql = "SELECT * FROM " + WorkData.dbTable

        if WorkData.connected is False:
            ErrorPopup.ErrorPopup("010")
            WorkData.systemText.set("Failed to export")
            WorkData.displayTimer = 0
            return -1

        try:
            # Execute the SQL command
            cursor = WorkData.connection.cursor()
            cursor.execute(sql)
            cursor.close()
        except Exception as error:
            ErrorPopup.ErrorPopup("008")
            WorkData.systemText.set(error)
            WorkData.displayTimer = 0
            return -1

        # Collects downloaded data and verifies it isn't empty
        DataDump = cursor.fetchall()
        if DataDump == ():
            ErrorPopup.ErrorPopup("009")
            return -1

        # Organizes Data prior to file-write
        AllData = []
        for i in range(0, len(DataDump)):
            tempList = []
            for x in DataDump[i]:
                if x == ":":
                    tempList.append("")
                else:
                    tempList.append(x)
            AllData.append(tempList)

        # writes to file
        ExportManager.ExportToExcel(AllData, filename, WorkData)


# Adds a new team from the database
# WORKS
def AddTeam(Number, Name, School, WrittenReportScore, TrackRunScore, Time1Min, Time1Sec, Time2Min, Time2Sec,\
            Time3Min, Time3Sec, HideScores, HideDisplay, Day, Type, OralScore, Fabrication, Total, Comments, Data):

    # Verifies user Input
    # Checks to make sure the Team name category is not null
    if Name == "":
        ErrorPopup.ErrorPopup("022")
        Data.systemText.set("Invalid Name")
        Data.displayTimer = 0
        return -1

    # Checks to make sure the Team Number is not null
    if Number == "":
        ErrorPopup.ErrorPopup("025")
        Data.systemText.set("Invalid Name")
        Data.displayTimer = 0
        return -1
    elif is_number(Number) is False:
        ErrorPopup.ErrorPopup("026")
        Data.systemText.set("Invalid Name")
        Data.displayTimer = 0
        return -1

    # Checks to make sure team number is unique
    # WORKS
    sql = "SELECT COUNT(*) FROM " + Data.dbTable + " WHERE number = " + Number

    try:
        cursor = Data.connection.cursor()
        cursor.execute(sql)
        NumResults = cursor.fetchone()
        cursor.close()
        if NumResults[0] > 0:
            ErrorPopup.ErrorPopup("027")
            Data.systemText.set("Team Number is already in use")
            Data.displayTimer = 0
            return -1
    except Exception as error:
        ErrorPopup.ErrorPopup("006")  # TODO Different Error Code
        Data.systemText.set(error)
        Data.displayTimer = 0
        return -1

    # Verifies that the information provided is of the correct format and is unique
    # Checks to make sure team name is unique
    # WORKS
    if Name != Data.getItem("name"):
        sql = "SELECT COUNT(*) FROM " + Data.dbTable + " WHERE name = '" + Name + "'"

        try:
            cursor = Data.connection.cursor()
            cursor.execute(sql)
            NumResults = cursor.fetchone()
            cursor.close()
            if NumResults[0] > 0:
                ErrorPopup.ErrorPopup("015")
                Data.systemText.set("Invalid Name")
                Data.displayTimer = 0
                return -1
        except Exception as error:
            ErrorPopup.ErrorPopup("006")  # TODO Different Error Code
            Data.systemText.set(error)
            Data.displayTimer = 0
            return -1

    # Checks Run Time variables
    varsToCheck = [Time1Min, Time1Sec, Time2Min, Time2Sec, Time3Min, Time3Sec]
    for i in varsToCheck:
        if i != "":
            if is_number(i) is False or len(i) > 2:
                ErrorPopup.ErrorPopup("016")
                Data.systemText.set("Invalid Run time value of: " + str(i))
                Data.displayTimer = 0
                return -1

    # Checks to make sure the scores are numbers
    varsScores = [WrittenReportScore, TrackRunScore, OralScore, Fabrication, Total]
    for i in range(len(varsScores)):
        if varsScores[i] != "":
            if is_number(varsScores[i]) is False:
                ErrorPopup.ErrorPopup("0" + str(17 + i))
                Data.systemText.set("Invalid (non-number) input value of: " + str(varsScores[i]))
                Data.displayTimer = 0
                return -1

    # Checks to make sure the competition type and day are not the default value
    if Day == "  Select Day  ":
        ErrorPopup.ErrorPopup("023")
        Data.systemText.set("Invalid selection for Competition Day")
        Data.displayTimer = 0
        return -1

    if Type == "  Select Competition Type  ":
        ErrorPopup.ErrorPopup("024")
        Data.systemText.set("Invalid selection for Competition Type")
        Data.displayTimer = 0
        return -1

    Comments = Comments.rstrip()
    Data.systemText.set("Adding Team... ")
    Data.displayTimer = 0
    print("Adding Team")

    # creates a string with the columns of the table
    columns = ""
    for i in range(0, len(Data.CurrentTeam.options)):
        if i != (len(Data.CurrentTeam.options) - 1):
            columns += (Data.CurrentTeam.options[i] + ", ")
        else:
            columns += Data.CurrentTeam.options[i]

    # creates a string with the values for each column
    timeRun1 = Time1Min + ":" + Time1Sec
    timeRun2 = Time2Min + ":" + Time2Sec
    timeRun3 = Time3Min + ":" + Time3Sec
    valuesList = [Name, Number, School, WrittenReportScore, Fabrication, timeRun1, timeRun2, timeRun3, TrackRunScore, Day, Type, OralScore, Total, Comments, HideDisplay, HideScores]
    values = ""

    for x in range(0, len(valuesList)):
        if str(valuesList[x]) == "":
            tempvalue = None
        else:
            tempvalue = str(valuesList[x])
        if x != (len(valuesList) - 1):
            if tempvalue is None:
                values += "NULL, "
            else:
                values += "'" + tempvalue + "', "
        else:
            if tempvalue is None:
                values += "NULL, "
            else:
                values += "'" + tempvalue + "'"

    sql = "INSERT INTO " + Data.dbTable + " (" + columns + ") VALUES (" + values + ")"
    Data.systemText.set(sql)
    Data.displayTimer = 0

    if Data.connected is False:
        ErrorPopup.ErrorPopup("010")
        Data.systemText.set("Failed to add team - no connection with database")
        Data.displayTimer = 0
        return -1

    try:
        # Execute the SQL command
        cursor = Data.connection.cursor()
        cursor.execute(sql)
        Data.connection.commit()
        cursor.close()
        return 1
    except Exception as error:
        ErrorPopup.ErrorPopup("003")
        Data.systemText.set(error)
        Data.displayTimer = 0
        return -1


# Generates an excel and a text document for the final results
# NOTE - Text document is just a fill-in of pre-designed victory documents.
# Creates a new table in the database that has all of the finalist information
def Finalize(WithSaturday, WithSunday, data, filename):
    print("Finalizing results... ")
    if data.connected is False:
        ErrorPopup.ErrorPopup("010")
        data.systemText.set("Not connected to database")
        data.displayTimer = 0
        return -1

    # TODO Add check to see if table access is enabled

    # Steps
    # 1. Pull down all data currently in database
    if WithSaturday == 1 and WithSunday == 0:
        sql = "SELECT * FROM " + data.dbTable + " WHERE hide_from_final_scores = 0 AND competition_day = '  Saturday  '"
    elif WithSaturday == 0 and WithSunday == 1:
        sql = "SELECT * FROM " + data.dbTable + " WHERE hide_from_final_scores = 0 AND competition_day = '  Sunday  '"
    else:
        sql = "SELECT * FROM " + data.dbTable + " WHERE hide_from_final_scores = 0"

    try:
        cursor = data.connection.cursor()
        cursor.execute(sql)
        dataDump = cursor.fetchall()
        cursor.close()

        # Checks to see if the data received is empty
        if dataDump == ():
            ErrorPopup.ErrorPopup("009")
            return -1
    except Exception as error:
        ErrorPopup.ErrorPopup("008")
        data.systemText.set(error)
        data.displayTimer = 0
        return -1

    # 3. Determine the place of each team (for all the extra fields, return as a list of strings for Queries)
    listOfValues = ExportManager.Finalize(dataDump, data)
    if listOfValues == -1:
        return -1

    # 5. Export the winning table information to an excel sheet TODO THIS
    try:
        f = open(filename, "w")
        for line in listOfValues:
            f.write(line)
            f.write("\n")
        f.close()
    except Exception as error:
        ErrorPopup.ErrorPopup("029")
        data.systemText.set(error)
        data.displayTimer = 0
        return -1

    # 5. Create the final_results table, clear it if it exists
    try:
        # Generates a new table
        cursor = data.connection.cursor()

        # Checks to see if there is a table named final_results
        sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = " + "'final_results'"
        data.connection.begin()
        cursor.execute(sql)
        if cursor.fetchone()[0] == 1:
            sql = "DELETE FROM final_results"
        else:
            sql = "CREATE TABLE `final_results` (" + \
                "`name` varchar(100) NOT NULL, " + \
                "`number` int(11) NOT NULL, " + \
                "`school` varchar(100) DEFAULT NULL, " + \
                "`written_report_score` decimal(4,0) DEFAULT NULL, " + \
                "`fabrication_score` decimal(4,0) DEFAULT NULL, " + \
                "`track_run_1` varchar(10) DEFAULT NULL, " + \
                "`track_run_2` varchar(10) DEFAULT NULL, " + \
                "`track_run_3` varchar(10) DEFAULT NULL, " + \
                "`track_run` decimal(4,0) DEFAULT NULL, " + \
                "`competition_day` varchar(45) DEFAULT NULL, " + \
                "`competition_type` varchar(45) DEFAULT NULL, " + \
                "`oral_presentation_score` decimal(4,0) DEFAULT NULL, " + \
                "`overall_score` decimal(4,0) DEFAULT NULL, " + \
                "`comments` varchar(200) DEFAULT NULL, " + \
                "`place_manual_saturday` INT DEFAULT NULL, " + \
                "`place_manual_sunday` INT DEFAULT NULL, " + \
                "`place_manual_both_days` INT DEFAULT NULL, " + \
                "`place_overall_saturday` INT DEFAULT NULL, " + \
                "`place_overall_sunday` INT DEFAULT NULL, " + \
                "`place_overall_both_days` INT DEFAULT NULL, " + \
                "`place_total` INT DEFAULT NULL, " + \
                "PRIMARY KEY (`number`), " + \
                "UNIQUE KEY `name_UNIQUE` (`name`), " + \
                "UNIQUE KEY `number_UNIQUE` (`number`)) ENGINE=InnoDB DEFAULT CHARSET=utf8"

        print(sql)
        cursor.execute(sql)
        data.connection.commit()
        cursor.close()
    except Exception as error:
        data.systemText.set(error)
        data.displayTimer = 0
        ErrorPopup.ErrorPopup("028")
        return -1

    # 6. Add Each team using the values list
    try:
        cursor = data.connection.cursor()
        for info in listOfValues:
            sql = "INSERT INTO `final_results` (" + data.FinalColumns + ") VALUES (" + info + ")"
            print(sql)
            cursor.execute(sql)
        data.connection.commit()
        cursor.close()
    except Exception as error:
        data.systemText.set(error)
        data.displayTimer = 0
        ErrorPopup.ErrorPopup("003")
        return -1


# Gets the information for one of the teams given a search criteria
# WORKS
def Search(value, Data, listOfEntries):
    Data.systemText.set("Gathering information for team: " + str(value))
    Data.displayTimer = 0

    #Gets result back from database
    if is_number(value) is True:
        sql = "SELECT * FROM " + Data.dbTable + " WHERE number = " + str(value)
    else:
        sql = "SELECT * FROM " + Data.dbTable + " WHERE name = '" + value + "'"

    Data.systemText.set(sql)
    Data.displayTimer = 0

    if Data.connected is False:
        ErrorPopup.ErrorPopup("010")
        Data.systemText.set("Failed to perform search - no connection to database")
        Data.displayTimer = 0
        return -1

    try:
        # Execute the SQL command
        cursor = Data.connection.cursor()
        cursor.execute(sql)
        cursor.close()
    except Exception as error:
        ErrorPopup.ErrorPopup("002")
        Data.systemText.set(error)
        Data.displayTimer = 0
        return -1

    receivedData = cursor.fetchall()
    if receivedData == ():
        ErrorPopup.ErrorPopup("004")
        return -1
    Data.ChangeTeam(Data.CurrentTeam.Translate(receivedData))

    listOfNames = ["school", "name", "written_report_score", "track_run", "comments", "fabrication_score", "oral_presentation_score", "overall_score"]
    for i in range(0, 8):
        item = listOfEntries[i]
        if i != 4:
            if Data.getItem(listOfNames[i]) is None:
                insertString = ""
            else:
                insertString = Data.getItem(listOfNames[i])
            item.delete(0, END)
            item.insert(0, insertString)

    # Changes the data in the Comments Box
    listOfEntries[4].delete("1.0", END)
    if Data.getItem(listOfNames[4]) is None:
        listOfEntries[4].insert("1.0", "")
    else:
        listOfEntries[4].insert("1.0", Data.getItem(listOfNames[4]))

    # Inserts track run time 1
    tempList = Data.getItem("track_run_1").split(":")
    listOfEntries[8].delete(0, END)
    listOfEntries[8].insert(0, tempList[0])
    listOfEntries[9].delete(0, END)
    listOfEntries[9].insert(0, tempList[1])

    # sets the run time for 2
    tempList = Data.getItem("track_run_2").split(":")
    listOfEntries[10].delete(0, END)
    listOfEntries[10].insert(0, tempList[0])
    listOfEntries[11].delete(0, END)
    listOfEntries[11].insert(0, tempList[1])

    # sets the run time for time 3
    tempList = Data.getItem("track_run_3").split(":")
    listOfEntries[12].delete(0, END)
    listOfEntries[12].insert(0, tempList[0])
    listOfEntries[13].delete(0, END)
    listOfEntries[13].insert(0, tempList[1])

    #sets the check boxes
    if Data.getItem("hide_from_display") == 1:
        listOfEntries[14].select()
    else:
        listOfEntries[14].deselect()

    if Data.getItem("hide_from_final_scores") == 1:
        listOfEntries[15].select()
    else:
        listOfEntries[15].deselect()

    # sets the drop down menus
    listOfEntries[16].set(Data.getItem("competition_day"))
    listOfEntries[17].set(Data.getItem("competition_type"))

    # sets the team number
    listOfEntries[18].set("Team Number: " + str(Data.getItem("number")))


# Updates the listBox with teams in the database every second
# WORKS
def UpdateList(Data, listBox):
    if Data.connected is True:

        # Resets the system text after x seconds
        x = 3
        if Data.displayTimer < x:
            Data.displayTimer += 1
        else:
            Data.displayTimer = 0
            Data.systemText.set("")

        # Tests to make sure connection is still open
        # DEPRECATED
        #if Data.connection.open != 1:
        #    ErrorPopup.ErrorPopup("006")
        #    CloseConnection(Data)
        #    Data.connected = False
        #    Data.connection = None
        #   return -1

        sql = "SELECT name, number FROM " + Data.dbTable
        print(sql)

        if Data.connected is False:
            ErrorPopup.ErrorPopup("010")
            Data.systemText.set("failed to update list of teams - no connection to database")
            Data.displayTimer = 0
            return -1

        try:
            cursor = Data.connection.cursor()
            cursor.execute(sql)
            Data.UpdateTeamList(cursor.fetchall(), listBox)
            cursor.close()
            listBox.after(3000, UpdateList, Data, listBox)
        except Exception as e:
            Data.systemText.set(e)
            Data.displayTimer = 0
            ErrorPopup.ErrorPopup("013")


# Disconnects from the database
# WORKS
def CloseConnection(Data):
    if Data.connected == True:
        Data.connection.close()
        Data.connection = None
        Data.connected = False
        print("Disconnected")
        Data.systemText.set("Disconnected")
        Data.displayTimer = 0


# Updates the information from a team
# WORKS
def Update(Name, School, WrittenReportScore, TrackRunScore, Time1Min, Time1Sec, Time2Min, Time2Sec,\
            Time3Min, Time3Sec, HideScores, HideDisplay, Day, Type, OralScore, Fabrication, Total, Comments, Data):
    teamNum = Data.CurrentTeam.getItem("number")
    Comments = Comments.rstrip()
    # Updates the Current Team information with the new inputted information

    # Checks to make sure the Team name category is not null
    if Name == "":
        ErrorPopup.ErrorPopup("022")
        Data.systemText.set("Invalid Name")
        Data.displayTimer = 0
        return -1

    # Verifies that the information provided is of the correct format and is unique
    # Checks to make sure team name is unique
    # WORKS
    if Name != Data.getItem("name"):
        sql = "SELECT COUNT(*) FROM " + Data.dbTable + " WHERE name = '" + Name + "'"

        try:
            cursor = Data.connection.cursor()
            cursor.execute(sql)
            NumResults = cursor.fetchone()
            cursor.close()
            if NumResults[0] > 0:
                ErrorPopup.ErrorPopup("015")
                Data.systemText.set("Invalid Name")
                Data.displayTimer = 0
                return -1
        except Exception as error:
            ErrorPopup.ErrorPopup("006")  # TODO Different Error Code
            Data.systemText.set(error)
            Data.displayTimer = 0
            return -1

    # Checks Run Time variables
    varsToCheck = [Time1Min, Time1Sec, Time2Min, Time2Sec, Time3Min, Time3Sec]
    for i in varsToCheck:
        if i != "":
            if is_number(i) is False or len(i) > 2:
                ErrorPopup.ErrorPopup("016")
                Data.systemText.set("Invalid Run time value of: " + str(i))
                Data.displayTimer = 0
                return -1

    # Checks to make sure the scores are numbers
    varsScores = [WrittenReportScore, TrackRunScore, OralScore, Fabrication, Total]
    for i in range(len(varsScores)):
        if varsScores[i] != "":
            if is_number(varsScores[i]) is False:
                ErrorPopup.ErrorPopup("0" + str(17 + i))
                Data.systemText.set("Invalid (non-number) input value of: " + str(varsScores[i]))
                Data.displayTimer = 0
                return -1


    # Checks to make sure the competition type and day are not the default value
    if Day == "  Select Day  ":
        ErrorPopup.ErrorPopup("023")
        Data.systemText.set("Invalid selection for Competition Day")
        Data.displayTimer = 0
        return -1

    if Type == "  Select Competition Type  ":
        ErrorPopup.ErrorPopup("024")
        Data.systemText.set("Invalid selection for Competition Type")
        Data.displayTimer = 0
        return -1

    # creates a string with the values for each column
    timeRun1 = Time1Min + ":" + Time1Sec
    timeRun2 = Time2Min + ":" + Time2Sec
    timeRun3 = Time3Min + ":" + Time3Sec
    valuesList = [Name, teamNum, School, WrittenReportScore, Fabrication, timeRun1, timeRun2, timeRun3, TrackRunScore,
                  Day, Type, OralScore, Total, Comments, HideDisplay, HideScores]

    for i in range(0, len(Data.CurrentTeam.options)):
        Data.CurrentTeam.info[Data.CurrentTeam.options[i]] = valuesList[i]

    #Constructs the list of terms for the UPDATE query
    values = ""
    for x in range(0, len(valuesList)):
        if str(valuesList[x]) == "":
            dataValue = "NULL"
        else:
            dataValue = "'" + str(valuesList[x]) + "'"

        if x != (len(valuesList) - 1):
            termString = Data.CurrentTeam.options[x] + " = " + dataValue + ", "
        else:
            termString = Data.CurrentTeam.options[x] + " = " + dataValue

        values += termString

    # Updates the information for the current team in the database
    updateCommand = "UPDATE " + Data.dbTable
    conditionsCommand = "SET " + values
    rowLocator = "WHERE number = " + str(teamNum)

    sql = updateCommand + " " + conditionsCommand + " " + rowLocator

    Data.systemText.set(sql)
    Data.displayTimer = 0

    if Data.connected is False:
        ErrorPopup.ErrorPopup("010")
        Data.systemText.set("failed to update team information - no connection to database")
        Data.displayTimer = 0
        return -1

    try:
        # Execute the SQL command
        cursor = Data.connection.cursor()
        cursor.execute(sql)
        Data.connection.commit()
        cursor.close()
    except Exception as error:
        Data.systemText.set(error)
        Data.displayTimer = 0
        ErrorPopup.ErrorPopup("007")
        return -1

# Gets a list of tables currently in the database
# UNUSED
def GetTables(data):
    sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = '" + data.dbName + "'"

    if data.connected is False:
        ErrorPopup.ErrorPopup("010")
        data.systemText.set("failed to update team information - no connection to database")
        data.displayTimer = 0
        return -1

    try:
        # Execute the SQL command
        cursor = data.connection.cursor()
        cursor.execute(sql)
        cursor.close()
    except Exception as error:
        data.systemText.set(error)
        data.displayTimer = 0
        ErrorPopup.ErrorPopup("000")
        return -1

