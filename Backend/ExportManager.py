import csv
from GUIs import ErrorPopup
from Backend import FinalTeam
from Backend import dbCommands
from operator import itemgetter

# Function that writes all downloaded data to an Excel file
# DONE
# TODO add error popup failed to write to file
def ExportToExcel(AllData, filename, WorkData):
    csvfile = open((filename + ".csv"), "w")
    stream = csv.writer(csvfile, dialect='excel', delimiter=',')

    # Writes the top row, which shows what each column is
    stream.writerow(WorkData.CurrentTeam.options)

    # Writes each row individually
    for row in AllData:
        stream.writerow(row)

    # Closes the file
    csvfile.close()


# Generates a list of strings that can be used to add data to a new table
# TODO Add Error popup could not find file
def GenerateStringsReportStyle(filename, Data):

    # Grabs the data from the file
    try:
        file = open(filename, "r")
        dataDump = file.read()
        file.close()
    except Exception as error:
        ErrorPopup.ErrorPopup("014")
        Data.systemText.set(error)
        Data.displayTimer = 0
        return -1

    print("DATA DUMP:")
    print(dataDump)
    print("\n")

    # Formats the information into the desired format
    rows = dataDump.split("\n")  # looks like "team,score", "team,score"
    listOfStrings = []
    for curRow in rows:
        items = curRow.split(",")
        listOfStrings.append(" SET written_report_score = " + items[1] + " WHERE number = " + str(items[0]))

    return listOfStrings

# used to format the data into the proper organization so that the Add-Team function can be used to import data
#
def GenerateListForImport(filename, Data):

    # TODO Add error popup could not find/open file
    # Grabs the data from the file
    try:
        file = open(filename, "r")
        dataDump = file.read()
        file.close()
    except Exception as error:
        ErrorPopup.ErrorPopup("014")
        Data.systemText.set(error)
        Data.displayTimer = 0
        return -1

    # Formats the information into the desired format
    rows = dataDump.split("\n")  # looks like "col1,col2,col3,col4,col5
    #Need the Data to be in this format: [Number, Name, School, WrittenReportScore, TrackRunScore, Time1Min, Time1Sec, Time2Min, Time2Sec,
    # ...Time3Min, Time3Sec, HideScores, HideDisplay, Day, Type, OralScore, Fabrication, Total, Comments, Data]
    formattedRows = []
    for curRow in range(1, len(rows) - 1):
        datapoints = rows[curRow].split(",")

        #TODO Determine competition type based on auto information

        newList = [datapoints[3], datapoints[7], datapoints[5], "", "", "", "", "", "", "", "", 0, 0, datapoints[9].split()[0], datapoints[4], "", "", "", "", Data, ""]
        formattedRows.append(newList)

    return formattedRows

# Function to format data for loading in from an autosave or an Export
def GenerateListForImportLoad(filename, Data):
    # TODO Add error popup could not find/open file
    # Grabs the data from the file
    try:
        file = open(filename, "r")
        dataDump = file.read()
        file.close()
    except Exception as error:
        ErrorPopup.ErrorPopup("014")
        Data.systemText.set(error)
        Data.displayTimer = 0
        return -1


    # Formats the information into the desired format
    rows = dataDump.split("\n")  # looks like "col1,col2,col3,col4,col5

    # Need the Data to be in this format: [Number, Name, School, WrittenReportScore, TrackRunScore, Time1Min, Time1Sec, Time2Min, Time2Sec,
    # ...Time3Min, Time3Sec, HideScores, HideDisplay, Day, Type, OralScore, Fabrication, Total, Comments, Data]
    formattedRows = []
    for curRow in range(2, len(rows) - 1, 2):

        datapoints = rows[curRow].split(",")

        # Splits the times
        Time1Min = ""
        Time1Sec = ""
        Time2Min = ""
        Time2Sec = ""
        Time3Min = ""
        Time3Sec = ""
        if datapoints[6] != "":
            timeSplit = datapoints[6].split(":")
            Time1Min = timeSplit[0]
            Time1Sec = timeSplit[1]

        if datapoints[7] != "":
            timeSplit = datapoints[7].split(":")
            Time2Min = timeSplit[0]
            Time2Sec = timeSplit[1]

        if datapoints[8] != "":
            timeSplit = datapoints[8].split(":")
            Time3Min = timeSplit[0]
            Time3Sec = timeSplit[1]

        # Generates the list with the inputs in the right order
        newList = [datapoints[1], datapoints[0], datapoints[2], datapoints[3], datapoints[9], Time1Min, Time1Sec, Time2Min, Time2Sec, Time3Min, Time3Sec, datapoints[16],
                   datapoints[15], datapoints[10], datapoints[11], datapoints[12], datapoints[5], datapoints[13], RemoveEndQuotes(datapoints[14]), Data, datapoints[4]]
        formattedRows.append(newList)

    return formattedRows

# Small recursive
def RemoveEndQuotes(s):
    start = 0
    end = len(s) - 1

    # finds the start of the string
    while(s[start]) == '"':
        start += 1

    # finds the end of the string
    while(s[end]) == '"':
        end -= 1

    return s[start:end + 1]


