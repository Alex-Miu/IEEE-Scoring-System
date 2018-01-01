# Settings GUI and SaveData function
from tkinter import *
from Backend import dbCommands
import json


def SaveData(name, ip, user, passW, data, textSize, table, wait, newheight, day):

    # Saves all settings to the working data class
    data.dbName = name
    data.dbIP = ip
    data.dbTable = "`" + table + "`"
    data.dbUser = user
    data.dbPass = passW
    data.fontSize = textSize
    data.delay = wait
    data.MAXheight = newheight
    data.today = day

    # Saves settings to the file
    config = open("Config.txt", "w")
    information = {"dbName": data.dbName, "dbIP": data.dbIP, "dbUser": data.dbUser, "dbPass": data.dbPass, "dbTable": data.dbTable,
                   "delay": data.delay, "fontSize": data.fontSize, "MAXheight": data.MAXheight}
    data = json.loads(json.dumps(information))
    config.write(json.dumps(data))
    config.close()

def Launch(DataClass, titleLabel):
    root = Tk()
    root.title("Settings")

    # Software Font Size
    fontLabel = Label(root, text="Font Size: ", font=(DataClass.font, DataClass.fontSize))
    fontLabel.grid(row=0, column=0, padx=2, pady=2)

    fontSizeBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    fontSizeBox.insert(0, DataClass.fontSize)
    fontSizeBox.grid(row=0, column=1, padx=2, pady=2)

    # Database Name Information
    dbNameLabel = Label(root, text="Database Name: ", font=(DataClass.font, DataClass.fontSize))
    dbNameLabel.grid(row=1, column=0, padx=2, pady=2)

    dbNameBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbNameBox.insert(0, DataClass.dbName)
    dbNameBox.grid(row=1, column=1, padx=2, pady=2)

    # Database IP Address
    dbIPLabel = Label(root, text="Database IP Address: ", font=(DataClass.font, DataClass.fontSize))
    dbIPLabel.grid(row=2, column=0, padx=2, pady=2)

    dbIPBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbIPBox.insert(0, DataClass.dbIP)
    dbIPBox.grid(row=2, column=1, padx=2, pady=2)

    # Database Username information
    dbUserLabel = Label(root, text="Database Username: ", font=(DataClass.font, DataClass.fontSize))
    dbUserLabel.grid(row=3, column=0, padx=2, pady=2)

    dbUserBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbUserBox.insert(0, DataClass.dbUser)
    dbUserBox.grid(row=3, column=1, padx=2, pady=2)

    # Database Password
    dbPassLabel = Label(root, text="Database Password: ", font=(DataClass.font, DataClass.fontSize))
    dbPassLabel.grid(row=4, column=0, padx=2, pady=2)

    dbPassBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbPassBox.insert(0, DataClass.dbPass)
    dbPassBox.grid(row=4, column=1, padx=2, pady=2)

    # Database Table name
    dbTableLabel = Label(root, text="Database Table Name: ", font=(DataClass.font, DataClass.fontSize))
    dbTableLabel.grid(row=5, column=0, padx=2, pady=2)

    tableWord = DataClass.dbTable.strip("`")
    dbTableBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbTableBox.insert(0, tableWord)
    dbTableBox.grid(row=5, column=1, padx=2, pady=2)

    # switch display time increment
    autoLabel = Label(root, text="Wait time before switch (s): ", font=(DataClass.font, DataClass.fontSize))
    autoLabel.grid(row=6, column=0, padx=2, pady=2)

    autoBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    autoBox.insert(0, DataClass.delay)
    autoBox.grid(row=6, column=1, padx=2, pady=2)

    # Maxiumum number of rows to display at any given time
    heightLabel = Label(root, text="Maximum number of rows to display: ", font=(DataClass.font, DataClass.fontSize))
    heightLabel.grid(row=7, column=0, padx=2, pady=2)

    heightBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    heightBox.insert(0, DataClass.MAXheight)
    heightBox.grid(row=7, column=1, padx=2, pady=2)

    # Requests the current day of the competition
    DayLabel = Label(root, text="Current Day: ", font=(DataClass.font, DataClass.fontSize))
    DayLabel.grid(row=8, column=0, padx=2, pady=2)

    DayBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    DayBox.insert(0, DataClass.today)
    DayBox.grid(row=8, column=1, padx=2, pady=2)

    # Implements buttons at the bottom of the window, including Save, Cancel, and Re-connect
    ButtonFrame = Frame(root)
    ButtonFrame.grid(row=9, column=0, columnspan=2)

    ReconnectButton = Button(ButtonFrame, text=" Connect ", font=(DataClass.font, DataClass.fontSize),
                             command=lambda: dbCommands.Connect(dbNameBox.get(), dbIPBox.get(), dbUserBox.get(),
                                                                dbPassBox.get(), DataClass, dbTableBox.get(), titleLabel, DayBox.get()))
    ReconnectButton.grid(row=0, column=0)

    SaveButton = Button(ButtonFrame, text=" Save ", font=(DataClass.font, DataClass.fontSize),
                        command=lambda: SaveData(dbNameBox.get(), dbIPBox.get(), dbUserBox.get(), dbPassBox.get(),
                                                 DataClass, fontSizeBox.get(), dbTableBox.get(), autoBox.get(), heightBox.get(), DayBox.get()))
    SaveButton.grid(row=0, column=1)

    CancelButton = Button(ButtonFrame, text=" Cancel ", font=(DataClass.font, DataClass.fontSize), command=root.destroy)
    CancelButton.grid(row=0, column=2)

