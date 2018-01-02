from Resources.tkinter import *
from Backend import dbCommands

def ExportPopup(WorkData):
    root = Tk()
    root.title("Export Data")
    label1 = Label(root, text="Export all team information to a Microsoft Excel Document.", font=(WorkData.font, WorkData.fontSize))
    label2 = Label(root, text="Enter filename: ", font=(WorkData.font, WorkData.fontSize))
    nameBox = Entry(root, width=40)
    CancelButton = Button(root, text=" Cancel ", command=root.destroy, font=(WorkData.font, WorkData.fontSize))
    ExportButton = Button(root, text=" Export ", command=lambda: dbCommands.ExportData(nameBox.get(), WorkData), font=(WorkData.font, WorkData.fontSize))

    #adds stuff to the window
    label1.grid(row=0, column=0, columnspan=2)
    label2.grid(row=2, column=0)
    nameBox.grid(row=2, column=1)
    CancelButton.grid(row=3, column=1)
    ExportButton.grid(row=3, column=0)