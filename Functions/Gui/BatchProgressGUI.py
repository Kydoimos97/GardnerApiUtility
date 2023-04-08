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

import datetime
import threading
import time

import PySimpleGUI as sg

from API_Calls.Functions.DataFunc.BatchProcessing import BatchProcessorConstructionMonitor, BatchProcessorUtahRealEstate
from API_Calls.Functions.Gui.DataTransfer import DataTransfer
from API_Calls.Functions.Gui.ImageLoader import ImageLoader
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped

counter = 1


class BatchProgressGUI:

    def __init__(self, BatchesNum, RestDomain, ParameterDict, HeaderDict, Type, ColumnSelection=None):

        """
    The __init__ function is the first function that gets called when an object of this class is created.
    It initializes all the variables and sets up a layout for the GUI. It also creates a window to display
    the dataframe in.

    Args:
        self: Represent the instance of the class
        BatchesNum: Determine the number of batches that will be created
        RestDomain: Specify the domain of the rest api
        ParameterDict: Pass the parameters of the request to the class
        HeaderDict: Store the headers of the dataframe
        Type: Determine the type of dataframe that is being created
        ColumnSelection: Select the columns to be displayed in the gui

    Returns:
        Nothing

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__parameterDict = ParameterDict
        self.__restDomain = RestDomain
        self.__headerDict = HeaderDict
        self.__columnSelection = ColumnSelection
        self.__type = Type
        self.dataframe = None

        self.__layout = None
        self.__batches = BatchesNum
        self.__window = None
        self.__batch_counter = 0

    def BatchGuiShow(self):
        """
    The BatchGuiShow function is called by the BatchGui function. It creates a progress bar layout and then calls the createGui function to create a GUI for batch processing.

    Args:
        self: Represent the instance of the class

    Returns:
        The __type of the batchgui class

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.CreateProgressLayout()
        self.createGui(self.__type)

    def CreateProgressLayout(self):

        """
    The CreateProgressLayout function creates the layout for the progress window.
        The function takes in self as a parameter and returns nothing.

        Parameters:
            self (object): The object that is calling this function.

    Args:
        self: Access the class variables and methods

    Returns:
        A list of lists

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        sg.theme('Default1')

        __Line1 = [sg.Push(), sg.Text(font=("Helvetica", 10), justification="center", key="--progress_text--"),
                   sg.Push()]

        __Line2 = [sg.Push(), sg.Text(font=("Helvetica", 10), justification="center", key="--timer--"),
                   sg.Text(font=("Helvetica", 10), justification="center", key="--time_est--"), sg.Push()]

        __Line3 = [
            sg.ProgressBar(max_value=self.__batches, bar_color=("#920303", "#C9c8c8"), orientation='h', size=(30, 20),
                           key='--progress_bar--')]


        layout = [__Line1, __Line2, __Line3]

        self.__layout = layout

    def createGui(self, Sourcetype):

        """
    The createGui function is the main function that creates the GUI.
    It takes in a type parameter which determines what kind of batch processor to use.
    The createGui function then sets up all the variables and objects needed for
    the program to run, including: window, start_time, update_text, valueObj (DataTransfer),
    processorObject (BatchProcessorConstructionMonitor or BatchProcessorUtahRealestate),
    and threading objects for TimeUpdater and ValueChecker functions. The createGui function also starts these threads.

    Args:
        self: Access the object itself
        Sourcetype: Determine which batch processor to use

    Returns:
        The dataframe

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__window = sg.Window('Progress', self.__layout, finalize=True, icon=ImageLoader("taskbar_icon.ico"))

        start_time = datetime.datetime.now().replace(microsecond=0)
        update_text = f"Batch {0} completed"
        self.__window['--progress_text--'].update(update_text)
        self.__window['--progress_bar--'].update(0)
        self.__window['--time_est--'].update("Est time needed 00:00:00")

        valueObj = DataTransfer()
        valueObj.setValue(0)

        if Sourcetype == "construction_monitor":

            processorObject = BatchProcessorConstructionMonitor(RestDomain=self.__restDomain,
                                                                NumBatches=self.__batches,
                                                                ParameterDict=self.__parameterDict,
                                                                HeaderDict=self.__headerDict,
                                                                ColumnSelection=self.__columnSelection,
                                                                valueObject=valueObj)
        elif Sourcetype == "utah_real_estate":
            processorObject = BatchProcessorUtahRealEstate(RestDomain=self.__restDomain,
                                                           NumBatches=self.__batches,
                                                           ParameterString=self.__parameterDict,
                                                           HeaderDict=self.__headerDict,
                                                           valueObject=valueObj)

        threading.Thread(target=self.TimeUpdater,
                         args=(start_time,),
                         daemon=True).start()
        print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | TimeUpdater Thread Successfully Started")

        batchFuncThread = threading.Thread(target=processorObject.FuncSelector,
                                           daemon=False)
        batchFuncThread.start()
        print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | BatchFunc Thread Successfully Started")
        threading.Thread(target=self.ValueChecker,
                         args=(valueObj,),
                         daemon=False).start()
        print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | ValueChecker Thread Successfully Started")

        while True:

            self.ProgressUpdater(valueObj)

            if valueObj.getValue() == -999:
                break

            window, event, values = sg.read_all_windows()
            if event.startswith('update'):
                __key_to_update = event[len('update'):]
                window[__key_to_update].update(values[event])
                window.refresh()
                pass

            if event == sg.WIN_CLOSED or event == "Cancel" or event == "Exit":
                break

            time.sleep(0.1)

        self.dataframe = processorObject.dataframe
        self.__window.close()

        PopupWrapped(text="Api Request Completed", windowType="notice")

    def ProgressUpdater(self, valueObj):
        """
    The ProgressUpdater function is a callback function that updates the progress bar and text
    in the GUI. It takes in one argument, which is an object containing information about the
    current batch number. The ProgressUpdater function then checks if this value has changed from
    the last time it was called (i.e., if we are on a new batch). If so, it updates both the progress
    bar and text with this new information.

    Args:
        self: Make the progressupdater function an instance method
        valueObj: Get the current value of the batch counter

    Returns:
        The value of the batch counter

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        if valueObj.getValue() != self.__batch_counter:
            self.__batch_counter = valueObj.getValue()

            __update_text = f"Batch {self.__batch_counter}/{self.__batches} completed"

            self.__window.write_event_value('update--progress_bar--', self.__batch_counter)
            self.__window.write_event_value('update--progress_text--', __update_text)
        else:
            pass

    def TimeUpdater(self, start_time):

        """
    The TimeUpdater function is a thread that updates the time elapsed and estimated time needed to complete
    the current batch. It does this by reading the start_time variable passed in, getting the current time,
    calculating how much time has passed since start_time was set and then updating a timer string with that value.
    It then calculates an estimation of how long it will take to finish all batches based on how many batches have been completed so far.

    Args:
        self: Make the function a method of the class
        start_time: Get the time when the function is called

    Returns:
        A string that is updated every 0

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        while True:
            if self.__batch_counter < self.__batches:

                __current_time = datetime.datetime.now().replace(microsecond=0)

                __passed_time = __current_time - start_time

                __timer_string = f"Time Elapsed {__passed_time}"

                try:
                    self.__window.write_event_value('update--timer--', __timer_string)
                except AttributeError as e:
                    print(
                        f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | BatchProgressGUI.py | Error = {e} | Timer string attribute error, this is okay if the display looks good, this exception omits fatal crashes due to an aesthetic error")
                    break

                __passed_time = __passed_time.total_seconds()

                try:
                    __time_est = datetime.timedelta(
                        seconds=(__passed_time * (self.__batches / self.__batch_counter) - __passed_time)).seconds
                except:
                    __time_est = datetime.timedelta(
                        seconds=(__passed_time * self.__batches - __passed_time)).seconds

                __time_est = time.strftime('%H:%M:%S', time.gmtime(__time_est))

                __end_string = f"Est time needed {__time_est}"
                self.__window.write_event_value('update--time_est--', __end_string)
            else:
                __end_string = f"Est time needed 00:00:00"
                self.__window.write_event_value('update--time_est--', __end_string)
            time.sleep(0.25)

    def ValueChecker(self, ObjectVal):
        """
    The ValueChecker function is a thread that checks the value of an object.
        It will check if the value has changed, and if it has, it will return True.
        If not, then it returns False.

    Args:
        self: Represent the instance of the class
        ObjectVal: Get the value of the object

    Returns:
        True if the value of the object has changed, and false if it hasn't

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        while True:
            time.sleep(0.3)
            if self.__batch_counter != ObjectVal.getValue():
                self.__batch_counter = ObjectVal.getValue()
                return True
            else:
                return False
