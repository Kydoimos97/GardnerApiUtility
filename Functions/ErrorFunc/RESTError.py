import time

from Functions.DataFunc.AuthUtil import AuthUtil
from Functions.ErrorFunc.ErrorPrint import RESTErrorPrint
from Functions.Gui.PopupWrapped import PopupWrapped


def RESTError(response):
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
    # Manual Error Codes
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
    # Catch All
    else:
        RESTErrorPrint(response)
        raise Exception(f"Status Code = {status_code} | An unknown exception occurred")
