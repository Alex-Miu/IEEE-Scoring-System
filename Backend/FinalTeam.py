from Backend import dbCommands

class FinalTeam:

    def __init__(self):
        self.orderOfItems = ["name", "number", "school", "written_report_score", "control_type", "fabrication_score", "track_run_1",
                             "track_run_2", "track_run_3", "track_run", "competition_day", "competition_type",
                             "oral_presentation_score", "overall_score", "comments", "place_manual_saturday",
                             "place_manual_sunday", "place_manual_both_days", "place_overall_saturday",
                             "place_overall_sunday", "place_overall_both_days", "place_total"]
        self.info = {}

        # Populates the self.info dictionary
        for i in self.orderOfItems:
            self.info[i] = "NULL"

    def Populate(self, teamInfo):
        for i in range(0, 15):
            self.info[self.orderOfItems[i]] = teamInfo[i]


    def genQuery(self):
        query = ""
        for i in self.orderOfItems:
            if i == self.orderOfItems[-1]:
                query += str(self.info[i])
            else:
                word = str(self.info[i])
                if dbCommands.is_number(word) is False:
                    if word == "None":
                        word = "NULL"
                    if word != "NULL":
                        word = "'" + word + "'"
                query += word + ", "
        print(query)
        return query
