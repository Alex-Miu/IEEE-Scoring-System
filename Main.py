from GUIs import JudgeGUI
from Resources import json

def main():
    # Sets a default settings list in case the Config.txt file could not be found
    settings = {
        "dbName": "testing",
        "dbIP": "127.0.0.1",
        "dbTable": "`maintable`",
        "dbUser": "program",
        "dbPass": "program",
        "fontSize": 10,
        "backup": 30000,
    }

    # Gets default font from Config.txt
    try:
        # Reads File
        configFile = open("Backend/Config.txt", "r")
        dataDump = configFile.read()
        configFile.close()
        settingsJSON = json.loads(dataDump)

        # Sets values
        settingsList = ["fontSize", "dbName", "dbTable", "dbIP", "dbUser", "dbPass", "backup"]

        for i in settingsList:
            if i in settingsJSON:
                if i is "backup":
                    settings[i] = int(settingsJSON[i])
                settings[i] = settingsJSON[i]

    except Exception as e:
        print(e)

    # Launches master GUI
    JudgeGUI.JudgeGUI(settings)


main()
