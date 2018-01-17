class Errors:

    def __init__(self):
        self.errorList = \
            {
                "000": "Unkown Error",
                "001": "Failed to Connect",
                "002": "Failed to retrieve team information",
                "003": "Failed to add team",
                "004": "Could not find team",
                "005": "Already connected",
                "006": "Lost connection with server",
                "007": "Failed to update team information",
                "008": "Failed to download complete table",
                "009": "Downloaded selection is empty",
                "010": "Not connected to database",
                "011": "Failed to import information. No changes saved to database",
                "012": "Failed to load information into Database",
                "013": "Failed to retrieve list of teams",
                "014": "Problem occurred with query"
            }

    def getError(self, code):
        return self.errorList[str(code)]
