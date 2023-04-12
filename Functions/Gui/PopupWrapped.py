#  Copyright (C) 2022-2023 - Willem van der Schans - All Rights Reserved.
#
#  2023 - Permission to utilize, edit, copy and maintain and source code related to this project within the project's scope is granted to the Kem C. Gardner Policy institute situated in Salt Lake City, Utah into perpetuity.
#
#  THE CONTENTS OF THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL.
#  UNAUTHORIZED COPYING, TRANSFERRING OR REPRODUCTION OF THE CONTENTS OF THIS PROJECT, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
#
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
import os
import time
from pathlib import Path

import PySimpleGUI as sg

from API_Calls.Functions.Gui.ImageLoader import ImageLoader


class PopupWrapped():

    def __init__(self, text="", windowType="notice", error=None):
        """
    The __init__ function is the first function that gets called when an object of this class is created.
    It sets up all the variables and creates a window for us to use.
    Args:
        self: Represent the instance of the class
        text: Set the text of the window
        windowType: Determine what type of window to create
        error: Display the error message in the window
    Returns:
        Nothing
    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__text = text
        self.__type = windowType
        self.__error = error
        self.__layout = []
        self.__windowObj = None
        self.__thread = None
        self.__counter = 0

        self.__createWindow()

    def __createLayout(self):
        """
    The __createLayout function is used to create the layout of the window.
    The function takes class variables and returns a window layout.
    It uses a series of if statements to determine what type of window it is, then creates a layout based on that information.
    Args:
        self: Refer to the current instance of a class
    Returns:
        A list of lists
    Doc Author:
        Willem van der Schans, Trelent AI
    """
        sg.theme('Default1')
        __Line1 = None
        __Line2 = None

        if self.__type == "notice":
            __Line1 = [sg.Push(),
                       sg.Text(u'\u2713', font=("Helvetica", 20, "bold"), justification="center"),
                       sg.Text(self.__text, justification="center", key="-textField-"), sg.Push()]
            __Line2 = [sg.Push(), sg.Ok(focus=True, size=(10, 1)), sg.Push()]
        elif self.__type == "noticeLarge":
            __Line1 = [sg.Push(),
                       sg.Text(u'\u2713', font=("Helvetica", 20, "bold"), justification="center"),
                       sg.Text(self.__text, justification="center", key="-textField-"), sg.Push()]
            __Line2 = [sg.Push(), sg.Ok(focus=True, size=(10, 1)), sg.Push()]
        elif self.__type == "errorLarge":
            __Line1 = [sg.Push(),
                       sg.Text(u'\u274C', font=("Helvetica", 20, "bold"), justification="center"),
                       sg.Text(self.__text, justification="center", key="-textField-"), sg.Push()]
            __Line2 = [sg.Push(), sg.Ok(focus=True, size=(10, 1)), sg.Push()]
        elif self.__type == "FatalErrorLarge":
            __Line1 = [sg.Push(),
                       sg.Text(u'\u274C', font=("Helvetica", 20, "bold"), justification="center"),
                       sg.Text(self.__text, justification="left", key="-textField-"), sg.Push()]
            __Line2 = [sg.Push(), sg.Ok(focus=True, size=(10, 1)), sg.Push()]
        elif self.__type == "error":
            __Line1 = [sg.Push(),
                       sg.Text(u'\u274C', font=("Helvetica", 20, "bold"), justification="center"),
                       sg.Text(f"{self.__text}: {self.__error}", justification="center", key="-textField-"),
                       sg.Push()]
            __Line2 = [sg.Push(), sg.Ok(focus=True, size=(10, 1)), sg.Push()]
        elif self.__type == "progress":
            __Line1 = [sg.Push(),
                       sg.Text(self.__text, justification="center", key="-textField-"), sg.Push()]

        if self.__type == "progress":
            self.__layout = [__Line1, ]
        else:
            self.__layout = [__Line1, __Line2]

    def __createWindow(self):
        """
    The __createWindow function is used to create the window object that will be displayed.
    The function takes class variables and a window object. The function first calls __createLayout, which creates the layout for the window based on what type of message it is (error, notice, progress). Then it uses PySimpleGUI's Window class to create a new window with that layout and some other parameters such as title and icon. If this is not a progress bar or permanent message then we start a timer loop that waits until either 100 iterations have passed or an event has been triggered (such as clicking &quot;Ok&quot; or closing the window). Once one of these events occurs
    Args:
        self: Reference the instance of the class
    Returns:
        A window object
    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__createLayout()

        if self.__type == "progress":
            self.__windowObj = sg.Window(title=self.__type, layout=self.__layout, finalize=True,
                                         modal=True,
                                         keep_on_top=True,
                                         disable_close=False,
                                         icon=ImageLoader("taskbar_icon.ico"),
                                         size=(290, 50))
        elif self.__type == "noticeLarge":
            self.__windowObj = sg.Window(title="Notice", layout=self.__layout, finalize=True,
                                         modal=True,
                                         keep_on_top=True,
                                         disable_close=False,
                                         icon=ImageLoader("taskbar_icon.ico"))
        elif self.__type == "errorLarge":
            self.__windowObj = sg.Window(title="Error", layout=self.__layout, finalize=True,
                                         modal=True,
                                         keep_on_top=True,
                                         disable_close=False,
                                         icon=ImageLoader("taskbar_icon.ico"))
        elif self.__type == "FatalErrorLarge":
            self.__windowObj = sg.Window(title="Fatal Error", layout=self.__layout, finalize=True,
                                         modal=True,
                                         keep_on_top=True,
                                         disable_close=False,
                                         icon=ImageLoader("taskbar_icon.ico"))
        else:
            self.__windowObj = sg.Window(title=self.__type, layout=self.__layout, finalize=True,
                                         modal=True,
                                         keep_on_top=True,
                                         disable_close=False,
                                         icon=ImageLoader("taskbar_icon.ico"),
                                         size=(290, 80))

        if self.__type != "progress" or self.__type.startswith("perm"):
            timer = 0
            while timer < 100:
                event, values = self.__windowObj.read()
                if event == "Ok" or event == sg.WIN_CLOSED:
                    break

                time.sleep(0.1)

            if self.__type == "FatalErrorLarge":
                try:
                    os.system(
                        f"start {Path(os.path.expandvars(r'%APPDATA%')).joinpath('GardnerUtil').joinpath('Logs')}")
                except Exception as e:
                    print(
                        f"PopupWrapped.py | Error = {e} | Log Folder not found please search manually for %APPDATA%\Roaming\GardnerUtil\Logs\n")

            self.__windowObj.close()

    def stopWindow(self):
        """
    The stopWindow function is used to close the window object that was created in the startWindow function.
    This is done by calling the close() method on self.__windowObj, which will cause it to be destroyed.
    Args:
        self: Represent the instance of the class
    Returns:
        The window object
    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__windowObj.close()

    def textUpdate(self, sleep=0.5):
        """
    The textUpdate function is a function that updates the text in the text field.
    It does this by adding dots to the end of it, and then removing them. This creates
    a loading effect for when something is being processed.
    Args:
        self: Refer to the object itself
        sleep: Control the speed of the text update
    Returns:
        A string that is the current text of the text field
    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__counter += 1
        if self.__counter == 4:
            self.__counter = 1
        newString = ""
        if self.__type == "notice":
            pass
        elif self.__type == "error":
            pass
        elif self.__type == "progress":
            newString = f"{self.__text}{'.' * self.__counter}"
        self.__windowObj.write_event_value('update-textField-', newString)

        time.sleep(sleep)

    def windowPush(self):

        """
    The windowPush function is used to update the values of a window object.
        The function takes in an event and values from the window object, then checks if the event starts with 'update'.
        If it does, it will take everything after 'update' as a key for updating that specific value.
        It will then update that value using its key and refresh the window.
    Args:
        self: Reference the object that is calling the function
    Returns:
        A tuple containing the event and values
    Doc Author:
        Willem van der Schans, Trelent AI
    """
        event, values = self.__windowObj.read()

        if event.startswith('update'):
            __key_to_update = event[len('update'):]
            self.__windowObj[__key_to_update].update(values[event])
            self.__windowObj.refresh()