# Determines the placement information for each team
# Returns a list of FinalTeam objects, in no apparent order
def Judge(dataDump, data):
    print("Placing teams")

    # Generates list of final teams without placement information
    listOfTeams = []
    for i in range(len(dataDump)):
        if dataDump[i] != "\n":
            tempTeam = FinalTeam.FinalTeam()
            tempTeam.Populate(dataDump[i])
            listOfTeams.append(tempTeam)

    # Adds placement information to each team (save index and thing to tuple, then order the dictionary by value size and go by index)

    # Inserts the total placement value for each team
    listOfScores = []  # Format [(number, score, trackScore), (number, score, trackScore)] # TODO add more match things here
    for teamIndex in range(len(listOfTeams)):
        if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
            if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(listOfTeams[teamIndex].info["track_run"]) is True:
                listOfScores.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]), float(listOfTeams[teamIndex].info["track_run"])))

    listOfScores.sort(key=itemgetter(2), reverse=True)
    listOfScores.sort(key=itemgetter(1), reverse=True)

    for place in range(len(listOfScores)):
        listOfTeams[listOfScores[place][0]].info["place_total"] = place + 1

    # Determines the placement_overall saturday, placement_overall_sunday, and placement_overall_both_days
    listOfScoresSaturday2Leg = []
    listOfScoresSaturday4Leg = []
    listOfScoresSunday2Leg = []
    listOfScoresSunday4Leg = []
    listOfScoresBothDays2Leg = [] # Format [(number, score, trackScore), (number, score, trackScore)] # TODO add more match things here
    listOfScoresBothDays4Leg = []
    for teamIndex in range(len(listOfTeams)):
        # Adds 2leg overall teams for saturday
        if listOfTeams[teamIndex].info["competition_day"].strip() == "Saturday" and listOfTeams[teamIndex].info["competition_type"] == "  2-leg overall  ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSaturday2Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 4leg overall teams for saturday
        elif listOfTeams[teamIndex].info["competition_day"].strip() == "Saturday" and listOfTeams[teamIndex].info["competition_type"] == "  4-leg overall  ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSaturday4Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 2leg overall teams for Sunday
        elif listOfTeams[teamIndex].info["competition_day"].strip() == "Sunday" and listOfTeams[teamIndex].info["competition_type"] == "  2-leg overall  ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSunday2Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 4leg overall teams for Sunday
        elif listOfTeams[teamIndex].info["competition_day"].strip() == "Sunday" and listOfTeams[teamIndex].info["competition_type"] == "  4-leg overall  ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSunday4Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 2leg overall teams for both days
        if listOfTeams[teamIndex].info["competition_type"] == "  2-leg overall  ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(
                        listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresBothDays2Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),
                                                 float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 4leg overall teams for both days
        elif listOfTeams[teamIndex].info["competition_type"] == "  4-leg overall  ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(
                        listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresBothDays4Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),
                                                 float(listOfTeams[teamIndex].info["track_run"])))

    # Sorts all of the lists
    listOfScoresSaturday2Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSaturday2Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresSaturday4Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSaturday4Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresSunday2Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSunday2Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresSunday4Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSunday4Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresBothDays2Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresBothDays2Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresBothDays4Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresBothDays4Leg.sort(key=itemgetter(1), reverse=True)

    # Gives the places for 2-leg overall both days
    largestIndex = 0
    if len(listOfScoresSaturday2Leg) > largestIndex:
        largestIndex = len(listOfScoresSaturday2Leg)
    if len(listOfScoresSaturday4Leg) > largestIndex:
        largestIndex = len(listOfScoresSaturday4Leg)
    if len(listOfScoresSunday2Leg) > largestIndex:
        largestIndex = len(listOfScoresSunday2Leg)
    if len(listOfScoresSunday4Leg) > largestIndex:
        largestIndex = len(listOfScoresSunday4Leg)
    if len(listOfScoresBothDays2Leg) > largestIndex:
        largestIndex = len(listOfScoresBothDays2Leg)
    if len(listOfScoresBothDays4Leg) > largestIndex:
        largestIndex = len(listOfScoresBothDays4Leg)

    for place in range(largestIndex):
        if place < len(listOfScoresSaturday2Leg):
            listOfTeams[listOfScoresSaturday2Leg[place][0]].info["place_overall_saturday"] = place + 1
        if place < len(listOfScoresSaturday4Leg):
            listOfTeams[listOfScoresSaturday4Leg[place][0]].info["place_overall_saturday"] = place + 1
        if place < len(listOfScoresSunday2Leg):
            listOfTeams[listOfScoresSunday2Leg[place][0]].info["place_overall_sunday"] = place + 1
        if place < len(listOfScoresSunday4Leg):
            listOfTeams[listOfScoresSunday4Leg[place][0]].info["place_overall_sunday"] = place + 1
        if place < len(listOfScoresBothDays2Leg):
            listOfTeams[listOfScoresBothDays2Leg[place][0]].info["place_overall_both_days"] = place + 1
        if place < len(listOfScoresBothDays4Leg):
            listOfTeams[listOfScoresBothDays4Leg[place][0]].info["place_overall_both_days"] = place + 1

    # Determines the placement_manual_saturday, placement_manual_sunday, placement_manual_both_days
    listOfScoresSaturday2Leg = []
    listOfScoresSaturday4Leg = []
    listOfScoresSunday2Leg = []
    listOfScoresSunday4Leg = []
    listOfScoresBothDays2Leg = []  # Format [(number, score, trackScore), (number, score, trackScore)] # TODO add more match things here
    listOfScoresBothDays4Leg = []
    for teamIndex in range(len(listOfTeams)):
        # Adds 2leg overall teams for saturday
        if listOfTeams[teamIndex].info["competition_day"].strip() == "Saturday" and listOfTeams[teamIndex].info["competition_type"] == "  2-leg manual   ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(
                        listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSaturday2Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]), float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 4leg overall teams for saturday
        elif listOfTeams[teamIndex].info["competition_day"].strip() == "Saturday" and listOfTeams[teamIndex].info["competition_type"] == "  4-leg manual   ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(
                        listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSaturday4Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),
                                                     float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 2leg overall teams for Sunday
        elif listOfTeams[teamIndex].info["competition_day"].strip() == "Sunday" and listOfTeams[teamIndex].info["competition_type"] == "  2-leg manual   ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(
                        listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSunday2Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),
                                                   float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 4leg overall teams for Sunday
        elif listOfTeams[teamIndex].info["competition_day"].strip() == "Sunday" and listOfTeams[teamIndex].info["competition_type"] == "  4-leg manual   ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresSunday4Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),
                                                   float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 2leg overall teams for both days
        if listOfTeams[teamIndex].info["competition_type"] == "  2-leg manual   ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info["track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(
                        listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresBothDays2Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),
                                                     float(listOfTeams[teamIndex].info["track_run"])))

        # Adds 4leg overall teams for both days
        elif listOfTeams[teamIndex].info["competition_type"] == "  4-leg manual   ":
            if listOfTeams[teamIndex].info["overall_score"] is not None and listOfTeams[teamIndex].info[
                "track_run"] is not None:
                if dbCommands.is_number(listOfTeams[teamIndex].info["overall_score"]) is True and dbCommands.is_number(
                        listOfTeams[teamIndex].info["track_run"]) is True:
                    listOfScoresBothDays4Leg.append((teamIndex, float(listOfTeams[teamIndex].info["overall_score"]),
                                                     float(listOfTeams[teamIndex].info["track_run"])))

    # Sorts all of the lists
    listOfScoresSaturday2Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSaturday2Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresSaturday4Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSaturday4Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresSunday2Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSunday2Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresSunday4Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresSunday4Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresBothDays2Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresBothDays2Leg.sort(key=itemgetter(1), reverse=True)
    listOfScoresBothDays4Leg.sort(key=itemgetter(2), reverse=True)
    listOfScoresBothDays4Leg.sort(key=itemgetter(1), reverse=True)

    # Gives the places for 2-leg overall both days
    largestIndex = 0
    if len(listOfScoresSaturday2Leg) > largestIndex:
        largestIndex = len(listOfScoresSaturday2Leg)
    if len(listOfScoresSaturday4Leg) > largestIndex:
        largestIndex = len(listOfScoresSaturday4Leg)
    if len(listOfScoresSunday2Leg) > largestIndex:
        largestIndex = len(listOfScoresSunday2Leg)
    if len(listOfScoresSunday4Leg) > largestIndex:
        largestIndex = len(listOfScoresSunday4Leg)
    if len(listOfScoresBothDays2Leg) > largestIndex:
        largestIndex = len(listOfScoresBothDays2Leg)
    if len(listOfScoresBothDays4Leg) > largestIndex:
        largestIndex = len(listOfScoresBothDays4Leg)

    for place in range(largestIndex):
        if place < len(listOfScoresSaturday2Leg):
            listOfTeams[listOfScoresSaturday2Leg[place][0]].info["place_manual_saturday"] = place + 1
        if place < len(listOfScoresSaturday4Leg):
            listOfTeams[listOfScoresSaturday4Leg[place][0]].info["place_manual_saturday"] = place + 1
        if place < len(listOfScoresSunday2Leg):
            listOfTeams[listOfScoresSunday2Leg[place][0]].info["place_manual_sunday"] = place + 1
        if place < len(listOfScoresSunday4Leg):
            listOfTeams[listOfScoresSunday4Leg[place][0]].info["place_manual_sunday"] = place + 1
        if place < len(listOfScoresBothDays2Leg):
            listOfTeams[listOfScoresBothDays2Leg[place][0]].info["place_manual_both_days"] = place + 1
        if place < len(listOfScoresBothDays4Leg):
            listOfTeams[listOfScoresBothDays4Leg[place][0]].info["place_manual_both_days"] = place + 1

    return listOfTeams


# Returns a list of query strings for each team that is ready for executing
def Finalize(dataDump, data):
    print("Generating SQL Commands")
    listOfTeams = Judge(dataDump, data)

    listOfFinalThings = []

    for team in listOfTeams:
        listOfFinalThings.append(team.genQuery())

    return listOfFinalThings