#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/
import requests

from API_Calls.Functions.Gui.PopupWrapped import PopupWrapped


def versionChecker():
    """
The versionChecker function is used to check if the current version of the program is up-to-date.
It does this by comparing the latest release on GitHub.
If they are not equal, it will pop up a window telling you that there's an update available.

Args:

Returns:
    A popup window with the current version and latest version

Doc Author:
    Willem van der Schans, Trelent AI
"""
    current_version = "1.0.3"
    response = requests.get("https://api.github.com/repos/Kydoimos97/GardnerApiUtility/releases/latest")
    latest_version = response.json()['name']
    text_string = f"A new version is available \n" \
                  f"Running version: {current_version} \n" \
                  f"Latest version: {latest_version}"
    print(text_string)

    if current_version != latest_version:
        PopupWrapped(text_string, windowType="versionWindow")
