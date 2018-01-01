# Main() Function, this is where the program starts

from GUIs import DisplayGUI
import json

def Main():

    # Sets a default settings list in case the Config.txt file could not be found
    settings = {
                "dbName": "testing",
                "dbIP": "127.0.0.1",
                "dbTable": "`maintable`",
                "dbUser": "program",
                "dbPass": "program",
                "fontSize": 10,
                "delay": 10,
                "MAXheight": 30
                }

    # Gets default font from Config.txt
    try:
        # Reads File
        configFile = open("Config.txt", "r")
        dataDump = configFile.read()
        configFile.close()
        settingsJSON = json.loads(dataDump)

        # Sets values
        settingsList = ["fontSize", "dbName", "dbTable", "dbIP", "dbUser", "dbPass", "delay", "MAXheight"]

        for i in settingsList:
            if i in settingsJSON:
                if i is "delay":
                    settings[i] = int(settingsJSON[i])
                settings[i] = settingsJSON[i]

    except Exception as e:
        print(e)

    # Launches master GUI
    DisplayGUI.Launch(settings)


Main()
