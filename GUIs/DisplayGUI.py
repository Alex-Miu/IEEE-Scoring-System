# Main Display GUI function

from tkinter import *
from Backend import DataManager
from GUIs import SettingsPopup
from Backend import dbCommands

def Launch(defaultSettings):

    # Initializes Active Data Object to store running information
    data = DataManager.DataManager(defaultSettings)

    # Generates window
    data.window = Tk()
    data.window.title("Display System")

    data.displayTitle = StringVar()
    data.displayTitle.set("DISPLAY SYSTEM")

    titleLabel = Label(data.window, textvariable=data.displayTitle, font=(data.font, 20))
    titleLabel.grid(row=0, column=0, columnspan=2)

    # Creates Row Frame and the row titles
    data.titleFrame = Frame(data.window)
    data.titleFrame.grid(row=1, column=0, columnspan=2, sticky=W)
    columnNames = [" Team # ", " School ", " Team Name ", " Type ", " Written Rep ", " Track Run ",
                   " Oral Pres ", " Fabrication ", " Overall Score ", " Run Time 1 ", " Run Time 2 ",
                   " Run Time 3 ", " Day "]
    for titleIndex in range(len(columnNames)):
        box = Label(data.titleFrame, text=("\n" + columnNames[titleIndex] + "\n"), borderwidth=1, relief="solid",
                    width=data.colSize[titleIndex],
                    font=(data.font, data.fontSize), bg="white")
        box.grid(row=0, rowspan=3, column=titleIndex, sticky=N)

    # Draws the table with the dat in it
    Draw(data)

    # Menu bar along the top
    menubar = Menu(data.window, font=(data.font, data.fontSize))
    menubar.add_command(label="Settings", command=lambda: SettingsPopup.Launch(data, data.root))
    menubar.add_command(label="Disconnect", command=lambda: dbCommands.CloseConnection(data))
    menubar.add_command(label="Switch", command=lambda: dbCommands.CycleThrough(data))
    menubar.add_command(label="Display Results", command=lambda: dbCommands.SwitchToFinal(data))
    data.window.config(menu=menubar)

    # rebinds the close window option to ensure the server is disconnected
    data.window.protocol('WM_DELETE_WINDOW', lambda: CloseAll(data))

    data.window.mainloop()


# Function that handles exiting using the red X button
# Saves a copy of the database if still connected, then exits the program
# WORKS
def CloseAll(data):
    dbCommands.CloseConnection(data)
    data.window.destroy()
    sys.exit()

def Draw(data):
    print("Drawing...")
    if data.cFrame is not None:
        data.cFrame.destroy()

    # Creates a Frame for the canvas and its scroll bar
    data.cFrame = Frame(data.window, width=data.window.winfo_width(), height=100)
    data.cFrame.grid(row=2, column=0, sticky=N)

    # Creates the Canvas
    data.root = Canvas(data.cFrame, scrollregion=(0, 0, 1500, 800))

    # Resets the tableValues
    data.tableValues = [[StringVar() for i in range(data.width)] for j in range(data.height)]

    print("ROWS: " + str(data.height))
    print("WIDTH: " + str(data.width))
    # Sets default empty strings to all labels
    for i in range(0, data.height):  # Rows
        for j in range(0, data.width):  # Columns
            data.tableValues[i][j].set("")

    # places a frame inside the canvas
    data.inside = Frame(data.root)
    data.inside.pack(fill="both")

    # Draws the grid in the canvas
    for i in range(data.height):  # Rows
        for j in range(data.width):  # Columns
            box = Label(data.inside, textvariable=data.tableValues[i][j], borderwidth=1, relief="solid",
                        width=data.colSize[j],
                        font=(data.font, data.fontSize), bg="white")
            box.grid(row=i, column=j)

    data.root.pack(side="left", fill="both", expand=True, anchor=N)

    print("Done Drawing")

# Re-builds the entire window to account for the new infomration
def DrawWinnerWindow(data, newType):
    data.titleFrame.destroy()
    data.titleFrame = Frame(data.window)
    data.titleFrame.grid(row=1, column=0, columnspan=2, sticky=W)
    if newType == "  2-leg  " or newType == "  4-leg  ":
        # Creates Row Frame and the row titles
        for titleIndex in range(len(data.resultsCategories)):
            box = Label(data.titleFrame, text=(data.resultsCategories[titleIndex][0]), borderwidth=1, relief="solid",
                        width=data.resultsCategories[titleIndex][1],
                        font=(data.font, data.fontSize), bg="white")
            box.grid(row=0, rowspan=3, column=titleIndex, sticky=N)
    else:
        columnNames = [" Team # ", " School ", " Team Name ", " Type ", " Written Rep ", " Track Run ",
                       " Oral Pres ", " Fabrication ", " Overall Score ", " Run Time 1 ", " Run Time 2 ",
                       " Run Time 3 ", " Day "]
        for titleIndex in range(len(columnNames)):
            box = Label(data.titleFrame, text=("\n" + columnNames[titleIndex] + "\n"), borderwidth=1, relief="solid",
                        width=data.colSize[titleIndex],
                        font=(data.font, data.fontSize), bg="white")
            box.grid(row=0, rowspan=3, column=titleIndex, sticky=N)