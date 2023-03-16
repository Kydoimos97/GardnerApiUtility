def RESTErrorPrint(response):
    if isinstance(response, int):
        print(f"Resource Response: {response}")
    else:
        response_txt = response.text
        print(f"Resource Response: {response_txt}")