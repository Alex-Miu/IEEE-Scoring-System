# File that contains functions used to reorganize data to fit into specified formats

from GUIs import DisplayGUI


# Function that receives the query response for a given category, and reorganizes it then inserts it into thing
def InsertToTable(data, dataDump):

    orderList = [2, 0, 1, 4, 3, 7, 9, 10, 11, 5, 12, 100, 6, 8]

    print("Inserting items into table...")

    # Sets the number of rows and asks for a re-draw
    data.height = len(dataDump)
    data.tableValues = None
    DisplayGUI.Draw(data)

    # Preps the offset so that the next request either gets the rest or moves on
    if len(dataDump) == int(data.MAXheight):
        data.offset += int(data.MAXheight)
        print("NEW OFFSET: " + str(data.offset))
    else:
        data.offset = 0

    for i in range(0, len(dataDump)):
        for col in range(0, 14):
            if col != 11:
                if dataDump[i][col] is None or dataDump[i][col] == ":":
                    data.tableValues[i][orderList[col]].set("")

                # Sets the Day to the proper acronym
                elif orderList[col] is 12:
                    if dataDump[i][col].strip() == "Sunday":
                        data.tableValues[i][orderList[col]].set("Su")
                    elif dataDump[i][col].strip() == "Saturday":
                        data.tableValues[i][orderList[col]].set("Sat")
                    else:
                        data.tableValues[i][orderList[col]].set("")

                else:
                    data.tableValues[i][orderList[col]].set(dataDump[i][col])

def InsertToWinningTable(data, dataDump):
    orderList = [1, 2, 0, 11, 15, 16, 17, 18, 19, 20]

    print("Inserting items into table...")

    # Sets the number of rows and asks for a re-draw
    data.height = len(dataDump)
    data.tableValues = None
    DisplayGUI.Draw(data)

    # Preps the offset so that the next request either gets the rest or moves on
    if len(dataDump) == int(data.MAXheight):
        data.offset += int(data.MAXheight)
        print("NEW OFFSET: " + str(data.offset))
    else:
        data.offset = 0

    for i in range(0, len(dataDump)):
        print(dataDump[i])
        for col in range(0, 10):
            print("i = " + str(i))
            print("col = " + str(col))
            print(data.tableValues[i][col].get())
            if dataDump[i][orderList[col]] is None or dataDump[i][orderList[col]] == "NULL":
                data.tableValues[i][col].set("")

            else:
                data.tableValues[i][col].set(dataDump[i][orderList[col]])