#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/

import PySimpleGUI as sg

from API_Calls.Functions.Gui.ImageLoader import ImageLoader


def BatchInputGui(batches, documentCount=None):
    """
The BatchInputGui function is a simple GUI that displays the number of batches and pages
that will be requested. It also gives the user an option to cancel or continue with their request.


Args:
    batches: Determine how many batches will be run
    documentCount: Determine how many documents will be retrieved

Returns:
    The event, which is the button that was pressed

Doc Author:
    Willem van der Schans, Trelent AI
"""
    event = None
    if documentCount is None:
        __text1 = f"This request will run {batches}"
    else:
        __text1 = f"This request will run {batches} batches and will retrieve {documentCount} rows"

    __text2 = "Press Continue to start request"

    __Line1 = [sg.Push(),
               sg.Text(__text1, justification="center"),
               sg.Push()]

    __Line2 = [sg.Push(),
               sg.Text(__text2, justification="center"),
               sg.Push()]

    __Line3 = [sg.Push(),
               sg.Ok("Continue"),
               sg.Cancel(),
               sg.Push()]

    window = sg.Window("Popup", [__Line1, __Line2, __Line3],
                       modal=True,
                       keep_on_top=True,
                       disable_close=True,
                       icon=ImageLoader("taskbar_icon.ico"))

    while True:
        event, values = window.read()
        if event == "Continue":
            break
        elif event == sg.WIN_CLOSED or event == "Cancel":
            break

    window.close()

    return event


def confirmDialog():
    """
The confirmDialog function is a simple confirmation dialog that asks the user if they want to continue with the request.
The function takes no arguments and returns the button event to allow for process confirmation.

Args:

Returns:
    The event that was triggered,

Doc Author:
    Willem van der Schans, Trelent AI
"""
    event = None
    __text1 = f"This request can take multiple minutes to complete"
    __text2 = "Press Continue to start the request"

    __Line1 = [sg.Push(),
               sg.Text(__text1, justification="center"),
               sg.Push()]

    __Line2 = [sg.Push(),
               sg.Text(__text2, justification="center"),
               sg.Push()]

    __Line3 = [sg.Push(),
               sg.Ok("Continue"),
               sg.Cancel(),
               sg.Push()]

    window = sg.Window("Popup", [__Line1, __Line2, __Line3],
                       modal=True,
                       keep_on_top=True,
                       disable_close=True,
                       icon=ImageLoader("taskbar_icon.ico"))

    while True:
        event, values = window.read()
        if event == "Continue":
            break
        elif event == sg.WIN_CLOSED or event == "Cancel":
            break

    window.close()

    return event
