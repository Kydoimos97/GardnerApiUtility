import copy
import datetime
import json
import os
import threading
import time
from datetime import date, timedelta
from pathlib import Path

import PySimpleGUI as sg
import requests
from cryptography.fernet import Fernet

from API_Calls.Functions.DataFunc.AuthUtil import AuthUtil
from API_Calls.Functions.DataFunc.BatchProcessing import BatchCalculator
from API_Calls.Functions.DataFunc.FileSaver import FileSaver
from API_Calls.Functions.ErrorFunc.RESTError import RESTError
from API_Calls.Functions.Gui.BatchGui import BatchInputGui
from API_Calls.Functions.Gui.BatchProgressGUI import BatchProgressGUI
from API_Calls.Functions.Gui.ImageLoader import ImageLoader
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped


class ConstructionMonitorInit:

    def __init__(self):

        """
    The __init__ function is called when the class is instantiated.
    It sets up the variables that will be used by other functions in this class.


    Args:
        self: Represent the instance of the class

    Returns:
        None

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.size = None
        self.SourceInclude = None
        self.dateStart = None
        self.dateEnd = None
        self.rest_domain = None
        self.auth_key = None
        self.ui_flag = None
        self.append_file = None

        passFlag = False

        while not passFlag:
            if os.path.isfile(Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Security')).joinpath(
                    "3v45wfvw45wvc4f35.av3ra3rvavcr3w")) and os.path.isfile(
                Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData").joinpath(
                    "Security").joinpath("auth.json")):
                try:
                    f = open(Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Security')).joinpath(
                        "3v45wfvw45wvc4f35.av3ra3rvavcr3w"), "rb")
                    key = f.readline()
                    f.close()
                    f = open(Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData").joinpath(
                        "Security").joinpath("auth.json"), "rb")
                    authDict = json.load(f)
                    fernet = Fernet(key)
                    self.auth_key = fernet.decrypt(authDict["cm"]["auth"]).decode()
                    passFlag = True
                except Exception as e:
                    print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | ConstructionMonitor/Core.py | Error = {e} | Auth.json not found opening AuthUtil")
                    AuthUtil()
            else:
                AuthUtil()

        self.__ShowGui(self.__CreateFrame(), "Construction Monitor Utility")

    def __ShowGui(self, layout, text):

        """
    The __ShowGui function is the main function that creates and displays the GUI.
    It takes in a layout, which is a list of lists containing all the elements to be displayed on screen.
    The text parameter specifies what title should appear at the top of the window.

    Args:
        self: Refer to the current instance of a class
        layout: Determine what the gui will look like
        text: Set the title of the window

    Returns:
        A dictionary of values

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        window = sg.Window(text, layout, grab_anywhere=False, return_keyboard_events=True,
                           finalize=True,
                           icon=ImageLoader("taskbar_icon.ico"))

        while True:
            event, values = window.read()

            if event == "Submit":
                try:
                    self.__SetValues(values)
                    break
                except Exception as e:
                    print(e)
                    RESTError(993)
                    raise SystemExit(933)
            elif event == sg.WIN_CLOSED or event == "Quit":
                break

        window.close()

    @staticmethod
    def __CreateFrame():

        """
    The __CreateFrame function creates the GUI layout for the application.
        The function returns a list of lists that contains all the elements to be displayed in the GUI window.
        This is done by creating each line as a list and then appending it to another list which will contain all lines.

    Args:

    Returns:
        The layout for the gui

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        sg.theme('Default1')

        line00 = [sg.HSeparator()]

        line0 = [sg.Image(ImageLoader("logo.png")),
                 sg.Push(),
                 sg.Text("Construction Monitor Utility", font=("Helvetica", 12, "bold"), justification="center"),
                 sg.Push(),
                 sg.Push()]

        line1 = [sg.HSeparator()]

        line3 = [sg.Text("Start Date : ", size=(15, None), justification="Right"),
                 sg.Input(default_text=(date.today() - timedelta(days=14)).strftime("%Y-%m-%d"), key="-Cal-",
                          size=(20, 1)),
                 sg.CalendarButton("Select Date", format="%Y-%m-%d", key='-start_date-', target="-Cal-")]

        line4 = [sg.Text("End Date : ", size=(15, None), justification="Right"),
                 sg.Input(default_text=date.today().strftime("%Y-%m-%d"), key="-EndCal-",
                          size=(20, 1)),
                 sg.CalendarButton("Select Date", format="%Y-%m-%d", key='-start_date-', target="-EndCal-")]

        line5 = [sg.HSeparator()]

        line6 = [sg.Push(),
                 sg.Text("File Settings", font=("Helvetica", 12, "bold"), justification="center"),
                 sg.Push()]

        line7 = [sg.HSeparator()]

        line8 = [sg.Text("Appending File : ", size=(15, None), justification="Right"),
                 sg.Input(default_text="", key="-AppendingFile-", disabled=True,
                          size=(20, 1)),
                 sg.FileBrowse("Browse File", file_types=[("csv files", "*.csv")], key='-append_file-',
                               target="-AppendingFile-")]

        line9 = [sg.HSeparator()]

        line10 = [sg.Push(), sg.Submit(focus=True), sg.Quit(), sg.Push()]

        layout = [line00, line0, line1, line3, line4, line5, line6, line7, line8, line9, line10]

        return layout

    def __SetValues(self, values):

        """
    The __SetValues function is used to set the values of the variables that are used in the __GetData function.
    The __SetValues function takes a dictionary as an argument, and then sets each variable based on what is passed into
    the dictionary. The keys for this dictionary are defined by the user when they create their own instance of this class.

    Args:
        self: Represent the instance of the class
        values: Pass in the values from the ui

    Returns:
        A dictionary of values

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.size = 1000

        if values["-Cal-"] != "":
            self.dateStart = values["-Cal-"]
        else:
            self.dateStart = (date.today() - timedelta(days=14)).strftime("%Y-%m-%d")

        if values["-EndCal-"] != "":
            self.dateEnd = values["-EndCal-"]
        else:
            self.dateEnd = date.today().strftime("%Y-%m-%d")

        self.rest_domain = "https://api.constructionmonitor.com/v2/powersearch/?"

        self.SourceInclude = None

        if values["-append_file-"] != "":
            self.append_file = str(values["-append_file-"])
        else:
            self.append_file = None

        self.ui_flag = True


