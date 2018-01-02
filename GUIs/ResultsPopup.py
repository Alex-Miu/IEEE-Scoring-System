from Resources.tkinter import *
from Backend import dbCommands

def ResultsPopup(Data):
    root = Tk()
    root.title("Get Results")

    Sat = IntVar()
    Sun = IntVar()
    Saturday = Checkbutton(root, text="Include teams from Saturday", variable=Sat, font=(Data.font, Data.fontSize))
    Sunday = Checkbutton(root, text="Include teams from Sunday", variable=Sun, font=(Data.font, Data.fontSize))
    nameBox = Entry(root, width=40, font=(Data.font, Data.fontSize))
    label1 = Label(root, text="Enter Results Name: ", font=(Data.font, Data.fontSize))
    Cancel = Button(root, text=" Cancel ", command=root.destroy, font=(Data.font, Data.fontSize))
    Finalize = Button(root, text=" Generate Results ", command=lambda: dbCommands.Finalize(Sat.get(), Sun.get(), Data, nameBox.get()), font=(Data.font, Data.fontSize))

    Saturday.grid(row=0, column=0, columnspan=2)
    Sunday.grid(row=1, column=0, columnspan=2)
    label1.grid(row=2, column=0)
    nameBox.grid(row=2, column=1)
    Cancel.grid(row=3, column=1)
    Finalize.grid(row=3, column=0)