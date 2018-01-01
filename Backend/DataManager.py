# Class that contains all active working data
from tkinter import StringVar

class DataManager:

    # Constructor
    def __init__(self, defaultSettings):

        # settings
        self.fontSize = defaultSettings["fontSize"]
        self.delay = int(defaultSettings["delay"])
        self.dbName = defaultSettings["dbName"]
        self.dbIP = defaultSettings["dbIP"]
        self.dbTable = defaultSettings["dbTable"]
        self.dbPass = defaultSettings["dbPass"]
        self.dbUser = defaultSettings["dbUser"]
        self.font = "Calibri"
        self.height = int(defaultSettings["MAXheight"])  # Number of rows, changes to the number of teams to display
        self.width = 13  # Number of Columns, stays constant
        self.displayTitle = None
        self.connected = False
        self.connection = None
        self.tableValues = None
        self.MAXheight = defaultSettings["MAXheight"]
        self.root = None  # Main Frame in the window
        self.window = None  # The Window
        self.Types = ["  4-leg manual   ", "  2-leg overall  ", "  2-leg manual   ", "  4-leg overall  "]
        self.counter = 0
        self.index = 0
        self.scrollbar = None
        self.colSize = [8, 31, 30, 8, 13, 11, 11, 13, 15, 12, 12, 12, 5]
        self.vsbar = None
        self.cFrame = None
        self.offset = 0
        self.inside = None
        self.endOfGame = False
        self.today = ""
        self.resultsCategories = [("\nTeam #\n", 8), ("\nSchool\n", 31), ("\nTeam Name\n", 30), ("\nType\n", 8), ("Place #\nManual\nSaturday", 13), ("Place #\nManual\nSunday", 11), ("Place #\nManual\nBoth Days", 11), ("Place #\nOverall\nSaturday", 13), ("Place #\nOverall\nSunday", 15), ("Place #\nOverall\nBoth Days", 12)]
        self.normalCategories = [" Team # ", " School ", " Team Name ", " Type ", " Written Rep ", " Track Run ", " Oral Pres ", " Fabrication ", " Overall Score ", " Run Time 1 ", " Run Time 2 ", " Run Time 3 ", " Day "]
        self.ResultsCycle = ["  4-leg manual   ", "  2-leg overall  ", "  2-leg manual   ", "  4-leg overall  ", "  2-leg  ", "  4-leg  "]
        self.showWinners = False
        self.titleFrame = None

    def getNextType(self):
        if self.index >= 3:
            self.index = 0
        else:
            self.index += 1
        return self.Types[self.index]

    def getNextWinningType(self):
        if self.index >= 5:
            self.index = 0
        else:
            self.index += 1
        print(self.ResultsCycle[self.index])
        return self.ResultsCycle[self.index]
