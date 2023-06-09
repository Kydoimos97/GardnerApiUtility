#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import ctypes
import datetime
import json
import os
from pathlib import Path

import PySimpleGUI as sg
from cryptography.fernet import Fernet

from API_Calls.Functions.ErrorFunc.RESTError import RESTError
from API_Calls.Functions.Gui.ImageLoader import ImageLoader
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped


class AuthUtil:

    def __init__(self):

        """
    The __init__ function is called when the class is instantiated.
    It sets up the initial state of the object, which in this case means that it creates a new window and displays it on screen.

    Args:
        self: Represent the instance of the class

    Returns:
        None

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.StandardStatus = None
        self.ListedOrModified = None
        self.file_name = None
        self.append_file = None
        self.keyPath = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Security'))
        self.filePath = Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData").joinpath("Security")
        self.k = None
        self.keyFlag = True
        self.jsonDict = {}
        self.passFlagUre = False
        self.passFlagCm = False
        self.outcomeText = "Please input the plain text keys in the input boxes above \n " \
                           "Submitting will overwrite any old values in an unrecoverable manner."

        if os.path.exists(self.filePath):
            pass
        else:
            if os.path.exists(Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData")):
                os.mkdir(self.filePath)
            else:
                os.mkdir(Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData"))
                os.mkdir(self.filePath)

        if os.path.exists(self.keyPath):
            pass
        else:
            if os.path.exists(Path(os.path.expandvars(r'%APPDATA%\GardnerUtil'))):
                os.mkdir(self.keyPath)
            else:
                os.mkdir(Path(os.path.expandvars(r'%APPDATA%\GardnerUtil')))
                os.mkdir(self.keyPath)

        if os.path.isfile(self.keyPath.joinpath("3v45wfvw45wvc4f35.av3ra3rvavcr3w")):
            try:
                f = open(self.keyPath.joinpath("3v45wfvw45wvc4f35.av3ra3rvavcr3w"), "rb")
                self.k = f.readline()
                f.close()
            except Exception as e:
                print(e)
                RESTError(402)
                raise SystemExit(402)
        else:
            self.k = Fernet.generate_key()
            f = open(self.keyPath.joinpath("3v45wfvw45wvc4f35.av3ra3rvavcr3w"), "wb")
            f.write(self.k)
            f.close()

            try:
                os.remove(self.filePath.joinpath("auth.json"))
            except Exception as e:
                # Logging
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Authutil.py | Error = {e} | Error in removing auth.json file - This can be due to the file not existing. Continuing...")
                pass

            f = open(self.filePath.joinpath("auth.json"), "wb")
            f.close()
            self.keyFlag = False

        self.__ShowGui(self.__CreateFrame(), "Authenticator Utility")

        try:
            ctypes.windll.kernel32.SetFileAttributesW(self.keyPath.joinpath("3v45wfvw45wvc4f35.av3ra3rvavcr3w"), 2)
        except Exception as e:
            # Logging
            print(
                f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Authutil.py |Error = {e} | Error when setting the key file as hidden. This is either a Permission error or Input Error. Continuing...")
            pass

    def __SetValues(self, values):

        """
    The __SetValues function is called when the user clicks on the &quot;OK&quot; button in the window.
    It takes a dictionary of values as an argument, and then uses those values to update
    the auth.json file with new keys for both Utah Real Estate and Construction Monitor.

    Args:
        self: Make the function a method of the class
        values: Store the values that are entered into the form

    Returns:
        A dictionary of the values entered by the user

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        ureCurrent = None
        cmCurrent = None
        keyFile = None
        self.popupFlag = False

        fernet = Fernet(self.k)

        try:
            f = open(self.filePath.joinpath("auth.json"), "r")
            keyFile = json.load(f)
            fileFlag = True
        except:
            fileFlag = False

        # Try initial decoding, if fails pass and write new keys and files
        if fileFlag:
            try:
                ureCurrent = fernet.decrypt(keyFile["ure"]['auth'].decode())
            except Exception as e:
                # Logging
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Authutil.py |Error = {e} | Error decoding Utah Real Estate Key. Continuing but this should be resolved if URE functionality will be accessed")
                ureCurrent = None

            try:
                cmCurrent = fernet.decrypt(keyFile["cm"]['auth'].decode())
            except Exception as e:
                # Logging
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Authutil.py |Error = {e} | Error decoding Construction Monitor Key. Continuing but this should be resolved if CM functionality will be accessed")
                cmCurrent = None

        if values["-ureAuth-"] != "":
            self.jsonDict.update(
                {"ure": {"parameter": "Authorization", "auth": fernet.encrypt(values["-ureAuth-"].encode()).decode()}})
            self.passFlagUre = True
        elif ureCurrent is not None:
            self.jsonDict.update(
                {"ure": {"parameter": "Authorization", "auth": fernet.encrypt(ureCurrent.encode()).decode()}})
            self.passFlagUre = True
        else:
            pass

        if values["-cmAuth-"] != "":
            if values["-cmAuth-"].startswith("Basic"):
                self.jsonDict.update(
                    {"cm": {"parameter": "Authorization",
                            "auth": fernet.encrypt(values["-cmAuth-"].encode()).decode()}})
                self.passFlagCm = True
            else:
                PopupWrapped("Please make sure you provide a HTTP Basic Auth key for construction Monitor",
                             windowType="AuthError")
                self.popupFlag = True
                pass
        elif ureCurrent is not None:
            self.jsonDict.update(
                {"cm": {"parameter": "Authorization", "auth": fernet.encrypt(cmCurrent.encode()).decode()}})
            self.passFlagUre = True
        else:
            pass

        if not self.passFlagUre and not self.passFlagCm:
            PopupWrapped("Please make sure you provide keys for both Utah Real estate and Construction Monitor",
                         windowType="errorLarge")
        if self.passFlagCm and not self.passFlagUre:
            PopupWrapped("Please make sure you provide a key for Utah Real estate", windowType="errorLarge")
        if not self.passFlagCm and self.passFlagUre and not self.popupFlag:
            PopupWrapped("Please make sure you provide a key for Construction Monitor", windowType="errorLarge")
        if self.popupFlag:
            pass
        else:
            jsonOut = json.dumps(self.jsonDict, indent=4)
            f = open(self.filePath.joinpath("auth.json"), "w")
            f.write(jsonOut)

    def __ShowGui(self, layout, text):

        """
    The __ShowGui function is a helper function that displays the GUI to the user.
    It takes in two arguments: layout and text. The layout argument is a list of lists,
    which contains all the elements that will be displayed on screen. The text argument
    is simply what will be displayed at the top of the window.

    Args:
        self: Represent the instance of the class
        layout: Pass the layout of the gui to be displayed
        text: Set the title of the window

    Returns:
        A window object
    """
        window = sg.Window(text, layout, grab_anywhere=False, return_keyboard_events=True,
                           finalize=True,
                           icon=ImageLoader("taskbar_icon.ico"))

        while not self.passFlagUre or not self.passFlagCm:
            event, values = window.read()

            if event == "Submit":
                try:
                    self.__SetValues(values)
                except Exception as e:
                    print(e)
                    RESTError(993)
                finally:
                    pass
            elif event == sg.WIN_CLOSED or event == "Quit":

                break
            else:
                pass

        window.close()

    def __CreateFrame(self):
        """
    The __CreateFrame function creates the GUI layout for the Authentication Utility.
    It is called by __init__ and returns a list of lists that contains all the elements
    that will be displayed in the window.

    Args:
        self: Access the class attributes and methods

    Returns:
        A list of lists

    Doc Author:
        Trelent
    """
        sg.theme('Default1')

        line00 = [sg.HSeparator()]

        line0 = [sg.Image(ImageLoader("logo.png")),
                 sg.Push(),
                 sg.Text("Authentication Utility", font=("Helvetica", 12, "bold"), justification="center"),
                 sg.Push(),
                 sg.Push()]

        line1 = [sg.HSeparator()]

        line2 = [sg.Push(),
                 sg.Text("Utah Real Estate API Key: ", justification="center"),
                 sg.Push()]

        line3 = [sg.Push(),
                 sg.Input(default_text="123", key="-ureAuth-", disabled=False,
                          size=(40, 1)),
                 sg.Push()]

        line4 = [sg.HSeparator()]

        line5 = [sg.Push(),
                 sg.Text("Construction Monitor HTTP BASIC Key: ", justification="center"),
                 sg.Push()]

        line6 = [sg.Push(),
                 sg.Input(default_text="Basic 123", key="-cmAuth-", disabled=False,
                          size=(40, 1)),
                 sg.Push()]

        line7 = [sg.HSeparator()]

        line8 = [sg.Push(),
                 sg.Text(self.outcomeText, justification="center"),
                 sg.Push()]

        line9 = [sg.HSeparator()]

        line10 = [sg.Push(), sg.Submit(focus=True), sg.Quit(), sg.Push()]

        layout = [line00, line0, line1, line2, line3, line4, line5, line6, line7, line8, line9, line10]

        return layout
