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


class UtahRealEstateInit:

    def __init__(self):

        """
    The __init__ function is called when the class is instantiated.
    It sets up the initial state of the object.


    Args:
        self: Represent the instance of the class

    Returns:
        The __createframe function

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.StandardStatus = None
        self.ListedOrModified = None
        self.dateStart = None
        self.dateEnd = None
        self.select = None
        self.file_name = None
        self.append_file = None

        self.__ShowGui(self.__CreateFrame(), "Utah Real Estate")

    def __ShowGui(self, layout, text):

        """
    The __ShowGui function is a helper function that creates the GUI window and displays it to the user.
    It takes in two parameters: layout, which is a list of lists containing all the elements for each row;
    and text, which is a string containing what will be displayed as the title of the window. The __ShowGui
    method then uses these parameters to create an instance of sg.Window with all its attributes set accordingly.

    Args:
        self: Refer to the current class instance
        layout: Pass the layout of the window to be created
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
                    raise SystemExit(993)
            elif event == sg.WIN_CLOSED or event == "Quit":
                break

        window.close()

    @staticmethod
    def __CreateFrame():
        """
    The __CreateFrame function creates the GUI layout for the application.
        The function returns a list of lists that contains all the elements to be displayed in the window.
        Each element is defined by its type and any additional parameters needed to define it.

    Args:

    Returns:
        A list of lists, which is used to create the gui

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        sg.theme('Default1')

        line00 = [sg.HSeparator()]

        line0 = [sg.Image(ImageLoader("logo.png")),
                 sg.Push(),
                 sg.Text("Utah Real Estate Utility", font=("Helvetica", 12, "bold"), justification="center"),
                 sg.Push(),
                 sg.Push()]

        line1 = [sg.HSeparator()]

        line2 = [sg.Text("MLS Status : ", size=(15, None), justification="Right"),
                 sg.DropDown(default_value="Active", values=["Active", "Closed"], key="-status-", size=(31, 1))]

        line3 = [sg.Text("Date Type: ", size=(15, None), justification="Right"),
                 sg.DropDown(default_value="Listing Date", values=["Listing Date", "Modification Date", "Close Date"],
                             key="-type-", size=(31, 1))]

        line4 = [sg.Text("Start Date : ", size=(15, None), justification="Right"),
                 sg.Input(default_text=(date.today() - timedelta(days=14)).strftime("%Y-%m-%d"), key="-DateStart-",
                          disabled=False, size=(20, 1)),
                 sg.CalendarButton("Select Date", format="%Y-%m-%d", key='-start_date-', target="-DateStart-")]

        line5 = [sg.Text("End Date : ", size=(15, None), justification="Right"),
                 sg.Input(default_text=(date.today().strftime("%Y-%m-%d")), key="-DateEnd-", disabled=False,
                          size=(20, 1)),
                 sg.CalendarButton("Select Date", format="%Y-%m-%d", key='-end_date-', target="-DateEnd-")]

        line7 = [sg.HSeparator()]

        line8 = [sg.Push(),
                 sg.Text("File Settings", font=("Helvetica", 12, "bold"), justification="center"),
                 sg.Push()]

        line9 = [sg.HSeparator()]

        line10 = [sg.Text("Appending File : ", size=(15, None), justification="Right"),
                  sg.Input(default_text="", key="-AppendingFile-", disabled=True,
                           size=(20, 1)),
                  sg.FileBrowse("Browse File", file_types=[("csv files", "*.csv")], key='-append_file-',
                                target="-AppendingFile-")]

        line11 = [sg.HSeparator()]

        line12 = [sg.Push(), sg.Submit(focus=True), sg.Quit(), sg.Push()]

        layout = [line00, line0, line1, line2, line3, line4, line5, line7, line8, line9, line10, line11,
                  line12]

        return layout

    def __SetValues(self, values):

        """
    The __SetValues function is used to set the values of the variables that are used in the
       __GetData function. The values are passed from a dictionary called 'values' which is created
       by parsing through an XML file using ElementTree. This function also sets default values for
       some of these variables if they were not specified in the XML file.

    Args:
        self: Represent the instance of the class
        values: Pass the values from the gui to this function

    Returns:
        A dictionary with the following keys:

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.StandardStatus = values["-status-"]

        self.ListedOrModified = values["-type-"]

        if values["-DateStart-"] != "":
            self.dateStart = values["-DateStart-"]
        else:
            self.dateStart = (date.today() - timedelta(days=14)).strftime("%Y-%m-%d")

        if values["-DateEnd-"] != "":
            self.dateEnd = values["-DateEnd-"]
        else:
            self.dateEnd = (date.today()).strftime("%Y-%m-%d")

        self.select = None

        if values["-append_file-"] != "":
            self.append_file = str(values["-append_file-"])
        else:
            self.append_file = None


