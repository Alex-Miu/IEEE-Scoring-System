# Error GUI

from tkinter import *
from Backend import Errors

def ErrorPopup(code):
    root = Tk()
    root.title("Error")
    codes = Errors.Errors()

    errorLabel = Label(root, text="An Error Occurred! Error Code: " + code)
    errorMessage = Label(root, text=codes.getError(code))
    ok = Button(root, text=" Ok ", command=root.destroy)
    errorLabel.grid(row=0)
    errorMessage.grid(row=1)
    ok.grid(row=2, sticky="e")