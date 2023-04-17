#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


def StringToList(string):
    """
The StringToList function takes a string and converts it into a list.
    The function is used to convert the input from the user into a list of strings, which can then be iterated through.

Args:
    string: Split the string into a list

Returns:
    A list of strings

Doc Author:
    Willem van der Schans, Trelent AI
"""
    listOut = list(string.split(","))
    return listOut
