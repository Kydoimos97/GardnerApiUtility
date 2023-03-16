import copy
import json
import os
import threading
from datetime import date, timedelta
from pathlib import Path

import PySimpleGUI as sg
import requests
from cryptography.fernet import Fernet

from API_Calls.Functions.DataFunc.BatchProcessing import BatchCalculator
from API_Calls.Functions.Gui.BatchGui import BatchInputGui
from API_Calls.Functions.Gui.BatchProgressGUI import BatchProgressGUI
from API_Calls.Functions.Gui.ImageLoader import ImageLoader
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped
from Functions.DataFunc.AuthUtil import AuthUtil
from Functions.DataFunc.FileSaver import FileSaver
from Functions.ErrorFunc.RESTError import RESTError


class ConstructionMonitorInit:

    def __init__(self):

        # Class Variables
        self.size = None
        self.SourceInclude = None
        self.dateStart = None
        self.dateEnd = None
        self.rest_domain = None
        self.auth_key = None
        self.ui_flag = None
        self.append_file = None

        # Call UI
        passFlag = False

        # Get Auth Key
        while not passFlag:
            if os.path.isfile(Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Security')).joinpath(
            "3v45wfvw45wvc4f35.av3ra3rvavcr3w")) and os.path.isfile(Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData").joinpath(
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
                except:
                    AuthUtil()
            else:
                AuthUtil()


        self.__ShowGui(self.__CreateFrame(), "Construction Monitor Utility")

    def __ShowGui(self, layout, text):

        # Create Window
        window = sg.Window(text, layout, grab_anywhere=False, return_keyboard_events=True,
                           finalize=True,
                           icon=ImageLoader("taskbar_icon.ico"))

        # Create an event loop
        while True:
            event, values = window.read()
            # End program if user closes window or
            # presses the OK button
            if event == "Submit":
                try:
                    self.__SetValues(values)
                    break
                except Exception as e:
                    # DEBUG
                    break
            elif event == sg.WIN_CLOSED or event == "Quit":
                # raise KeyboardInterrupt("User cancelled the program")
                break

        window.close()

    @staticmethod
    def __CreateFrame():

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

        line5 = [[sg.Text("Column Sub-Selection : ", size=(23, None), justification="Right"),
                  sg.Checkbox(text="", default=True, key="-select_columns-", size=(15, 1)),
                  sg.Push()]]

        line6 = [sg.HSeparator()]

        line7 = [sg.Push(),
                 sg.Text("File Settings", font=("Helvetica", 12, "bold"), justification="center"),
                 sg.Push()]

        line8 = [sg.HSeparator()]

        line9 = [sg.Text("Appending File : ", size=(15, None), justification="Right"),
                  sg.Input(default_text="", key="-AppendingFile-", disabled=True,
                           size=(20, 1)),
                  sg.FileBrowse("Browse File", file_types=[("csv files", "*.csv")], key='-append_file-',
                                target="-AppendingFile-")]

        line10 = [sg.HSeparator()]

        line11 = [sg.Push(), sg.Submit(focus=True), sg.Quit(), sg.Push()]

        layout = [line00, line0, line1, line3, line4, line5, line6, line7, line8, line9, line10, line11]

        return layout

    def __SetValues(self, values):

        # Page-limit
        self.size = 1000

        # start_date
        if values["-Cal-"] != "":
            self.dateStart = values["-Cal-"]
        else:
            self.dateStart = (date.today() - timedelta(days=14)).strftime("%Y-%m-%d")

        # start_date
        if values["-EndCal-"] != "":
            self.dateEnd = values["-EndCal-"]
        else:
            self.dateEnd = date.today().strftime("%Y-%m-%d")

        # Rest Domain
        self.rest_domain = "https://api.constructionmonitor.com/v2/powersearch/?"

        # Column Selection
        if values["-select_columns-"] == "True":
            self.SourceInclude = "state,county,city,description,valuation,sqft,units,permitdate,lastupdated," \
                                 "permitstatus "
        else:
            self.SourceInclude = None

        # appending_file
        if values["-append_file-"] != "":
            self.append_file = str(values["-append_file-"])
        else:
            self.append_file = None

        # UIflag [obsolete flag] TODO: Remove
        self.ui_flag = True


class ConstructionMonitorMain:

    def __init__(self, siteClass):

        # Inherited from Class
        self.__siteClass = siteClass
        self.__restDomain = None
        self.__headerDict = None
        self.__columnSelection = None
        self.__appendFile = None

        # Created In Class
        self.__parameterDict = {}
        self.__search_id = None
        self.__record_val = 0
        self.__batches = 0

        # Read from UI
        self.__ui_flag = None

        # Read from BatchProcessor
        self.dataframe = None

        try:
            self.mainFunc()
        except SystemError as e:
            if "Status Code = 1000 | Catastrophic Error" in str(getattr(e, 'message', repr(e))):
                pass
        except Exception as e:
            raise e

    def mainFunc(self):
        self.__ParameterCreator()

        # Count Request
        self.__getCountUI()
        # Batch Calculator
        self.__batches = BatchCalculator(self.__record_val, self.__parameterDict)
        # Ask to continue
        if self.__ui_flag:
            BatchInputGui(self.__batches)
        # Show Batch Progress
        BatchGuiObject = BatchProgressGUI(RestDomain=self.__restDomain,
                                          ParameterDict=self.__parameterDict,
                                          HeaderDict=self.__headerDict,
                                          ColumnSelection=self.__columnSelection,
                                          BatchesNum=self.__batches,
                                          Type="construction_monitor")
        BatchGuiObject.BatchGuiShow()
        self.dataframe = BatchGuiObject.dataframe
        FileSaver("cm", self.dataframe, self.__appendFile)

    def __ParameterCreator(self):
        __Source_dict = {key: value for key, value in self.__siteClass.__dict__.items() if
                         not key.startswith('__') and not callable(key)}

        # Extract non parameter variables
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

        # Create Parameter Dictionary
        temp_dict = copy.copy(__Source_dict)
        for key, value in temp_dict.items():
            if value is None:
                __Source_dict.pop(key)
            else:
                pass

        self.__parameterDict = copy.copy(__Source_dict)

    # Get the count of number of batches to be run

    def __getCount(self):
        __count_resp = None

        try:
            # Try for count request
            __temp_param_dict = copy.copy(self.__parameterDict)

            __count_resp = requests.post(url=self.__restDomain,
                                         headers=self.__headerDict,
                                         json=__temp_param_dict)

            # Error Handling if not valid
            if __count_resp.status_code != 200:
                RESTError(__count_resp)

        # requests Error Handling
        except requests.exceptions.Timeout:
            RESTError(790)
        except requests.exceptions.TooManyRedirects:
            RESTError(791)
        except requests.exceptions.RequestException:
            RESTError(1000)

        # Get needed Values
        __count_resp = __count_resp.json()

        # Set values
        self.__record_val = __count_resp["hits"]["total"]["value"]

        # Garbage Collection
        del __count_resp, __temp_param_dict

    def __getCountUI(self):

        if self.__ui_flag:
            uiObj = PopupWrapped(text="Batch request running", windowType="progress", error=None)

            # Thread get Count to keep gui in mainloop
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