class UtahRealEstateMain:

    def __init__(self, siteClass):

        """
    The __init__ function is the first function that runs when an object of this class is created.
    It sets up all the variables and functions needed for this class to work properly.

    Args:
        self: Represent the instance of the class
        siteClass: Determine which site to pull data from

    Returns:
        Nothing

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.dataframe = None
        self.__batches = 0
        self.__siteClass = siteClass
        self.__headerDict = None
        self.__parameterString = ""
        self.__appendFile = None
        self.__dateStart = None
        self.__dateEnd = None
        self.__restDomain = 'https://resoapi.utahrealestate.com/reso/odata/Property?'
        self.keyPath = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Security')).joinpath(
            "3v45wfvw45wvc4f35.av3ra3rvavcr3w")
        self.filePath = Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData").joinpath(
            "Security").joinpath("auth.json")
        self.key = None

        try:
            self.mainFunc()
        except KeyError as e:
            # This allows for user cancellation of the program using the quit button
            if "ListedOrModified" in str(getattr(e, 'message', repr(e))):
                RESTError(1101)
                print(e)
                pass
        except AttributeError as e:
            if e is not None:
                print(
                    f"UtahRealEstate/Core.py | Error = {e} | Authentication Error | Please update keys in AuthUtil")
                RESTError(401)
                pass
            else:
                pass
        except Exception as e:
            print(e)
            RESTError(1001)
            raise SystemExit(1001)

    def mainFunc(self):

        """
    The mainFunc function is the main function of this module. It will be called by the GUI when a user clicks on
    the &quot;Run&quot; button in the GUI. The mainFunc function should contain all of your code for running your program, and it
    should return a dataframe that contains all the data you want to display in your final report.

    Args:
        self: Reference the object itself

    Returns:
        A dataframe

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        passFlag = False

        while not passFlag:
            if os.path.isfile(self.keyPath) and os.path.isfile(self.filePath):
                try:
                    f = open(self.keyPath, "rb")
                    key = f.readline()
                    f.close()
                    f = open(self.filePath, "rb")
                    authDict = json.load(f)
                    fernet = Fernet(key)
                    authkey = fernet.decrypt(authDict["ure"]["auth"]).decode()
                    self.__headerDict = {authDict["ure"]["parameter"]: authkey}
                    passFlag = True
                except Exception as e:
                    print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | UtahRealEstate/Core.py | Error = {e} | Auth.json not found opening AuthUtil")
                    AuthUtil()
            else:
                AuthUtil()


        self.__ParameterCreator()

        self.__getCountUI()

        self.__batches = BatchCalculator(self.__record_val, None)

        if self.__batches != 0:
            startTime = datetime.datetime.now().replace(microsecond=0)
            eventReturn = BatchInputGui(self.__batches, self.__record_val)
            if eventReturn == "Continue":
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Request for {self.__batches} batches sent to server")
                BatchGuiObject = BatchProgressGUI(RestDomain=self.__restDomain,
                                                  ParameterDict=self.__parameterString,
                                                  HeaderDict=self.__headerDict,
                                                  BatchesNum=self.__batches,
                                                  Type="utah_real_estate")
                BatchGuiObject.BatchGuiShow()
                self.dataframe = BatchGuiObject.dataframe
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Dataframe retrieved with {self.dataframe.shape[0]} rows and {self.dataframe.shape[1]} columns in {time.strftime('%H:%M:%S', time.gmtime((datetime.datetime.now().replace(microsecond=0) - startTime).total_seconds()))}")
                FileSaver("ure", self.dataframe, self.__appendFile)
            else:
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Request for {self.__batches} batches canceled by user")
        else:
            RESTError(994)
            raise SystemExit(994)

    def __ParameterCreator(self):
        """
    The __ParameterCreator function is used to create the filter string for the ReST API call.
    The function takes in a siteClass object and extracts all of its parameters into a dictionary.
    It then creates an appropriate filter string based on those parameters.

    Args:
        self: Bind the object to the class

    Returns:
        A string to be used as the parameter in the api call

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        filter_string = ""

        __Source_dict = {key: value for key, value in self.__siteClass.__dict__.items() if
                         not key.startswith('__') and not callable(key)}

        self.__appendFile = __Source_dict["append_file"]
        __Source_dict.pop("append_file")

        temp_dict = copy.copy(__Source_dict)
        for key, value in temp_dict.items():
            if value is None:
                __Source_dict.pop(key)
            else:
                pass

        if __Source_dict["ListedOrModified"] == "Listing Date":
            filter_string = f"$filter=ListingContractDate%20gt%20{__Source_dict['dateStart']}%20and%20ListingContractDate%20le%20{__Source_dict['dateEnd']}"
        elif __Source_dict["ListedOrModified"] == "Modification Date":
            filter_string = f"$filter=ModificationTimestamp%20gt%20{__Source_dict['dateStart']}T:00:00:00Z%20and%20ModificationTimestamp%20le%20{__Source_dict['dateEnd']}T:23:59:59Z"
        elif __Source_dict["ListedOrModified"] == "Close Date":
            filter_string = f"$filter=CloseDate%20gt%20{__Source_dict['dateStart']}%20and%20CloseDate%20le%20{__Source_dict['dateEnd']}"

        filter_string = filter_string + f"%20and%20StandardStatus%20has%20Odata.Models.StandardStatus'{__Source_dict['StandardStatus']}'"

        self.__parameterString = filter_string

    def __getCount(self):
        """
    The __getCount function is used to determine the number of records that will be returned by the query.
    This function is called when a user calls the count() method on a ReST object. The __getCount function uses
    the $count parameter in OData to return only an integer value representing how many records would be returned
    by the query.

    Args:
        self: Represent the instance of the class

    Returns:
        The number of records in the data set

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        __count_resp = None

        try:
            __count_resp = requests.get(f"{self.__restDomain}{self.__parameterString}&$count=true",
                                        headers=self.__headerDict)

            if __count_resp.status_code != 200:
                RESTError(__count_resp)
                raise SystemExit(0)

            self.__record_val = int(__count_resp.json()["@odata.count"])

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

    def __getCountUI(self):

        """
    The __getCountUI function is a wrapper for the __getCount function.
    It creates a progress window and updates it while the __getCount function runs.
    The purpose of this is to keep the GUI responsive while running long processes.

    Args:
        self: Represent the instance of the class

    Returns:
        A popupwrapped object

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        uiObj = PopupWrapped(text="Batch request running", windowType="progress", error=None)

        threadGui = threading.Thread(target=self.__getCount,
                                     daemon=False)
        threadGui.start()

        while threadGui.is_alive():
            uiObj.textUpdate()
            uiObj.windowPush()
        else:
            uiObj.stopWindow()
