#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import datetime


def RESTErrorPrint(response):
    """
The RESTErrorPrint function is used to print the response from a ReST API call.
If the response is an integer, it will be printed as-is. If it's not an integer,
it will be converted to text and then printed.

Args:
    response: Print the response from a rest api call

Returns:
    The response text

Doc Author:
    Willem van der Schans, Trelent AI
"""
    if isinstance(response, int):
        print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Resource Response: {response}")
    else:
        response_txt = response.text
        print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Resource Response: {response_txt}")
