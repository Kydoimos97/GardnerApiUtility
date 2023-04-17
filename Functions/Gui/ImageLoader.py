#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import base64
import os
from io import BytesIO
from os.path import join, normpath

from PIL import Image


def ImageLoader(file):
    """
The ImageLoader function takes in a file name and returns the image as a base64 encoded string.
This is used to send images to the API for processing.

Args:
    file: Specify the image file to be loaded

Returns:
    A base64 encoded image string

Doc Author:
    Willem van der Schans, Trelent AI
"""
    try:
        __path = normpath(join(str(os.getcwd().split("API_Calls", 1)[0]), "API_Calls"))
        __path = normpath(join(__path, "Images"))
        __path = join(__path, file).replace("\\", "/")

        image = Image.open(__path)

        __buff = BytesIO()

        image.save(__buff, format="png")

        img_str = base64.b64encode(__buff.getvalue())

        return img_str
    except Exception as e:
        # We cannot log this error like other errors due to circular imports
        raise e
