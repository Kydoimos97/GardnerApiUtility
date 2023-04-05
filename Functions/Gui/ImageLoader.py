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
import base64
import os
from os.path import join, normpath
from io import BytesIO
from PIL import Image


def ImageLoader(file):
    # Create Source path
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
