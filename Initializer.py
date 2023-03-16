import os
from pathlib import Path

import PySimpleGUI as sg
from API_Calls.Sources.ConstructionMonitor.Core import ConstructionMonitorInit, \
    ConstructionMonitorMain
from API_Calls.Sources.Realtor.Core import realtorCom
from API_Calls.Sources.UtahRealEstate.Core import UtahRealEstateMain, UtahRealEstateInit
from API_Calls.Functions.Gui.ImageLoader import ImageLoader
from Functions.DataFunc.AuthUtil import AuthUtil
from Functions.Gui.PopupWrapped import PopupWrapped
from Sources.CFBP.Core import Cencus
import subprocess


class initializer:

    def __init__(self):
        self.classObj = None

        # Call UI
        self.__ShowGui(self.__CreateFrame(), "Data Tool")

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
            if event == "Construction Monitor":
                ConstructionMonitorMain(ConstructionMonitorInit())
            elif event == "Utah Real Estate":
                UtahRealEstateMain(UtahRealEstateInit())
            elif event == "Realtor.Com":
                realtorCom()
            elif event == "Census":
                Cencus()
            elif event == "Authorization Utility":
                AuthUtil()
            elif event == "Open Data Folder":
                try:
                    os.system(f"start {Path(os.path.expanduser('~/Documents')).joinpath('GardnerUtilData')}")
                except:
                    try:
                        os.system(f"start {Path(os.path.expanduser('~/Documents'))}")
                    except:
                        PopupWrapped(text="You don't have a documents folder!! \n"
                                          "Something is seriously wrong with your file structure \n"
                                          "The program will not work until such a folder is made", windowType="errorLarge")

            elif event in ('Exit', None):
                try:
                    break
                except Exception as e:
                    # DEBUG
                    break

            # etc. # DEBUG
            elif event == sg.WIN_CLOSED or event == "Quit":
                break

        window.close()

    def __CreateFrame(self):
        sg.theme('Default1')

        line0 = [sg.HSeparator()]

        line1 = [sg.Image(ImageLoader("logo.png")),
                 sg.Push(),
                 sg.Text("Gardner Data Utility", font=("Helvetica", 12, "bold"), justification="center"),
                 sg.Push(),
                 sg.Push()]

        line3 = [sg.HSeparator()]

        line4 = [sg.Push(),
                 sg.Text("Api Sources", font=("Helvetica", 10, "bold"), justification="center"),
                 sg.Push()]

        line5 = [[sg.Push(), sg.Button("Construction Monitor", size=(20,None)), sg.Push(), sg.Button("Utah Real Estate", size=(20,None)), sg.Push()]]

        line6 = [[sg.Push(), sg.Button("Realtor.Com", size=(20,None)), sg.Push(), sg.Button("Census", size=(20,None)), sg.Push()]]

        line8 = [sg.HSeparator()]

        line9 = [sg.Push(),
                 sg.Text("Utilities", font=("Helvetica", 10, "bold"), justification="center"),
                 sg.Push()]

        line10 = [[sg.Push(), sg.Button("Authorization Utility", size=(20,None)), sg.Button("Open Data Folder", size=(20,None)), sg.Push()]]

        line11 = [sg.HSeparator()]

        layout = [line0, line1, line3, line4, line5, line6, line8, line9, line10, line11]

        return layout



