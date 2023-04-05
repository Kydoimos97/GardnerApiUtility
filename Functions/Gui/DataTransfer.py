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
class DataTransfer():

    def __init__(self):
        """
    The __init__ function is called when the class is instantiated.
    It sets the initial value of self.__value to 0.

    Args:
        self: Represent the instance of the class

    Returns:
        Nothing

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__value = 0

    def setValue(self, value):
        """
    The setValue function sets the value of the object.


    Args:
        self: Represent the instance of the class
        value: Set the value of the instance variable __value

    Returns:
        The value that was passed to it

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        self.__value = value

    def getValue(self):
        """
    The getValue function returns the value of the private variable __value.
    This is a getter function that allows access to this private variable.

    Args:
        self: Represent the instance of the class

    Returns:
        The value of the instance variable

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        return self.__value

    def whileValue(self):
        """
    The whileValue function is a function that will run the getValue function until it is told to stop.
    This allows for the program to constantly be checking for new values from the sensor.

    Args:
        self: Refer to the current instance of the class

    Returns:
        The value of the input

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        while True:
            self.getValue()
