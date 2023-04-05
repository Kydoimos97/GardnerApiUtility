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
