#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import datetime
import math
from datetime import date

import pandas as pd
import requests

from API_Calls.Functions.DataFunc.DataSupportFunctions import StringToList


def BatchCalculator(TotalRecords, Argument_Dict):
    """
The BatchCalculator function takes two arguments:
    1. TotalRecords - the total number of records in the database
    2. Argument_Dict - a dictionary containing all the arguments passed to this function by the user

Args:
    TotalRecords: Determine the number of batches that will be needed to complete the query
    Argument_Dict: Pass in the arguments that will be used to query the database

Returns:
    The total number of batches that will be made

Doc Author:
    Willem van der Schans, Trelent AI
"""
    try:
        document_limit = Argument_Dict["size"]
    except Exception as e:
        # Logging
        print(
            f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | BatchProcessing.py |Error = {e} | Batch Calculator document limit overwritten to 200 from input")
        document_limit = 200

    return int(math.ceil(float(TotalRecords) / float(document_limit)))


class BatchProcessorConstructionMonitor:

    def __init__(self, RestDomain, NumBatches, ParameterDict, HeaderDict, ColumnSelection, valueObject):

        """
    The __init__ function is the constructor for a class. It is called when an object of that class
    is created, and it sets up the attributes of that object. In this case, we are setting up our
    object to have a dataframe attribute (which will be used to store all of our data), as well as
    attributes for each parameter in our ReST call.

    Args:
        self: Represent the instance of the class
        RestDomain: Specify the domain of the rest api
        NumBatches: Determine how many batches of data to retrieve
        ParameterDict: Pass in the parameters that will be used to make the api call
        HeaderDict: Pass the header dictionary from the main function to this class
        ColumnSelection: Determine which columns to pull from the api
        valueObject: Pass in the value object that is used to determine what values are returned

    Returns:
        An object of the class

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.dataframe = None
        self.__numBatches = NumBatches
        self.__parameterDict = ParameterDict
        self.__restDomain = RestDomain
        self.__headerDict = HeaderDict
        self.__columnSelection = ColumnSelection
        self.valueObject = valueObject
        self.__maxRequests = 10000
        self.__requestCount = math.ceil(self.__numBatches / (self.__maxRequests / int(self.__parameterDict['size'])))
        self.__requestCalls = math.ceil(self.__maxRequests / int(self.__parameterDict['size']))
        self.__dateTracker = None

    def FuncSelector(self):
        """
    The FuncSelector function is a function that takes the valueObject and passes it to the ConstructionMonitorProcessor function.
    The ConstructionMonitorProcessor function then uses this valueObject to determine which of its functions should be called.

    Args:
        self: Represent the instance of the class

    Returns:
        The result of the constructionmonitorprocessor function

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.ConstructionMonitorProcessor(self.valueObject)

    def ConstructionMonitorProcessor(self, valueObject):
        """
    The ConstructionMonitorProcessor function will use requests to get data from
       ConstructionMontior.com's ReST API and store it into a pandas DataFrame object called __df (which is local). This
       process will be repeated until all the data has been collected from ConstructionMonitor.com's ReST API, at which point __df will contain all

    Args:
        self: Represent the instance of the object itself
        valueObject: Update the progress bar in the gui

    Returns:
        A dataframe

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        __df = None
        for callNum in range(0, self.__requestCount):
            self.__parameterDict["from"] = 0

            if self.__requestCount > 1 and callNum != self.__requestCount - 1:
                __batchNum = self.__requestCalls
                if __df is None:
                    self.__dateTracker = str(date.today())
                else:
                    self.__dateTracker = min(pd.to_datetime(__df['lastIndexedDate'])).strftime('%Y-%m-%d')
            elif self.__requestCount == 1:
                __batchNum = self.__numBatches
                self.__dateTracker = str(date.today())
            else:
                __batchNum = self.__numBatches / (self.__maxRequests / int(self.__parameterDict['size'])) - (
                        self.__requestCount - 1)
                self.__dateTracker = min(pd.to_datetime(__df['lastIndexedDate'])).strftime('%Y-%m-%d')

            self.__parameterDict['dateEnd'] = self.__dateTracker

            for record in range(0, int(math.ceil(__batchNum))):
                if record != 0:
                    self.__parameterDict["from"] = record * int(self.__parameterDict["size"])

                response = requests.post(url=self.__restDomain,
                                         headers=self.__headerDict,
                                         json=self.__parameterDict)

                counter = 0
                try:
                    response = response.json()['hits']['hits']
                except KeyError as e:
                    # Logging
                    print(
                        f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | BatchProcessing.py |Error = {e} | Count Request Error Server Response: {response.json()} | Batch = {record} | Parameters = {self.__parameterDict} | Headers = {self.__headerDict}")
                    continue

                valueObject.setValue(valueObject.getValue() + 1)

                if record == 0 and callNum == 0:
                    __df = pd.json_normalize(response[counter]["_source"])
                    __df["id"] = response[counter]['_id']
                    __df["county"] = response[counter]["_source"]['county']['county_name']
                    counter += 1

                for i in range(counter, len(response)):
                    __tdf = pd.json_normalize(response[i]["_source"])
                    __tdf["id"] = response[i]['_id']
                    __tdf["county"] = response[i]["_source"]['county']['county_name']
                    __df = pd.concat([__df, __tdf], ignore_index=True)

        if self.__columnSelection is not None:
            __col_list = StringToList(self.__columnSelection)
            __col_list.append("id")
            __col_list.append("county")
        else:
            pass

        self.dataframe = __df
        valueObject.setValue(-999)


class BatchProcessorUtahRealEstate:

    def __init__(self, RestDomain, NumBatches, ParameterString, HeaderDict, valueObject):
        """
    The __init__ function is the constructor for a class. It is called when an object of that class
    is instantiated, and it sets up the attributes of that object. In this case, we are setting up
    the dataframe attribute to be None (which will be set later), and we are also setting up some
    other attributes which will help us make our API calls.

    Args:
        self: Represent the instance of the class
        RestDomain: Specify the domain of the rest api
        NumBatches: Determine how many batches of data to pull from the api
        ParameterString: Pass the parameters to the rest api
        HeaderDict: Pass in the header information for the api call
        valueObject: Create a dataframe from the json response

    Returns:
        The instance of the class

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.dataframe = None
        self.__numBatches = NumBatches
        self.__parameterString = ParameterString
        self.__restDomain = RestDomain
        self.__headerDict = HeaderDict
        self.valueObject = valueObject

    def FuncSelector(self):
        """
    The FuncSelector function is a function that takes the valueObject as an argument and then calls the appropriate
        function based on what was selected in the dropdown menu.  The valueObject is passed to each of these functions
        so that they can access all of its attributes.

    Args:
        self: Represent the instance of the class

    Returns:
        The function that is selected by the user

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.BatchProcessingUtahRealestateCom(self.valueObject)

    def BatchProcessingUtahRealestateCom(self, valueObject):
        """
    The BatchProcessingUtahRealestateCom function is a function that takes in the valueObject and uses it to
       update the progress bar. It also takes in self, which contains all the necessary information for this
       function to work properly. The BatchProcessingUtahRealestateCom function will then use requests to get data from
       UtahRealestate.com's ReST API and store it into a pandas DataFrame object called __df (which is local). This
       process will be repeated until all the data has been collected from UtahRealestate.com's ReST API, at which point __df will contain all

    Args:
        self: Represent the instance of the class
        valueObject: Pass the value of a progress bar to the function

    Returns:
        A dataframe of the scraped data

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        __df = pd.DataFrame()

        for batch in range(self.__numBatches):

            if batch == 0:
                response = requests.get(f"{self.__restDomain}{self.__parameterString}&top=200",
                                        headers=self.__headerDict)

                response_temp = response.json()
                __df = pd.json_normalize(response_temp, record_path=['value'])

            else:
                response = requests.get(f"{self.__restDomain}{self.__parameterString}&top=200&$skip={batch * 200}",
                                        headers=self.__headerDict)

                response_temp = response.json()
                response_temp = pd.json_normalize(response_temp, record_path=['value'])
                __df = pd.concat([__df, response_temp], ignore_index=True)

            valueObject.setValue(valueObject.getValue() + 1)

        self.dataframe = __df
        valueObject.setValue(-999)
