#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/

import PySimpleGUI as sg

from API_Calls.Functions.Gui.ImageLoader import ImageLoader


def BatchInputGui(batches):
    """
The BatchInputGui function is a simple GUI that asks the user if they want to continue with the number of batches
that have been selected. This function is called by the BatchInputGui function in order to confirm that this is what
the user wants.

Args:
    batches: Display the number of batches that will be run

Returns:
    A boolean value

Doc Author:
    Willem van der Schans, Trelent AI
"""
    __text1 = f"This request will run {batches} batches"
    __text2 = "Press Continue to start request"

    __Line1 = [sg.Push(),
               sg.Text(__text1, justification="center"),
               sg.Push()]

    __Line2 = [sg.Push(),
               sg.Text(__text2, justification="center"),
               sg.Push()]

    __Line3 = [sg.Push(),
               sg.Ok("Continue"),
               sg.Push()]

    window = sg.Window("Batch popup", [__Line1, __Line2, __Line3],
                       modal=True,
                       keep_on_top=True,
                       disable_close=True,
                       icon=ImageLoader("taskbar_icon.ico"),
                       size=(290, 100))

    while True:
        event, values = window.read()
        if event == "Continue":
            break
        elif event == sg.WIN_CLOSED or event == "Cancel":

            break

    window.close()
