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
                "014": "Could not open file!",
                "015": "Name is already Taken, please enter a different one.",
                "016": "Invalid time value in Run Time Input. Must be an integer of length 2 or less",
                "017": "Invalid input for Written Report Score - must be a number",
                "018": "Invalid input for Track Run Score - must be a number",
                "019": "Invalid input for Oral Score - must be a number",
                "020": "Invalid input for Fabrication Score - must be a number",
                "021": "Invalid input for Overall (total) Score - must be a number",
                "022": "Invalid name: Team Name cannot be empty",
                "023": "You must select an option for the Competition Day",
                "024": "You must select an option for the Competition Type",
                "025": "Team Number cannot be Null",
                "026": "Team Number must be a number",
                "027": "Team Number is already in use. Select a different Team Number",
                "028": "Failed to create final results table",
                "029": "Failed to write to file"
            }

    def getError(self, code):
        return self.errorList[str(code)]
