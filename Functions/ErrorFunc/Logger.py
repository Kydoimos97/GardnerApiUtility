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

import datetime
import os
import sys
from pathlib import Path


def logger():
    """
The logger function redirects stdout and stderr to log files in the user's AppData directory.

Args:

Returns:
    The filepaths of the log files created

Doc Author:
    Willem van der Schans, Trelent AI
"""
    dir_path = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Logs'))
    if os.path.exists(dir_path):
        pass
    else:
        if os.path.exists(Path(os.path.expandvars(r'%APPDATA%\GardnerUtil'))):
            os.mkdir(dir_path)
        else:
            os.mkdir(Path(os.path.expandvars(r'%APPDATA%\GardnerUtil')))
            os.mkdir(dir_path)

    def sorted_ls(path):

        """
    The sorted_ls function takes a path as an argument and returns the files in that directory sorted by modification time.

    Args:
        path: Specify the path of the directory to be sorted

    Returns:
        A list of files in the directory specified by path sorted by modification time

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))

    del_list = sorted_ls(dir_path)[0:(len(sorted_ls(dir_path)) - 50)]
    for file in del_list:
        os.remove(dir_path.joinpath(file))
        print(f"Log file {file} deleted")

    filePath = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Logs')).joinpath(
        f"stdout{datetime.datetime.today().strftime('%m%d%Y_%H%M%S')}.log")
    sys.stdout = open(filePath, 'w')

    filePath = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Logs')).joinpath(
        f"stderr{datetime.datetime.today().strftime('%m%d%Y_%H%M%S')}.log")
    sys.stderr = open(filePath, 'w')
