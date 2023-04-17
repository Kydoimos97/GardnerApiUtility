#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped


def ErrorPopup(textString):
    """
The ErrorPopup function is used to display a popup window with an error message.
It takes one argument, textString, which is the string that will be displayed in the popup window.
The function also opens up the log folder upon program exit.

Args:
    textString: Display the error message

Returns:
    Nothing, but it does print an error message to the console

Doc Author:
    Willem van der Schans, Trelent AI
"""
    PopupWrapped(
        f"ERROR @ {textString} \n"
        f"Log folder will be opened upon program exit",
        windowType="FatalErrorLarge")
