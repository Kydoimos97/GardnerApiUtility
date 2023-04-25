#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import datetime
import os
from pathlib import Path

import PySimpleGUI as sg

from API_Calls.Functions.DataFunc.AuthUtil import AuthUtil
from API_Calls.Functions.DataFunc.versionChecker import versionChecker
from API_Calls.Functions.ErrorFunc.Logger import logger
from API_Calls.Functions.Gui.ImageLoader import ImageLoader
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped
from API_Calls.Sources.CFBP.Core import CFBP
from API_Calls.Sources.ConstructionMonitor.Core import ConstructionMonitorInit, \
    ConstructionMonitorMain
from API_Calls.Sources.Realtor.Core import realtorCom
from API_Calls.Sources.UtahRealEstate.Core import UtahRealEstateMain, UtahRealEstateInit


class initializer:

    def __init__(self):

        """
    The __init__ function is called when the class is instantiated.
    It sets up the logging, calls the __ShowGui function to create and display
    the GUI, and then calls __CreateFrame to create a frame for displaying widgets.


    Args:
        self: Represent the instance of the class

    Returns:
        Nothing

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.classObj = None

        logger()

        print("\n\n-------------Initiate Program---------------------\n\n")

        self.__ShowGui(self.__CreateFrame(), "Data Tool")

        print("\n\n-------------Closing Program---------------------\n\n")

    def __ShowGui(self, layout, text):

        """
    The __ShowGui function is the main function that displays the GUI.
    It takes two arguments: layout and text. Layout is a list of lists, each containing a tuple with three elements:
        1) The type of element to be displayed (e.g., &quot;Text&quot;, &quot;InputText&quot;, etc.)
        2) A dictionary containing any additional parameters for that element (e.g., size, default value, etc.)
        3) An optional key name for the element (used in event handling). If no key name is provided then one will be generated automatically by PySimpleGUIQt based on its position in the layout list

    Args:
        self: Represent the instance of the class
        layout: Pass the layout of the window to be created
        text: Set the title of the window

    Returns:
        A window object

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        versionChecker()

        window = sg.Window(text, layout, grab_anywhere=False, return_keyboard_events=True,
                           finalize=True,
                           icon=ImageLoader("taskbar_icon.ico"))

        while True:
            event, values = window.read()

            if event == "Construction Monitor":
                print(
                    f"\n{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Initiating Construction Monitor API Call-----------------")
                ConstructionMonitorMain(ConstructionMonitorInit())
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Closing Construction Monitor API Call---------------------\n")
            elif event == "Utah Real Estate":
                print(
                    f"\n{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Initiating Utah Real Estate API Call-----------------")
                UtahRealEstateMain(UtahRealEstateInit())
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Closing Utah Real Estate API Call---------------------\n")
            elif event == "Realtor.Com":
                print(
                    f"\n{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Initiating Realtor.com API Call-----------------")
                realtorCom()
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Closing Realtor.com API Call---------------------\n")
            elif event == "CFPB Mortgage":
                print(
                    f"\n{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Initiating ffiec.cfpb API Call-----------------")
                CFBP()
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Closing ffiec.cfpb API Call---------------------\n")
            elif event == "Authorization Utility":
                print(
                    f"\n{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Initiating Authorization Utility-----------------")
                AuthUtil()
                print(
                    f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Closing Authorization Utility---------------------\n")
            elif event == "Open Data Folder":
                print(
                    f"\n{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | -------------Data Folder Opened-----------------")
                try:
                    os.system(f"start {Path(os.path.expanduser('~/Documents')).joinpath('GardnerUtilData')}")
                except:
                    try:
                        os.system(f"start {Path(os.path.expanduser('~/Documents'))}")
                    except Exception as e:
                        print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Initializer.py | Error = {e} | Documents folder not found")
                        PopupWrapped(
                            text="Documents folder not found. Please create a Windows recognized documents folder",
                            windowType="errorLarge")

            elif event in ('Exit', None):
                try:
                    break
                except Exception as e:
                    print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Initializer.py | Error = {e} | Error on program exit, for logging purposes only.")
                    break
            elif event == sg.WIN_CLOSED or event == "Quit":
                break

        window.close()

    def __CreateFrame(self):

        """
    The __CreateFrame function is a helper function that creates the layout for the main window.
    It returns a list of lists, which is then passed to sg.Window() as its layout parameter.

    Args:
        self: Represent the instance of the class

    Returns:
        A list of lists, which is then passed to the sg

    Doc Author:
        Willem van der Schans, Trelent AI
    """
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

        line5 = [[sg.Push(), sg.Button("Construction Monitor", size=(20, None)), sg.Push(),
                  sg.Button("Utah Real Estate", size=(20, None)), sg.Push()]]

        line6 = [[sg.Push(), sg.Button("Realtor.Com", size=(20, None)), sg.Push(),
                  sg.Button("CFPB Mortgage", size=(20, None)),
                  sg.Push()]]

        line8 = [sg.HSeparator()]

        line9 = [sg.Push(),
                 sg.Text("Utilities", font=("Helvetica", 10, "bold"), justification="center"),
                 sg.Push()]

        line10 = [[sg.Push(), sg.Button("Authorization Utility", size=(20, None)),
                   sg.Button("Open Data Folder", size=(20, None)), sg.Push()]]

        line11 = [sg.HSeparator()]

        layout = [line0, line1, line3, line4, line5, line6, line8, line9, line10, line11]

        return layout
