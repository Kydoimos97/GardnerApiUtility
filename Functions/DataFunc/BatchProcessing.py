import math
from datetime import date

import pandas as pd
import requests

from API_Calls.Functions.DataFunc.DataSupportFunctions import StringToList


def BatchCalculator(TotalRecords, Argument_Dict):
    try:
        document_limit = Argument_Dict["size"]
    except:
        document_limit = 200

    return int(math.ceil(float(TotalRecords) / float(document_limit)))


class BatchProcessorConstructionMonitor:

    def __init__(self, RestDomain, NumBatches, ParameterDict, HeaderDict, ColumnSelection, valueObject):
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
        self.ConstructionMonitorProcessor(self.valueObject)

    def ConstructionMonitorProcessor(self, valueObject):
        __df = None
        for callNum in range(0, self.__requestCount):
            self.__parameterDict["from"] = 0
            # Split Batches
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

                # Do Post call
                response = requests.post(url=self.__restDomain,
                                         headers=self.__headerDict,
                                         json=self.__parameterDict)

                counter = 0
                try:
                    response = response.json()['hits']['hits']
                except KeyError as e:
                    print(
                        f"Server Response: {response.json()} | Error: {e} | Batch = {record} | Parameters = {self.__parameterDict} | Headers = {self.__headerDict}")
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

        # __df.drop_duplicates(inplace=True, ignore_index=True) DEBUG

        self.dataframe = __df
        valueObject.setValue(-999)


class BatchProcessorUtahRealEstate():

    def __init__(self, RestDomain, NumBatches, ParameterString, HeaderDict, valueObject):
        self.dataframe = None
        self.__numBatches = NumBatches
        self.__parameterString = ParameterString
        self.__restDomain = RestDomain
        self.__headerDict = HeaderDict
        self.valueObject = valueObject

    def FuncSelector(self):
        self.BatchProcessingUtahRealestateCom(self.valueObject)

    def BatchProcessingUtahRealestateCom(self, valueObject):
        # Batch Process
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

        # __df.drop_duplicates(inplace=True, ignore_index=True) DEBUG

        self.dataframe = __df
        valueObject.setValue(-999)
