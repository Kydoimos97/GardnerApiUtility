#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import os
from pathlib import Path

import PySimpleGUI as sg

from API_Calls.Functions.Gui.ImageLoader import ImageLoader


def DataChecker(Name, DataPath):
    """
The DataChecker function is used to check if the user has selected a valid data file.
    If the user selects an invalid file, they will be prompted to select another one until
    they choose a valid one.

Args:
    Name: Display the name of the data file that is being selected
    Path: Set the initial folder for the file browser

Returns:
    A list of all the data files in a directory

Doc Author:
    Willem van der Schans, Trelent AI
"""
    __text1 = f"Select existing {Name} csv data file:"

    __Line1 = [sg.Push(),
               sg.Text(__text1, justification="center"),
               sg.Push()]

    __Line2 = [sg.Text("Choose a file: "),
               sg.Input(),
               sg.FileBrowse(file_types=(("Data Files (.csv)", "*.csv"),), initial_folder=DataPath)]

    __Line3 = [sg.Push(),
               sg.Ok("Continue"),
               sg.Cancel(),
               sg.Push()]

    window = sg.Window("Batch popup", [__Line1, __Line2, __Line3],
                       modal=True,
                       keep_on_top=True,
                       disable_close=False,
                       icon=ImageLoader("taskbar_icon.ico"))

    while True:
        event, values = window.read()
        if event == "Continue":
            break
        elif event == sg.WIN_CLOSED or event == "Cancel":

            break

    window.close()


DataChecker("Construction Monitor", Path(os.path.expanduser('~/Documents')))
