import datetime
import threading
import time

import pandas as pd
import requests
from bs4 import *

from API_Calls.Functions.DataFunc.FileSaver import FileSaver
from API_Calls.Functions.ErrorFunc.RESTError import RESTError
from API_Calls.Functions.Gui.BatchGui import confirmDialog
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped


class realtorCom:

    def __init__(self):
        """
    The __init__ function is called when the class is instantiated.
    It sets up the initial state of an object, and it's where you put code that needs to run before anything else in your class.

    Args:
        self: Represent the instance of the class

    Returns:
        A new object

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__page_html = None
        self.__update_date = None
        self.__last_date = None
        self.__idDict = {"State": "C3", "County": "E3", "Zip": "F3"}
        self.__linkDict = {}
        self.dfState = None
        self.dfCounty = None
        self.dfZip = None
        self.uiString = "Files Saved to \n"

        page_html = requests.get("https://www.realtor.com/research/data/").text
        self.__page_html = BeautifulSoup(page_html, "html.parser")

        eventReturn = confirmDialog()
        if eventReturn == "Continue":
            startTime = datetime.datetime.now().replace(microsecond=0)
            self.__linkGetter()
            self.__showUi()
            PopupWrapped(text=self.uiString, windowType="noticeLarge")
            print(
                f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Data retrieved with in {time.strftime('%H:%M:%S', time.gmtime((datetime.datetime.now().replace(microsecond=0) - startTime).total_seconds()))}")
        else:
            print(
                f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | User Canceled Request")
            pass

    def __showUi(self):

        """
    The __showUi function is a helper function that creates and displays the progress window.
    It also starts the dataUpdater thread, which will update the progress bar as it runs.


    Args:
        self: Represent the instance of the class

    Returns:
        A popupwrapped object

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        uiObj = PopupWrapped(text="Request running", windowType="progress", error=None)

        threadGui = threading.Thread(target=self.__dataUpdater,
                                     daemon=False)
        threadGui.start()

        while threadGui.is_alive():
            uiObj.textUpdate()
            uiObj.windowPush()
        else:
            uiObj.stopWindow()

    def __linkGetter(self):

        """
    The __linkGetter function is a private function that takes the idDict dictionary and adds
    a link to each entry in the dictionary. The link is used to access historical data for each
    scope symbol.

    Args:
        self: Refer to the object itself

    Returns:
        A dictionary of all the links to the history pages

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        for key, value in self.__idDict.items():
            for row in self.__page_html.find_all("div", {"class": "monthly"}):
                try:
                    for nestedRow in row.find_all("a"):
                        if "History" in str(nestedRow.get("href")) and key in str(nestedRow.get("href")):
                            self.__idDict[key] = {"id": value, "link": nestedRow.get("href")}
                except Exception as e:
                    print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Realtor/Core.py | Error = {e} | Error while getting document links for realtor.com")
                    RESTError(801)
                    raise SystemExit(801)

    def __dataUpdater(self):

        """
    The __dataUpdater function is a private function that updates the dataframes for each of the three
        types of realtor data. It takes class variables and return the path to the saved file. The function first creates an empty
        dictionary called tempdf, then iterates through each key in self.__idDict (which contains all three ids).
        For each key, it reads in a csv file from the link associated with that id and saves it to tempdf as a pandas
        DataFrame object. Then, depending on which type of realtor data we are dealing with (State/County/Zip), we save


    Args:
        self: Access the attributes and methods of the class

    Returns:
        The path of the saved file

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        for key, value in self.__idDict.items():
            tempdf = pd.read_csv(self.__idDict[key]['link'], low_memory=False)

            if key == "State":
                self.dfState = tempdf
            elif key == "County":
                self.dfCounty = tempdf
            elif key == "Zip":
                self.dfZip = tempdf

            FileSaveObj = FileSaver(f"realtor_{key}", tempdf)
            self.uiString = self.uiString + f"{key} : {FileSaveObj.getPath()} \n"
