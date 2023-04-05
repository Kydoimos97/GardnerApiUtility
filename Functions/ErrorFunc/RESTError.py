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

from API_Calls.Functions.ErrorFunc.ErrorPrint import RESTErrorPrint


def RESTError(response):
    """
The RESTError function is used to check the status code of a response object and raise an exception if it is not 200.
The function takes in a response object as its only argument, checks the status_code attribute of that object, and
raises an appropriate exception based on what that code is. The exceptions are:

Args:
    response: Print out the response if there is an error

Returns:
    The response object

Doc Author:
    Willem van der Schans, Trelent AI
"""
    if isinstance(response, int):
        status_code = response
    else:
        status_code = response.status_code

    if status_code == 200:
        print(f"Status Code = {status_code} | Api Request completed successfully")
        pass
    elif status_code == 301:
        RESTErrorPrint(response)
        raise ValueError(f"Status Code = {status_code} | Endpoint redirection; check domain name and endpoint name")
    elif status_code == 400:
        RESTErrorPrint(response)
        raise ValueError(f"Status Code = {status_code} | Bad Request; check input argument")
    elif status_code == 401:
        RESTErrorPrint(response)
        raise PermissionError(f"Status Code = {status_code} | Authentication Error: use get_request_auth")
    elif status_code == 403:
        RESTErrorPrint(response)
        raise PermissionError(f"Status Code = {status_code} | Access Error: the resource you are trying to access "
                              f"is forbidden")
    elif status_code == 404:
        RESTErrorPrint(response)
        raise NameError(f"Status Code = {status_code} | Resource not found: the resource you are trying to access "
                        f"does not exist on the server")
    elif status_code == 405:
        RESTErrorPrint(response)
        raise SystemError(f"Status Code = {status_code} | Method is not valid, request rejected by server")
    elif status_code == 408:
        RESTErrorPrint(response)
        raise SystemError(f"Status Code = {status_code} | Requests timeout by server")
    elif status_code == 503:
        RESTErrorPrint(response)
        raise SystemError(f"Status Code = {status_code} | The resource is not ready for the get request")

    elif status_code == 790:
        raise SystemError(f"Status Code = {status_code} | Requests timeout within requests")
    elif status_code == 791:
        raise SystemError(f"Status Code = {status_code} | Too many redirects, bad url")
    elif status_code == 990:
        raise SystemError(f"Status Code = {status_code} | No password input")
    elif status_code == 991:
        raise SystemError(f"Status Code = {status_code} | No username input")
    elif status_code == 992:
        raise SystemError(f"Status Code = {status_code} | No authentication input (Basic or User/PW)")
    elif status_code == 1000:
        raise SystemError(f"Status Code = {status_code} | Catastrophic Error")
    elif status_code == 1100:
        raise KeyboardInterrupt(f"Status Code = {status_code} | User has cancelled the program execution")
    elif status_code == 1200:
        raise KeyboardInterrupt(f"Status Code = {status_code} | Request returned no documents")

    else:
        RESTErrorPrint(response)
        raise Exception(f"Status Code = {status_code} | An unknown exception occurred")
