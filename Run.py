import os
from pathlib import Path
from Initializer import initializer
import datetime
import sys

# Setup Logging
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
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


# Clean old log files
del_list = sorted_ls(dir_path)[0:(len(sorted_ls(dir_path)) - 50)]
for file in del_list:
    os.remove(dir_path.joinpath(file))
    print(f"Log file {file} deleted")

# Coerce Out and Err to files
# filePath = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Logs')).joinpath(
#     f"stdout{datetime.datetime.today().strftime('%m%d%Y_%H%M%S')}.log")
# sys.stdout = open(filePath, 'w')

# filePath = Path(os.path.expandvars(r'%APPDATA%\GardnerUtil\Logs')).joinpath(
#     f"stderr{datetime.datetime.today().strftime('%m%d%Y_%H%M%S')}.log")
# sys.stderr = open(filePath, 'w')

initializer()
