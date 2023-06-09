import datetime
import threading
import time

import pandas as pd
import requests

from API_Calls.Functions.DataFunc.FileSaver import FileSaver
from API_Calls.Functions.DataFunc.Settings import settings
from API_Calls.Functions.ErrorFunc.RESTError import RESTError
from API_Calls.Functions.Gui.BatchGui import confirmDialog
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped


class CFBP:

    def __init__(self, state_arg=None, year_arg=None):
        """
    The __init__ function is called when the class is instantiated.
    Its job is to initialize the object with some default values, and do any other setup that might be necessary.
    The __init__ function can take arguments, but it doesn't have to.

    Args:
        self: Represent the instance of the class
        state_arg: Set the state_arg attribute of the class
        year_arg: Set the year of data to be retrieved

    Returns:
        A popupwrapped object

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.state_arg = state_arg
        self.year_arg = year_arg
        self.uiString = None
        self.link = None

        eventReturn = confirmDialog()
        if eventReturn == "Continue":
            startTime = datetime.datetime.now().replace(microsecond=0)
            self.__showUi()
            print(
                f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | API Link = {self.link}")
            F = FileSaver("cfbp", pd.read_csv(self.link, low_memory=False))
            print(
                f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Data retrieved with in {time.strftime('%H:%M:%S', time.gmtime((datetime.datetime.now().replace(microsecond=0) - startTime).total_seconds()))}")

            self.uiString = (
                f"ffiec.cfpb.gov (Mortgage API) request Completed \n {self.year_arg} data retrieved \n Data Saved at {F.getPath()}")

            PopupWrapped(text=self.uiString, windowType="noticeLarge")
        else:
            print(
                f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | User Canceled Request")
            pass

    def __showUi(self):

        """
    The __showUi function is a function that creates a progress bar window.
    The __showUi function takes class variables and returns a windowobj.


    Args:
        self: Represent the instance of the class

    Returns:
        The uiobj variable

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        uiObj = PopupWrapped(text="Cenus Request running", windowType="progress", error=None)

        threadGui = threading.Thread(target=self.__dataGetter,
                                     daemon=False)
        threadGui.start()

        while threadGui.is_alive():
            uiObj.textUpdate()
            uiObj.windowPush()
        else:
            uiObj.stopWindow()

    def __dataGetter(self):
        """
    The __dataGetter function is a private function that gets the data from the CFPB API.
    It takes no arguments, but uses self.state_arg and self.year_arg to create a URL for the API call.

    Args:
        self: Represent the instance of the class

    Returns:
        A response object

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        arg_dict_bu = locals()

        link = settings.settingCFBPLink

        if self.state_arg is None:
            self.state_arg = "UT"
        else:
            pass

        if self.year_arg is None:
            self.year_arg = str(datetime.date.today().year - 1)
        else:
            pass

        passFlag = False

        while not passFlag:

            self.link = link + f"states={self.state_arg}" + f"&years={self.year_arg}"

            response = requests.get(self.link)

            if response.status_code == 400:
                self.year_arg = int(self.year_arg) - 1

            else:
                passFlag = True

        RESTError(response)
        raise SystemExit(0)
