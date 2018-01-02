# Filename: Team.py
# Project: Real Time Scoring System
# Organization: IEEE - UMBC Student Branch
# Author: Alex Miu
# Date: 11/28/2017
# Description: This file contains the class definition for the Team Class, which will contain all of the data related to a team participating in the competition.

# imports
import json
import ast

class Team:

    # Constructor - Meant for making objects from scratch by inputting all of the required fields
    def __init__(self, name, number, school, written_report_score=None, track_run_1=None, track_run_2=None, track_run_3=None, track_run=None, competition_day=None, competition_type=None, oral_presentation_score=None, fabrication_score=None, overall_score=None, comments=None, hide_from_display=False, hide_from_final_scores=False, control_type=None):
        self.info = {
                     "name": name,
                     "number": number,
                     "school": school,
                     "written_report_score": written_report_score,
                     "track_run_1": track_run_1,
                     "track_run_2": track_run_2,
                     "track_run_3": track_run_3,
                     "track_run": track_run,
                     "competition_day": competition_day,
                     "competition_type": competition_type,
                     "oral_presentation_score": oral_presentation_score,
                     "fabrication_score": fabrication_score,
                     "overall_score": overall_score,
                     "comments": comments,
                     "hide_from_display": hide_from_display,
                     "hide_from_final_scores": hide_from_final_scores,
                     "control_type": control_type
                    }
        self.options = ["name", "number", "school", "written_report_score", "control_type", "fabrication_score", "track_run_1", "track_run_2", "track_run_3",
                   "track_run", "competition_day", "competition_type", "oral_presentation_score",
                   "overall_score", "comments", "hide_from_display", "hide_from_final_scores"]

    # Returns a JSON object of the team information
    #TODO this doesn't work
    def ToJSON(self):
        return json.dumps(self.info)

    def FromJSON(self, object):
        self.info = json.loads(json.dumps(object))

    def Change(self, newTeam):
        self.info = newTeam

    def getItem(self, key):
        return self.info[key]

    def Translate(self, newData):
        # All of the options
        newDict = {}
        for i in range(0, len(newData[0])):
            newDict[self.options[i]] = newData[0][i]
        return newDict

