import base64
import os
from os.path import join, normpath
from io import BytesIO
from PIL import Image


def ImageLoader(file):
    # Create Source path
    __path = normpath(join(str(os.getcwd().split("API_Calls", 1)[0]), "API_Calls"))
    __path = normpath(join(__path, "Images"))
    __path = join(__path, file).replace("\\", "/")

    # open Image
    image = Image.open(__path)

    # Create BytesIO object
    __buff = BytesIO()

    # Save image to buffer
    image.save(__buff, format="png")

    # Encode image to base64
    img_str = base64.b64encode(__buff.getvalue())

    # Return image_string
    return img_str
