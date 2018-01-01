from tkinter import *
from Backend import dbCommands
from json import *


# Function that should save the new information to the config file
def SaveData(dbName, dbIP, dbUser, dbPass, DataClass, fontSize, dbTable, backupTime):
    DataClass.systemText.set("Saving settings...")

    config = open("Config.txt", "w")
    information = {"dbName": dbName, "dbIP": dbIP, "dbUser": dbUser, "dbPass": dbPass, "dbTable": dbTable, "backup": backupTime, "fontSize": fontSize}
    data = loads(dumps(information))
    config.write(dumps(data))
    config.close()
    DataClass.setFontSize(fontSize)
    DataClass.dbName = dbName
    DataClass.dbIP = dbIP
    DataClass.dbUser = dbUser
    DataClass.dbTable = "`" + dbTable.strip("`") + "`"
    DataClass.dbPass = dbPass
    DataClass.backup = backupTime


# Function that runs the settings Window
def SettingsGUI(DataClass, listBox):
    root = Tk()
    root.title("Settings")

    # TODO ADD A CATCH FOR IF THING IS EMPTY
    config = open("Config.txt", "r")
    settings = config.read()
    settings = loads(settings)

    #Software Font Size
    fontLabel = Label(root, text="Font Size: ", font=(DataClass.font, DataClass.fontSize))
    fontLabel.grid(row=0, column=0, padx=2, pady=2)

    fontSizeBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    fontSizeBox.insert(0, DataClass.fontSize)
    fontSizeBox.grid(row=0, column=1, padx=2, pady=2)


    #Database Name Information
    dbNameLabel = Label(root, text="Database Name: ", font=(DataClass.font, DataClass.fontSize))
    dbNameLabel.grid(row=1, column=0, padx=2, pady=2)

    dbNameBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbNameBox.insert(0, DataClass.dbName)
    dbNameBox.grid(row=1, column=1, padx=2, pady=2)


    #Database IP Address
    dbIPLabel = Label(root, text="Database IP Address: ", font=(DataClass.font, DataClass.fontSize))
    dbIPLabel.grid(row=2, column=0, padx=2, pady=2)

    dbIPBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbIPBox.insert(0, DataClass.dbIP)
    dbIPBox.grid(row=2, column=1, padx=2, pady=2)


    #Database Username information
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

    dbTableBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    dbTableBox.insert(0, DataClass.dbTable.strip("`"))
    dbTableBox.grid(row=5, column=1, padx=2, pady=2)

    # Autosave time increment
    autoLabel = Label(root, text="Auto-save Time Increment (ms): ", font=(DataClass.font, DataClass.fontSize))
    autoLabel.grid(row=6, column=0, padx=2, pady=2)

    autoBox = Entry(root, font=(DataClass.font, DataClass.fontSize))
    autoBox.insert(0, DataClass.backup)
    autoBox.grid(row=6, column=1, padx=2, pady=2)

    #Implements buttons at the bottom of the window, including Save, Cancel, and Re-connect
    ButtonFrame = Frame(root)
    ButtonFrame.grid(row=7, column=0, columnspan=2)

    ReconnectButton = Button(ButtonFrame, text=" Connect ", font=(DataClass.font, DataClass.fontSize), command=lambda: dbCommands.Connect(dbNameBox.get(), dbIPBox.get(), dbUserBox.get(), dbPassBox.get(), DataClass, dbTableBox.get(), listBox))
    ReconnectButton.grid(row=0, column=0)

    SaveButton = Button(ButtonFrame, text=" Save ", font=(DataClass.font, DataClass.fontSize), command=lambda: SaveData(dbNameBox.get(), dbIPBox.get(), dbUserBox.get(), dbPassBox.get(), DataClass, fontSizeBox.get(), dbTableBox.get(), autoBox.get()))
    SaveButton.grid(row=0, column=1)

    CancelButton = Button(ButtonFrame, text=" Cancel ", font=(DataClass.font, DataClass.fontSize), command=root.destroy)
    CancelButton.grid(row=0, column=2)