#  Copyright (C) 2022-2023 - Willem van der Schans - All Rights Reserved.
#
#  THE CONTENTS OF THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL.
#  UNAUTHORIZED COPYING, TRANSFERRING OR REPRODUCTION OF THE CONTENTS OF THIS PROJECT, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
#  The receipt or possession of the source code and/or any parts thereof does not convey or imply any right to use them
#  for any purpose other than the purpose for which they were provided to you.
#
#  The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to
#  the warranties of merchantability, fitness for a particular purpose and non infringement.
#  In no event shall the authors or copyright holders be liable for any claim, damages or other liability,
#  whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software
#  or the use or other dealings in the software.
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#
#  THE CONTENTS OF THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL.
#  UNAUTHORIZED COPYING, TRANSFERRING OR REPRODUCTION OF THE CONTENTS OF THIS PROJECT, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
#  The receipt or possession of the source code and/or any parts thereof does not convey or imply any right to use them
#  for any purpose other than the purpose for which they were provided to you.
#
#
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
from API_Calls.Functions.ErrorFunc.Logger import logger
import subprocess


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

        # Setup Logging
        logger()

        # Call UI
        self.__ShowGui(self.__CreateFrame(), "Data Tool")

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
                                          "The program will not work until such a folder is made",
                                     windowType="errorLarge")

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

        line6 = [[sg.Push(), sg.Button("Realtor.Com", size=(20, None)), sg.Push(), sg.Button("Census", size=(20, None)),
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
