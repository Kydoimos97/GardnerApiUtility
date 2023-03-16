import threading
import pandas as pd
import requests
from bs4 import *
from Functions.DataFunc.FileSaver import FileSaver
from Functions.Gui.PopupWrapped import PopupWrapped


class realtorCom:

    def __init__(self):
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

        self.__linkGetter()
        self.__showUi()

        PopupWrapped(text=self.uiString, windowType="noticeLarge")

    def __showUi(self):

        uiObj = PopupWrapped(text="Request running", windowType="progress", error=None)

        # Thread get Count to keep gui in mainloop
        threadGui = threading.Thread(target=self.__dataUpdater,
                                     daemon=False)
        threadGui.start()

        while threadGui.is_alive():
            uiObj.textUpdate()
            uiObj.windowPush()
        else:
            uiObj.stopWindow()

    def __linkGetter(self):

        for key, value in self.__idDict.items():
            for row in self.__page_html.find_all("div", {"class": "monthly"}):
                try:
                    for nestedRow in row.find_all("a"):
                        if "History" in str(nestedRow.get("href")) and key in str(nestedRow.get("href")):
                            self.__idDict[key] = {"id": value, "link": nestedRow.get("href")}
                except Exception as e:
                    # DEBUG
                    print(e)
                    pass

    def __dataUpdater(self):

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
