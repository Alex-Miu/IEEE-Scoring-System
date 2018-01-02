from tkinter import *
from Backend import dbCommands

def AddNewGUI(Data):
    root = Tk()
    root.title("Add New Team")

    # Creates the frame with all of the data fields in it
    fieldsFrame = Frame(root)
    fieldsFrame.pack(side="left", fill="both", anchor="w", expand=True)

    # Works with Team Name
    NameFrame = LabelFrame(fieldsFrame, text=" Team Name ", font=(Data.font, Data.fontSize))
    NameFrame.grid(row=2, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    NameBox = Entry(NameFrame, width=40, font=(Data.font, Data.fontSize))
    NameBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # Works with School
    SchoolFrame = LabelFrame(fieldsFrame, text=" School ", font=(Data.font, Data.fontSize))
    SchoolFrame.grid(row=3, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    SchoolBox = Entry(SchoolFrame, width=40, font=(Data.font, Data.fontSize))
    SchoolBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # Handles written report score
    WrittenReportScoreFrame = LabelFrame(fieldsFrame, text=" Written Report Score ", font=(Data.font, Data.fontSize))
    WrittenReportScoreFrame.grid(row=4, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    WrittenReportScoreBox = Entry(WrittenReportScoreFrame, width=10, font=(Data.font, Data.fontSize))
    WrittenReportScoreBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # Handles track run score
    TrackRunScoreFrame = LabelFrame(fieldsFrame, text=" Track Run Score ", font=(Data.font, Data.fontSize))
    TrackRunScoreFrame.grid(row=5, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    TrackRunScoreBox = Entry(TrackRunScoreFrame, width=10, font=(Data.font, Data.fontSize))
    TrackRunScoreBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # Handles the three run times
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

    # implements the check boxes
    HideScoresVal = IntVar()
    HideDisplayVal = IntVar()

    HideScoresCheck = Checkbutton(fieldsFrame, text=" Hide from Final Scores ", variable=HideScoresVal, font=(Data.font, Data.fontSize))
    HideDisplayCheck = Checkbutton(fieldsFrame, text=" Hide from Display ", variable=HideDisplayVal, font=(Data.font, Data.fontSize))

    HideScoresCheck.grid(row=2, column=1, sticky="w")
    HideDisplayCheck.grid(row=2, column=1, sticky="ws")

    # Implements Competition day drop-down
    DayFrame = LabelFrame(fieldsFrame, text=" Competition Day ", font=(Data.font, Data.fontSize))
    DayFrame.grid(row=3, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
    DayDrop = StringVar(DayFrame)
    DayDrop.set("  Select Day  ")  # default value
    DayDropMenu = OptionMenu(DayFrame, DayDrop, "  Saturday    ", "  Sunday      ")
    DayDropMenu.pack()

    # implements Competition type drop-down
    TypeFrame = LabelFrame(fieldsFrame, text=" Competition Type ", font=(Data.font, Data.fontSize))
    TypeFrame.grid(row=4, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
    TypeDrop = StringVar(TypeFrame)
    TypeDrop.set("  Select Competition Type  ")  # default value
    TypeDropMenu = OptionMenu(TypeFrame, TypeDrop, "  2-leg manual   ", "  2-leg overall  ", "  4-leg manual   ",
                              "  4-leg overall  ")
    TypeDropMenu.pack()

    # Implements Oral Presentation Score
    OralFrame = LabelFrame(fieldsFrame, text=" Oral Presentation Score ", font=(Data.font, Data.fontSize))
    OralFrame.grid(row=5, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    OralBox = Entry(OralFrame, width=5, font=(Data.font, Data.fontSize))
    OralBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # Implements Fabrication Score
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

    # Implements Overall Score
    TotalFrame = LabelFrame(fieldsFrame, text=" Overall Score ", font=(Data.font, Data.fontSize))
    TotalFrame.grid(row=8, column=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    TotalBox = Entry(TotalFrame, width=5, font=(Data.font, Data.fontSize))
    TotalBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # implements Comments Box
    CommentsFrame = LabelFrame(fieldsFrame, text=" Comments ", font=(Data.font, Data.fontSize))
    CommentsFrame.grid(row=9, column=0, columnspan=2, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    CommentsBox = Text(CommentsFrame, width=60, height=6, font=(Data.font, Data.fontSize))
    CommentsBox.pack()

    # Implements the Team Number listing
    NumberFrame = LabelFrame(fieldsFrame, text=" Team Number ", font=(Data.font, Data.fontSize))
    NumberFrame.grid(row=1, column=0, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    NumberBox = Entry(NumberFrame, width=5, font=(Data.font, Data.fontSize))
    NumberBox.grid(row=2, column=5, columnspan=8, padx=20, pady=2)

    # Implements Update and Add Buttons
    # TODO add function call
    DoneButton = Button(fieldsFrame, text=" Add ", font=(Data.font, Data.fontSize), command=lambda: dbCommands.AddTeam(NumberBox.get(),\
                                                                                      NameBox.get(),\
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
                                                                                      Data,
                                                                                      ControlDrop.get()))
    DoneButton.grid(row=1, column=1, sticky="w")

    root.mainloop()