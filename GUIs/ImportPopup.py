from tkinter import *
from tkinter import filedialog
from Backend import dbCommands


# tkinter function that opens a file browser to locate the desired filepath
def getFile(fileNameBox):
    filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("excel files","*.xlsx"),("csv files","*.csv"),("all files","*.*")))
    fileNameBox.delete(0, END)
    return filename

def ImportPopup(Data):
    root = Tk()
    root.title("Import Data")

    # Generates GUI information
    SelectButton = Button(root, text=" Browse ", command =lambda: fileNameBox.insert(0, getFile(fileNameBox)), font=(Data.font, Data.fontSize))
    CancelButton = Button(root, text=" Cancel ", command=root.destroy, font=(Data.font, Data.fontSize))
    ImportButton = Button(root, text=" Import ", command=lambda: dbCommands.ImportData(fileNameBox.get(), Drop.get(), Data), font=(Data.font, Data.fontSize))
    label1 = Label(root, text="Enter File Name", font=(Data.font, Data.fontSize))
    fileNameBox = Entry(root, width=50, font=(Data.font, Data.fontSize))
    Drop = StringVar(root)
    Drop.set("  Select Data Type  ")  # default value
    DropMenu = OptionMenu(root, Drop, "  Team Information  ", "  Written Report Scores  ", "  Table Backup  ")

    # Draws the GUI
    DropMenu.grid(row=0, column=1)
    label1.grid(row=1, column=0)
    fileNameBox.grid(row=1, column=1)
    SelectButton.grid(row=1, column=2)
    CancelButton.grid(row=2, column=2)
    ImportButton.grid(row=2, column=1)
