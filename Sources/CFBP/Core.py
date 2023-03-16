import threading
from datetime import date
import pandas as pd
import requests

from Functions.DataFunc.FileSaver import FileSaver
from Functions.ErrorFunc.RESTError import RESTError
from Functions.Gui.PopupWrapped import PopupWrapped


class Cencus:

    def __init__(self, state_arg=None, year_arg=None):
        self.state_arg = state_arg
        self.year_arg = year_arg
        self.uiString = None
        self.link = None

        self.__showUi()
        print(self.link)
        F = FileSaver("cfbp", pd.read_csv(self.link, low_memory=False))
        self.uiString = (
            f"ffiec.cfpb.gov (Mortgage API) request Completed \n {self.year_arg} data retrieved \n Data Saved at {F.getPath()}")

        PopupWrapped(text=self.uiString, windowType="noticeLarge")

    def __showUi(self):

        uiObj = PopupWrapped(text="Cenus Request running", windowType="progress", error=None)

        # Thread get Count to keep gui in mainloop
        threadGui = threading.Thread(target=self.__dataGetter,
                                     daemon=False)
        threadGui.start()

        while threadGui.is_alive():
            uiObj.textUpdate()
            uiObj.windowPush()
        else:
            uiObj.stopWindow()

    def __dataGetter(self):
        arg_dict_bu = locals()

        link = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?"

        # Check Input
        if self.state_arg is None:
            self.state_arg = "UT"
        else:
            pass

        if self.year_arg is None:
            self.year_arg = str(date.today().year - 1)
        else:
            pass

        passFlag = False

        while not passFlag:
            # Create Get URL
            self.link = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?" + f"states={self.state_arg}" + f"&years={self.year_arg}"
            # Call URL
            # Get requests need URL modification for filters
            # What do you want to do with this data? Get average
            response = requests.get(self.link)

            if response.status_code == 400:
                self.year_arg = int(self.year_arg) - 1

            else:
                passFlag = True

        # Response Code Handling
        RESTError(response)
