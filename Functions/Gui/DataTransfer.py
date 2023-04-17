#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


class DataTransfer:

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
