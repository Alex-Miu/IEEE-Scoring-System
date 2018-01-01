import Team
from tkinter import *

class WorkingData:
    # Constructor
    def __init__(self, startSettings):
        self.fontSize = startSettings["fontSize"]
        self.font = "Calibri"  # default font
        self.teamList = []
        self.CurrentTeam = Team.Team("", "", "")
        self.connection = None
        self.connected = False
        self.system = None
        self.systemText = None
        self.displayTimer = 0
        self.FinalColumns = "name, number, school, written_report_score, fabrication_score, track_run_1, track_run_2, track_run_3, track_run, competition_day, competition_type, oral_presentation_score, overall_score, comments, place_manual_saturday, place_manual_sunday, place_manual_both_days, place_overall_saturday, place_overall_sunday, place_overall_both_days, place_total"

        # Settings
        self.backup = startSettings["backup"]
        self.dbName = startSettings["dbName"]
        self.dbIP = startSettings["dbIP"]
        self.dbTable = startSettings["dbTable"]
        self.dbPass = startSettings["dbPass"]
        self.dbUser = startSettings["dbUser"]

    def setFontSize(self, newFont):
        self.fontSize = newFont

    def getFontSize(self):
        return self.fontSize

    def getTeamList(self):
        return self.teamList

    def UpdateTeamList(self, newList, listBox):
        newListing = []
        listBox.delete(0, END)
        for i in range(0, len(newList)):
            s = " "
            teamName = newList[i][0]
            teamNum = newList[i][1]
            line = s.join((str(teamNum), ":    ", str(teamName)))
            newListing.append(line)
            listBox.insert(i, line)
        self.teamList = newListing

    def ChangeTeam(self, newTeam):
        self.CurrentTeam.Change(newTeam)

    def getItem(self, key):
        return self.CurrentTeam.getItem(key)




