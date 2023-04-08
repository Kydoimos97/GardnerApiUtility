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
import os
from pathlib import Path

import pandas as pd

from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped


class FileSaver:

    def __init__(self, method, outputDF, AppendingPath=None):
        """
    The __init__ function is called when the class is instantiated.
    It sets up the instance of the class, and defines all variables that will be used by other functions in this class.
    The __init__ function takes two arguments: self and method.  The first argument, self, refers to an instance of a
    class (in this case it's an instance of DataFrameSaver). The second argument, method refers to a string value that
    is passed into DataFrameSaver when it's instantiated.

    Args:
        self: Represent the instance of the class
        method: Determine which dataframe to append the new data to
        outputDF: Pass in the dataframe that will be saved to a csv file
        AppendingPath: Specify the path to an existing csv file that you want to append your dataframe to

    Returns:
        Nothing

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.docPath = Path(os.path.expanduser('~/Documents')).joinpath("GardnerUtilData").joinpath(
            datetime.datetime.today().strftime('%m%d%Y'))
        self.data = outputDF
        self.dataAppending = None
        self.appendFlag = True
        self.fileName = f"{method}_{datetime.datetime.today().strftime('%m%d%Y_%H%M%S')}.csv"
        self.uiFlag = True

        if method.lower() == "ure":
            self.primaryKey = "ListingKeyNumeric"
        elif method.lower() == "cm":
            self.primaryKey = "id"
        elif "realtor" in method.lower():
            self.primaryKey = None
            self.uiFlag = False
        elif method.lower() == "cfbp":
            self.primaryKey = None
            self.uiFlag = False
        else:
            raise ValueError("method input is invalid choice one of 4 options: URE, CM, Realtor, CFBP")

        if AppendingPath is None:
            self.appendFlag = False
        else:
            self.dataAppending = pd.read_csv(AppendingPath)

        if self.appendFlag:
            if self.primaryKey is not None:
                # Due to low_memory loading the columns are not typed properly,
                # since we are comparing this will be an issue since we need to do type comparisons,
                # so here we coerce the types of the primary keys to numeric.
                # If another primary key is ever chosen make sure to core to the right data type.
                self.dataAppending[self.primaryKey] = pd.to_numeric(self.dataAppending[self.primaryKey])
                self.data[self.primaryKey] = pd.to_numeric(self.data[self.primaryKey])

                self.outputFrame = pd.concat([self.dataAppending, self.data]).drop_duplicates(subset=[self.primaryKey],
                                                                                              keep="last")
            else:
                self.outputFrame = pd.concat([self.dataAppending, self.data]).drop_duplicates(keep="last")
        else:
            self.outputFrame = self.data

        if os.path.exists(self.docPath):
            self.outputFrame.to_csv(self.docPath.joinpath(self.fileName), index=False)
        else:
            os.mkdir(self.docPath)
            self.outputFrame.to_csv(self.docPath.joinpath(self.fileName), index=False)

        if self.uiFlag:
            if self.appendFlag:
                PopupWrapped(text=f"File Appended and Saved to {self.docPath.joinpath(self.fileName)}",
                             windowType="noticeLarge")

                # Logging
                print(
                    f"{method} API request Completed at {datetime.datetime.now()} | File Appended and Saved to {self.docPath.joinpath(self.fileName)} | Exit Code 0")
            else:
                PopupWrapped(text=f"File Saved to {self.docPath.joinpath(self.fileName)}", windowType="noticeLarge")

                # Logging
                print(
                    f"{method} API request Completed at {datetime.datetime.now()} | File Saved to {self.docPath.joinpath(self.fileName)} | Exit Code 0")
        else:
            pass

    def getPath(self):
        """
    The getPath function returns the path to the file.
        It is a string, and it joins the docPath with the fileName.

    Args:
        self: Represent the instance of the class

    Returns:
        The path to the file

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        return str(self.docPath.joinpath(self.fileName))
