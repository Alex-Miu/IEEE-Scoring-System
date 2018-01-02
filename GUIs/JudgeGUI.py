# Filename: JudgeGUI.py
# Project: Real Time Scoring System
# Organization: IEEE - UMBC Student Branch
# Author: Alex Miu
# Date: 12/01/2017
# Description: This file contains the code for the User interface of the Data Entry System.


# imports
from Resources.tkinter import *

from Backend import dbCommands, WorkingData
from GUIs import AddNewGUI
from GUIs import ExportPopup
from GUIs import ImportPopup
from GUIs import ResultsPopup
from GUIs import SettingsGUI


def JudgeGUI(defaultFont):
    root = Tk()

    Data = WorkingData.WorkingData(defaultFont)
    root.title("Data Entry System")

    #Adds Menus to the window bar
    menubar = Menu(root, font=(Data.font, Data.fontSize))
    menubar.add_command(label="Import", command=lambda: ImportPopup.ImportPopup(Data), font=(Data.font, Data.fontSize))
    menubar.add_command(label="Export", command=lambda: ExportPopup.ExportPopup(Data), font=(Data.font, Data.fontSize))
    menubar.add_command(label="Settings", command=lambda: SettingsGUI.SettingsGUI(Data, listBox), font=(Data.font, Data.fontSize))
    menubar.add_command(label="Get Results", command=lambda: ResultsPopup.ResultsPopup(Data), font=(Data.font, Data.fontSize))
    menubar.add_command(label="Disconnect", command=lambda: dbCommands.CloseConnection(Data), font=(Data.font, Data.fontSize))
    root.config(menu=menubar)

    # rebinds the close window option to ensure the server is disconnected
    root.protocol('WM_DELETE_WINDOW', lambda: CloseAll(Data, root))

    # Creates the system label along the bottom
    Data.systemText = StringVar()
    system = Label(root, textvariable=Data.systemText, anchor="w", width=100, font=(Data.font, Data.fontSize))
    system.pack(side="bottom", fill="x", anchor=S, expand=False)

    # Saves a backup of the current table every x minutes
    system.after(Data.backup, dbCommands.ExportData, "table_backup", Data)

    #Creates the frame that holds the scroll section
    scrollFrame = Frame(root)
    scrollFrame.pack(side="left", fill="y", anchor=W, expand=True)

    #Creates the scrollbar and listbox
    scrollbar = Scrollbar(scrollFrame, orient="vertical")
    listBox = Listbox(scrollFrame, width=30, height=20, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listBox.yview)
    scrollbar.pack(side="right", fill="y")
    listBox.pack(side="left", fill="y", anchor=W, expand=True)

    #Creates the frame with all of the data fields in it
    fieldsFrame = Frame(root)
    fieldsFrame.pack(side="left", fill="both", anchor="w", expand=True)

    #Adds fields for data input

    #Works with Search Frame
    searchFrame = LabelFrame(fieldsFrame, text=" Search ", font=(Data.font, Data.fontSize))
    searchFrame.grid(row=0, column=0, columnspan=2, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    searchLabel = Label(searchFrame, text="Enter Team Name or Number:", font=(Data.font, Data.fontSize))
    searchLabel.grid(row=2, column=5, padx=5, pady=2)

    searchBox = Entry(searchFrame, width=40, font=(Data.font, Data.fontSize))
    searchBox.grid(row=2, column=7, pady=2)

    searchButton = Button(searchFrame, text=" Search ", font=(Data.font, Data.fontSize), command= lambda: dbCommands.Search(searchBox.get(), Data, [SchoolBox, NameBox, WrittenReportScoreBox, TrackRunScoreBox, CommentsBox, FabricationBox, OralBox, TotalBox, Time1BoxMin, Time1BoxSec, Time2BoxMin, Time2BoxSec, Time3BoxMin, Time3BoxSec, HideDisplayCheck, HideScoresCheck, DayDrop, TypeDrop, teamNumVar, ControlDrop]))
    searchButton.grid(row=2, column=11, padx=5, pady=2)


    #Works with Team Name
    NameFrame = LabelFrame(fieldsFrame, text=" Team Name ", font=(Data.font, Data.fontSize))
    NameFrame.grid(row=2, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    NameBox = Entry(NameFrame, width=40, font=(Data.font, Data.fontSize))
    NameBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    #Works with School
    SchoolFrame = LabelFrame(fieldsFrame, text=" School ", font=(Data.font, Data.fontSize))
    SchoolFrame.grid(row=3, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    SchoolBox = Entry(SchoolFrame, width=40, font=(Data.font, Data.fontSize))
    SchoolBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    #Handles written report score
    WrittenReportScoreFrame = LabelFrame(fieldsFrame, text=" Written Report Score ", font=(Data.font, Data.fontSize))
    WrittenReportScoreFrame.grid(row=4, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    WrittenReportScoreBox = Entry(WrittenReportScoreFrame, width=10, font=(Data.font, Data.fontSize))
    WrittenReportScoreBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    #Handles track run score
    TrackRunScoreFrame = LabelFrame(fieldsFrame, text=" Track Run Score ", font=(Data.font, Data.fontSize))
    TrackRunScoreFrame.grid(row=5, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    TrackRunScoreBox = Entry(TrackRunScoreFrame, width=10, font=(Data.font, Data.fontSize))
    TrackRunScoreBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    #Handles the three run times
    RunTimeFrame = LabelFrame(fieldsFrame, text=" Run Times ", font=(Data.font, Data.fontSize))
    RunTimeFrame.grid(row=6, rowspan=2, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    Time1Label = Label(RunTimeFrame, text="Run Time 1:   ", font=(Data.font, Data.fontSize))
    Time1Label.grid(row=2, column=5, padx=5, pady=2)

    Time1Label2 = Label(RunTimeFrame, text=":", font=(Data.font, Data.fontSize))
    Time1Label2.grid(row=2, column=10, pady=2)

    Time1BoxMin = Entry(RunTimeFrame, width=2, font=(Data.font, Data.fontSize))
    Time1BoxMin.grid(row=2, column=8, pady=2)

    Time1BoxSec = Entry(RunTimeFrame, width=2, font=(Data.font, Data.fontSize))
    Time1BoxSec.grid(row=2, column=12, pady=2)

    Time2Label = Label(RunTimeFrame, text="Run Time 2:   ", font=(Data.font, Data.fontSize))
    Time2Label.grid(row=5, column=5, padx=5, pady=2)

    Time2Label2 = Label(RunTimeFrame, text=":", font=(Data.font, Data.fontSize))
    Time2Label2.grid(row=5, column=10, pady=2)

    Time2BoxMin = Entry(RunTimeFrame, width=2, font=(Data.font, Data.fontSize))
    Time2BoxMin.grid(row=5, column=8, pady=2)

    Time2BoxSec = Entry(RunTimeFrame, width=2, font=(Data.font, Data.fontSize))
    Time2BoxSec.grid(row=5, column=12, pady=2)

    Time3Label = Label(RunTimeFrame, text="Run Time 3:   ", font=(Data.font, Data.fontSize))
    Time3Label.grid(row=7, column=5, padx=5, pady=2)

    Time3Label2 = Label(RunTimeFrame, text=":", font=(Data.font, Data.fontSize))
    Time3Label2.grid(row=7, column=10, pady=2)

    Time3BoxMin = Entry(RunTimeFrame, width=2, font=(Data.font, Data.fontSize))
    Time3BoxMin.grid(row=7, column=8, pady=2)

    Time3BoxSec = Entry(RunTimeFrame, width=2, font=(Data.font, Data.fontSize))
    Time3BoxSec.grid(row=7, column=12, pady=2)

    #implements the check boxes
    HideScoresVal = IntVar()
    HideDisplayVal = IntVar()

    HideScoresCheck = Checkbutton(fieldsFrame, text=" Hide from Final Scores ", variable=HideScoresVal, font=(Data.font, Data.fontSize))
    HideDisplayCheck = Checkbutton(fieldsFrame, text=" Hide from Display ", variable=HideDisplayVal, font=(Data.font, Data.fontSize))

    HideScoresCheck.grid(row=2, column=1, sticky="w")
    HideDisplayCheck.grid(row=2, column=1, sticky="ws")

    #Implements Competition day drop-down
    DayFrame = LabelFrame(fieldsFrame, text=" Competition Day ", font=(Data.font, Data.fontSize))
    DayFrame.grid(row=3, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
    DayDrop = StringVar(DayFrame)
    DayDrop.set("  Select Day  ")  # default value
    DayDropMenu = OptionMenu(DayFrame, DayDrop, "  Saturday  ", "  Sunday  ")
    DayDropMenu.pack()

    #implements Competition type drop-down
    TypeFrame = LabelFrame(fieldsFrame, text=" Competition Type ", font=(Data.font, Data.fontSize))
    TypeFrame.grid(row=4, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
    TypeDrop = StringVar(TypeFrame)
    TypeDrop.set("  Select Competition Type  ")  # default value
    TypeDropMenu = OptionMenu(TypeFrame, TypeDrop, "  2-leg manual   ", "  2-leg overall  ", "  4-leg manual   ", "  4-leg overall  ")
    TypeDropMenu.pack()

    #Implements Oral Presentation Score
    OralFrame = LabelFrame(fieldsFrame, text=" Oral Presentation Score ", font=(Data.font, Data.fontSize))
    OralFrame.grid(row=5, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    OralBox = Entry(OralFrame, width=5, font=(Data.font, Data.fontSize))
    OralBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    #Implements Fabrication Score
    FabricationFrame = LabelFrame(fieldsFrame, text=" Fabrication Score ", font=(Data.font, Data.fontSize))
    FabricationFrame.grid(row=6, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    FabricationBox = Entry(FabricationFrame, width=5, font=(Data.font, Data.fontSize))
    FabricationBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # Implements control type optionMenu
    ControlFrame = LabelFrame(fieldsFrame, text=" Control Type ", font=(Data.font, Data.fontSize))
    ControlFrame.grid(row=7, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
    ControlDrop = StringVar(TypeFrame)
    ControlDrop.set("  Select Control Type  ")  # default value
    ControlDropMenu = OptionMenu(ControlFrame, ControlDrop, "  manual  ", "  auto  ", "  auto fb  ")
    ControlDropMenu.pack()

    #Implements Overall Score
    TotalFrame = LabelFrame(fieldsFrame, text=" Overall Score ", font=(Data.font, Data.fontSize))
    TotalFrame.grid(row=8, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    TotalBox = Entry(TotalFrame, width=5, font=(Data.font, Data.fontSize))
    TotalBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    #implements Comments Box
    CommentsFrame = LabelFrame(fieldsFrame, text=" Comments ", font=(Data.font, Data.fontSize))
    CommentsFrame.grid(row=9, column=0, columnspan=2, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    CommentsBox = Text(CommentsFrame, width=60, height=6, font=(Data.font, Data.fontSize))
    CommentsBox.pack()


    #Implements the Team Number listing
    teamNumVar = StringVar()
    teamNumVar.set("Team Number: " + str(Data.getItem("number")))
    TeamNumDisplay = Label(fieldsFrame, textvariable=teamNumVar, font=(Data.font, Data.fontSize))
    TeamNumDisplay.grid(row=1)

    # Binds an action to the list box
    listBox.bind("<Double-Button-1>", (lambda x: dbCommands.Search(listBox.get(listBox.curselection()[0]).split(":")[0], Data,
                                                        [SchoolBox, NameBox, WrittenReportScoreBox, TrackRunScoreBox,
                                                         CommentsBox, FabricationBox, OralBox, TotalBox, Time1BoxMin,
                                                         Time1BoxSec, Time2BoxMin, Time2BoxSec, Time3BoxMin,
                                                         Time3BoxSec, HideDisplayCheck, HideScoresCheck, DayDrop,
                                                         TypeDrop, teamNumVar, ControlDrop])))

    #Implements Update and Add Buttons
    UpdateButton = Button(fieldsFrame, text=" Update ", command=lambda: dbCommands.Update(NameBox.get(),\
                                                                                      SchoolBox.get(),\
                                                                                      WrittenReportScoreBox.get(),\
                                                                                      TrackRunScoreBox.get(),\
                                                                                      Time1BoxMin.get(),\
                                                                                      Time1BoxSec.get(),\
                                                                                      Time2BoxMin.get(),\
                                                                                      Time2BoxSec.get(),\
                                                                                      Time3BoxMin.get(),\
                                                                                      Time3BoxSec.get(),\
                                                                                      HideScoresVal.get(),\
                                                                                      HideDisplayVal.get(),\
                                                                                      DayDrop.get(),\
                                                                                      TypeDrop.get(),\
                                                                                      OralBox.get(),\
                                                                                      FabricationBox.get(),\
                                                                                      TotalBox.get(),\
                                                                                      CommentsBox.get("1.0", END),
                                                                                      Data, ControlDrop.get()), font=(Data.font, Data.fontSize))
    UpdateButton.grid(row=1, column=1, sticky="w")
    AddButton = Button(fieldsFrame, text=" Add Team ", command=lambda: AddNewGUI.AddNewGUI(Data), font=(Data.font, Data.fontSize))
    AddButton.grid(row=1, column=1)

    #Loops the window to keep it open
    root.mainloop()

# Function that handles exiting using the red X button
# Saves a copy of the database if still connected, then exits the program
# WORKS
def CloseAll(Data, root):
    if Data.connected is True:
        dbCommands.ExportData("autosave_on_exit", Data)
    dbCommands.CloseConnection(Data)
    root.destroy()
    sys.exit()

