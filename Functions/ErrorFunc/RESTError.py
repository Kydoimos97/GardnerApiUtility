#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import datetime

from API_Calls.Functions.ErrorFunc.ErrorPopup import ErrorPopup
from API_Calls.Functions.ErrorFunc.ErrorPrint import RESTErrorPrint


def RESTError(response):
    """
The RESTError function is a function that checks the status codes.
If it is 200, then everything went well and nothing happens. If it isn't 200, then an error message will be printed to
the console with information about what happened (i.e., if there was an authentication error or if the resource wasn't found).
The function also raises an exception and opens an error popup for easy debugging.

Args:
    response: Print out the response from the server

Returns:
    A text string

Doc Author:
    Trelent
"""
    if isinstance(response, int):
        status_code = response
    else:
        status_code = response.status_code

    if status_code == 200:
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Api Request completed successfully"
        print(textString)
        pass
    elif status_code == 301:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Endpoint redirection; check domain name and endpoint name"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 400:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Bad Request; check input arguments"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 401:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Authentication Error: No keys found"
        ErrorPopup(textString)
        raise PermissionError(textString)
    elif status_code == 402:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Authentication Error: Cannot access decryption Key in %appdata%/roaming/GardnerUtil/security"
        ErrorPopup(textString)
        raise PermissionError(textString)
    elif status_code == 403:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Access Error: the resource you are trying to access is forbidden"
        ErrorPopup(textString)
        raise PermissionError(textString)
    elif status_code == 404:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Resource not found: the resource you are trying to access does not exist on the server"
        ErrorPopup(textString)
        raise NameError(textString)
    elif status_code == 405:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Method is not valid, request rejected by server"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 408:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Requests timeout by server"
        ErrorPopup(textString)
        raise TimeoutError(textString)
    elif status_code == 503:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | The resource is not ready for the get request"
        ErrorPopup(textString)
        raise SystemError(textString)
    elif status_code == 701:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Error in coercing icon to bits (Imageloader.py)"
        ErrorPopup(textString)
        raise TypeError(textString)
    elif status_code == 801:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Resource Error, HTML cannot be parsed the website's HTML source might be changed"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 790:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Requests timeout within requests"
        ErrorPopup(textString)
        raise TimeoutError(textString)
    elif status_code == 791:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Too many redirects, Bad url"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 990:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | No password input"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 991:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | No username input"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 992:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | No authentication input (Basic or User/PW)"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 993:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Submission Error: input values could not be coerced to arguments"
        ErrorPopup(textString)
        print(ValueError(textString))
    elif status_code == 994:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Submission Error: server returned no documents"
        ErrorPopup(textString)
        raise ValueError(textString)
    elif status_code == 1000:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Catastrophic Error"
        ErrorPopup(textString)
        raise SystemError(textString)
    elif status_code == 1001:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | Main Function Error Break"
        raise SystemError(textString)
    elif status_code == 1100:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | User has cancelled the program execution"
        raise KeyboardInterrupt(textString)
    elif status_code == 1101:
        RESTErrorPrint(response)
        textString = f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | User returned to main menu using the exit button"
        print(textString)
    else:
        RESTErrorPrint(response)
        raise Exception(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Status Code = {status_code} | An unknown exception occurred")
