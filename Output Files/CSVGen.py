# Randomly generates a bunch of teams
from Resources import random
from Backend import dbCommands

Dates = ["  Saturday  ", "  Sunday  "]
Types = ["  2-leg manual   ", "  2-leg overall  ", "  4-leg manual   ", "  4-leg overall  "]
ControlTypes = ["  manual  ", "  auto  ", "  auto fb  "]
School = "School"


Teams = []
for number in range(0, 300):
    teamName = "Team " + str(number)
    hide_from_display = 0
    hide_from_final_scores = 0
    control_type = random.sample(ControlTypes, 1)[0]
    competition_type = random.sample(Types, 1)[0]
    day = random.sample(Dates, 1)[0]
    track_score = random.randint(1, 101)
    overall_score = random.randint(1, 101)
    timeList = []
    for i in range(6):
        timeList.append(random.randint(1, 60))
    fabrication = random.randint(1, 101)
    oral_score = random.randint(1, 101)
    written_score = random.randint(1, 101)

    track_run_1 = str(timeList[0]) + ":" + str(timeList[1])
    track_run_2 = str(timeList[2]) + ":" + str(timeList[3])
    track_run_3 = str(timeList[4]) + ":" + str(timeList[5])

    row = ""
    list_things = [teamName, number, School, written_score, control_type, fabrication, track_run_1, track_run_2, track_run_3, track_score, day, competition_type, oral_score, overall_score, "Comments Section", hide_from_display, hide_from_final_scores]
    for i in range(len(list_things)):
        if i == len(list_things) - 1:
            row += str(list_things[i])
        else:
            if dbCommands.is_number is False:
                row += "'" + str(list_things[i]) + "',"
            else:
                row += str(list_things[i]) + ","

    Teams.append(row)

file = open("SampleData.csv", "w")
file.write("teamName,number,School,written_score,control_type,fabrication,track_run_1,track_run_2,track_run_3,track_score,day,competition_type,oral_score,overall_score,Comments Section,hide_from_display,hide_from_final_scores")
for row in Teams:
    file.write(row)
    file.write("\n")
file.close()
