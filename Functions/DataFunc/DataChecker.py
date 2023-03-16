# Open FileBrowser
import os
from pathlib import Path

# If None don't do anything

# If File exists look for last date and time, set as starting date and time.

# After combine files and delete dupes.

import PySimpleGUI as sg
from API_Calls.Functions.Gui.ImageLoader import ImageLoader


def DataChecker(Name, Path):
    __text1 = f"Select existing {Name} csv data file:"

    __Line1 = [sg.Push(),
               sg.Text(__text1, justification="center"),
               sg.Push()]

    __Line2 = [sg.Text("Choose a file: "),
               sg.Input(),
               sg.FileBrowse(file_types=(("Data Files (.csv)", "*.csv"),), initial_folder=Path)]

    __Line3 = [sg.Push(),
               sg.Ok("Continue"),
               sg.Cancel(),
               sg.Push()]

    window = sg.Window("Batch popup", [__Line1, __Line2, __Line3],
                       modal=True,
                       keep_on_top=True,
                       disable_close=False,
                       icon=ImageLoader("taskbar_icon.ico"))

    # Event Loop
    while True:
        event, values = window.read()
        if event == "Continue":
            break
        elif event == sg.WIN_CLOSED or event == "Cancel":
            #raise KeyboardInterrupt("User cancelled the program")
            break

    window.close()


DataChecker("Construction Monitor", Path(os.path.expanduser('~/Documents')))
# Create Path creator and general referencer.
    # Folder Name: Real Estate Data
    # SubFolders, based on Name reference?