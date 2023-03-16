import datetime
import threading
import PySimpleGUI as sg
import time
from API_Calls.Functions.DataFunc.BatchProcessing import BatchProcessorConstructionMonitor, BatchProcessorUtahRealEstate
from API_Calls.Functions.Gui.DataTransfer import DataTransfer
from API_Calls.Functions.Gui.ImageLoader import ImageLoader
from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped

counter = 1


class BatchProgressGUI():

    def __init__(self, BatchesNum, RestDomain, ParameterDict, HeaderDict, Type, ColumnSelection=None):

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
        self.CreateProgressLayout()
        self.createGui(self.__type)

    def CreateProgressLayout(self):
        # ----------Layout----------
        sg.theme('Default1')

        __Line1 = [sg.Push(), sg.Text(font=("Helvetica", 10), justification="center", key="--progress_text--"),
                   sg.Push()]

        __Line2 = [sg.Push(), sg.Text(font=("Helvetica", 10), justification="center", key="--timer--"),
                   sg.Text(font=("Helvetica", 10), justification="center", key="--time_est--"), sg.Push()]

        __Line3 = [
            sg.ProgressBar(max_value=self.__batches, bar_color=["#920303", "#C9c8c8"], orientation='h', size=(30, 20),
                           key='--progress_bar--')]

        __Line4 = [sg.Push(), sg.Cancel(), sg.Push()]

        layout = [__Line1, __Line2, __Line3, __Line4]

        self.__layout = layout

    def createGui(self, type):
        # ----------Window and Variables----------
        self.__window = sg.Window('Progress', self.__layout, finalize=True, icon=ImageLoader("taskbar_icon.ico"))

        # Set initial Positions
        start_time = datetime.datetime.now().replace(microsecond=0)
        update_text = f"Batch {0} completed"
        self.__window['--progress_text--'].update(update_text)
        self.__window['--progress_bar--'].update(0)
        self.__window['--time_est--'].update("Est time needed 00:00:00")

        valueObj = DataTransfer()
        valueObj.setValue(0)

        if type == "construction_monitor":

            print("1") #Debug
            processorObject = BatchProcessorConstructionMonitor(RestDomain=self.__restDomain,
                                                                NumBatches=self.__batches,
                                                                ParameterDict=self.__parameterDict,
                                                                HeaderDict=self.__headerDict,
                                                                ColumnSelection=self.__columnSelection,
                                                                valueObject=valueObj)
        elif type == "utah_real_estate":
            print("2") #Debug
            processorObject = BatchProcessorUtahRealEstate(RestDomain=self.__restDomain,
                                                           NumBatches=self.__batches,
                                                           ParameterString=self.__parameterDict,
                                                           HeaderDict=self.__headerDict,
                                                           valueObject=valueObj)

        # Set MultiThreading
        threading.Thread(target=self.TimeUpdater,
                         args=(start_time,),
                         daemon=True).start()

        batchFuncThread = threading.Thread(target=processorObject.FuncSelector,
                                           daemon=False)

        batchFuncThread.start()

        threading.Thread(target=self.ValueChecker,
                         args=(valueObj,),
                         daemon=False).start()

        # Set Main Window Event Loop
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
                # raise KeyboardInterrupt("User cancelled the program")
                break

            time.sleep(0.1)

        self.dataframe = processorObject.dataframe
        self.__window.close()

        PopupWrapped(text="Api Request Completed", windowType="notice")

    # ---------Progress Bar Function----------
    def ProgressUpdater(self, valueObj):
        if valueObj.getValue() != self.__batch_counter:
            self.__batch_counter = valueObj.getValue()

            __update_text = f"Batch {self.__batch_counter}/{self.__batches} completed"

            # Push Updates
            self.__window.write_event_value('update--progress_bar--', self.__batch_counter)
            self.__window.write_event_value('update--progress_text--', __update_text)
        else:
            pass

    # ----------Time Updater Function----------
    def TimeUpdater(self, start_time):

        while True:
            if self.__batch_counter < self.__batches:
                # ----------Timer----------
                # Get Current Time
                __current_time = datetime.datetime.now().replace(microsecond=0)

                # Get Time
                __passed_time = __current_time - start_time

                # Create Updated String and Update
                __timer_string = f"Time Elapsed {__passed_time}"

                try:
                    self.__window.write_event_value('update--timer--', __timer_string)
                except AttributeError:
                    # Allows for thread specific check if window has closed since we can't read events here
                    break

                # ----------Time Estimator----------
                # Get time in seconds
                __passed_time = __passed_time.total_seconds()

                # Get time Estimation and set format
                try:
                    __time_est = datetime.timedelta(
                        seconds=(__passed_time * (self.__batches / self.__batch_counter) - __passed_time)).seconds
                except:
                    __time_est = datetime.timedelta(
                        seconds=(__passed_time * self.__batches - __passed_time)).seconds

                __time_est = time.strftime('%H:%M:%S', time.gmtime(__time_est))

                # Create Updated String and Update
                __end_string = f"Est time needed {__time_est}"
                self.__window.write_event_value('update--time_est--', __end_string)
            else:
                __end_string = f"Est time needed 00:00:00"
                self.__window.write_event_value('update--time_est--', __end_string)
            time.sleep(0.25)

    def ValueChecker(self, ObjectVal):
        while True:
            time.sleep(0.3)
            if self.__batch_counter != ObjectVal.getValue():
                self.__batch_counter = ObjectVal.getValue()
                return True
            else:
                return False
