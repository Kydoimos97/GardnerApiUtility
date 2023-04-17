#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


import datetime
import os
import sys
from pathlib import Path


def logger():
    """
The logger function creates a log file in the user's AppData directory.
The function will create the directory if it does not exist.
The function will also delete the oldest file when 100 logs have been saved to prevent bloat.

Args:

Returns:
    A file path to the log file that was created

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

    filePath = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Logs')).joinpath(
        f"{datetime.datetime.today().strftime('%m%d%Y_%H%M%S')}.log")
    sys.stdout = open(filePath, 'w')
    sys.stderr = sys.stdin = sys.stdout

    def sorted_ls(path):
        """
    The sorted_ls function takes a path as an argument and returns the files in that directory sorted by modification time.

    Args:
        path: Specify the directory to be sorted

    Returns:
        A list of files in a directory sorted by modification time

    Doc Author:
        Willem van der Schans, Trelent AI
    """
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))

    del_list = sorted_ls(dir_path)[0:(len(sorted_ls(dir_path)) - 100)]
    for file in del_list:
        os.remove(dir_path.joinpath(file))
        print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Log file {file} deleted")
