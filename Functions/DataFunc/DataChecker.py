#  Copyright (C) 2022-2023 - Willem van der Schans - All Rights Reserved.
#
#  THE CONTENTS OF THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL.
#  UNAUTHORIZED COPYING, TRANSFERRING OR REPRODUCTION OF THE CONTENTS OF THIS PROJECT, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
#  The receipt or possession of the source code and/or any parts thereof does not convey or imply any right to use them
#  for any purpose other than the purpose for which they were provided to you.
#
#  The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to
#  the warranties of merchantability, fitness for a particular purpose and non infringement.
#  In no event shall the authors or copyright holders be liable for any claim, damages or other liability,
#  whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software
#  or the use or other dealings in the software.
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#
#  THE CONTENTS OF THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL.
#  UNAUTHORIZED COPYING, TRANSFERRING OR REPRODUCTION OF THE CONTENTS OF THIS PROJECT, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
#  The receipt or possession of the source code and/or any parts thereof does not convey or imply any right to use them
#  for any purpose other than the purpose for which they were provided to you.
#
#
# Open FileBrowser
import os
from pathlib import Path

# If None don't do anything

# If File exists look for last date and time, set as starting date and time.

# After combine files and delete dupes.

import PySimpleGUI as sg
from API_Calls.Functions.Gui.ImageLoader import ImageLoader


def DataChecker(Name, Path):
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