class ConstructionMonitorMain:

    def __init__(self, siteClass):

        """
    The __init__ function is the first function that runs when an object of this class is created.
    It sets up all the variables and functions needed for this class to run properly.


    Args:
        self: Represent the instance of the class
        siteClass: Identify the site that is being used

    Returns:
        Nothing

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__siteClass = siteClass
        self.__restDomain = None
        self.__headerDict = None
        self.__columnSelection = None
        self.__appendFile = None

        self.__parameterDict = {}
        self.__search_id = None
        self.__record_val = 0
        self.__batches = 0

        self.__ui_flag = None

        self.dataframe = None

        try:
            self.mainFunc()
        except SystemError as e:
            if "Status Code = 1000 | Catastrophic Error" in str(getattr(e, 'message', repr(e))):
                print(
                    f"ConstructionMonitor/Core.py | Error = {e} | Cooerced SystemError in ConstructionMonitorMain class")
                pass
        except AttributeError as e:
            # This allows for user cancellation of the program using the quit button
            if "'NoneType' object has no attribute 'json'" in str(getattr(e, 'message', repr(e))):
                RESTError(1101)
                print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Error {e}")
                pass
            elif e is not None:
                print(
                    f"ConstructionMonitor/Core.py | Error = {e} | Authentication Error | Please update keys in AuthUtil")
                RESTError(401)
                print(e)
                pass
            else:
                pass
        except Exception as e:
            print(e)
            RESTError(1001)
            raise SystemExit(1001)

    def mainFunc(self):
        """
    The mainFunc function is the main function of this module. It will be called by the GUI or CLI to execute
    the code in this module. The mainFunc function will first create a parameter dictionary using the __ParameterCreator
    method, then it will get a count of all records that match its parameters using the __getCountUI method, and then
    it will calculate how many batches are needed to retrieve all records with those parameters using BatchCalculator.
    After that it asks if you want to continue with retrieving data from Salesforce (if running in GUI mode). Then it shows
    a progress bar for each

    Args:
        self: Refer to the current object

    Returns:
        The dataframe

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__ParameterCreator()

        print(
            f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Param Dict = {self.__parameterDict}")
        print(
            f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Rest Domain = {self.__restDomain}")

        self.__getCountUI()

        self.__batches = BatchCalculator(self.__record_val, self.__parameterDict)

        print(
            f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Batches = {self.__batches} | Rows {self.__record_val}")

        if self.__batches != 0:
            startTime = datetime.datetime.now().replace(microsecond=0)
            eventReturn = BatchInputGui(self.__batches, self.__record_val)
            if eventReturn == "Continue":
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Request for {self.__batches} batches sent to server")
                BatchGuiObject = BatchProgressGUI(RestDomain=self.__restDomain,
                                                  ParameterDict=self.__parameterDict,
                                                  HeaderDict=self.__headerDict,
                                                  ColumnSelection=self.__columnSelection,
                                                  BatchesNum=self.__batches,
                                                  Type="construction_monitor")
                BatchGuiObject.BatchGuiShow()
                self.dataframe = BatchGuiObject.dataframe
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Dataframe retrieved with {self.dataframe.shape[0]} rows and {self.dataframe.shape[1]} columns in {time.strftime('%H:%M:%S', time.gmtime((datetime.datetime.now().replace(microsecond=0) - startTime).total_seconds()))}")
                FileSaver("cm", self.dataframe, self.__appendFile)
            else:
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Request for {self.__batches} batches canceled by user")
        else:
            RESTError(994)
            raise SystemExit(994)

    def __ParameterCreator(self):
        """
    The __ParameterCreator function is used to create the parameter dictionary that will be passed into the
        __Request function. The function takes in a siteClass object and extracts all of its attributes, except for
        those that start with '__' or are callable. It then creates a dictionary from these attributes and stores it as
        self.__parameterDict.

    Args:
        self: Make the function a method of the class

    Returns:
        A dictionary of parameters and a list of non parameter variables

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        __Source_dict = {key: value for key, value in self.__siteClass.__dict__.items() if
                         not key.startswith('__') and not callable(key)}

        self.__restDomain = __Source_dict["rest_domain"]
        __Source_dict.pop("rest_domain")
        self.__headerDict = {"Authorization": __Source_dict["auth_key"]}
        __Source_dict.pop("auth_key")
        self.__columnSelection = __Source_dict["SourceInclude"]
        __Source_dict.pop("SourceInclude")
        self.__ui_flag = __Source_dict["ui_flag"]
        __Source_dict.pop("ui_flag")
        self.__appendFile = __Source_dict["append_file"]
        __Source_dict.pop("append_file")

        temp_dict = copy.copy(__Source_dict)
        for key, value in temp_dict.items():
            if value is None:
                __Source_dict.pop(key)
            else:
                pass

        self.__parameterDict = copy.copy(__Source_dict)

    def __getCount(self):
        """
    The __getCount function is used to get the total number of records that are returned from a query.
    This function is called by the __init__ function and sets the self.__record_val variable with this value.

    Args:
        self: Represent the instance of the class

    Returns:
        The total number of records in the database

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        __count_resp = None

        try:

            __temp_param_dict = copy.copy(self.__parameterDict)

            __count_resp = requests.post(url=self.__restDomain,
                                         headers=self.__headerDict,
                                         json=__temp_param_dict)

        except requests.exceptions.Timeout as e:
            print(e)
            RESTError(790)
            raise SystemExit(790)
        except requests.exceptions.TooManyRedirects as e:
            print(e)
            RESTError(791)
            raise SystemExit(791)
        except requests.exceptions.MissingSchema as e:
            print(e)
            RESTError(1101)
        except requests.exceptions.RequestException as e:
            print(e)
            RESTError(405)
            raise SystemExit(405)

        __count_resp = __count_resp.json()

        self.__record_val = __count_resp["hits"]["total"]["value"]

        del __count_resp, __temp_param_dict

    def __getCountUI(self):

        """
    The __getCountUI function is a wrapper for the __getCount function.
    It allows the user to run __getCount in a separate thread, so that they can continue working while it runs.
    The function will display a progress bar and update with text as it progresses through its tasks.

    Args:
        self: Access the class variables and methods

    Returns:
        The count of the number of records in the database

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        if self.__ui_flag:
            uiObj = PopupWrapped(text="Batch request running", windowType="progress", error=None)

            threadGui = threading.Thread(target=self.__getCount,
                                         daemon=False)
            threadGui.start()

            while threadGui.is_alive():
                uiObj.textUpdate()
                uiObj.windowPush()
            else:
                uiObj.stopWindow()

        else:
            self.__getCount()
