from Resources.tkinter import *
from Backend import Errors

def ErrorPopup(code):
    root = Tk()
    root.title("Error")
    Codes = Errors.Errors()

    errorLabel = Label(root, text="An Error Occurred! Error Code: " + code)
    errorMessage = Label(root, text=Codes.getError(code))
    ok = Button(root, text=" Ok ", command=root.destroy)
    errorLabel.grid(row=0)
    errorMessage.grid(row=1)
    ok.grid(row=2, sticky="e")