#   This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/


# Setting NameSpace for maintenance

class settings:
    #   Version Checker
    #       Update accordingly using semantic versioning: https://semver.org/
    settingVersion = "1.2.0"
    #       Update in conjunction with settingDownloadSourceLink
    settingGithubApiUrl = "https://api.github.com/repos/Kydoimos97/GardnerApiUtility/releases/latest"

    #   PopUpWrapped
    #       Singular Reference free to change
    settingGenerationToolLink = 'https://www.debugbear.com/basic-auth-header-generator'
    #       Update in conjunction with settingDownloadSourceLink
    settingDownloadSourceLink = 'https://github.com/Kydoimos97/GardnerApiUtility/releases/latest'

    # CFBP Source
    #       This link downloads csv's immedately so minimal change is likely required in the source code
    settingCFBPLink = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?"

    # ConstructionMonitor Source
    #       Check the REST call and data parser when updating this
    settingCMRestDomain = "https://api.constructionmonitor.com/v2/powersearch/?"

    # Realtor.Com Source
    #       Updating This link likely requires a rewrite of the html parser
    settingRealtorLink = "https://www.realtor.com/research/data/"

    # UtahRealEstate Source
    #       API links are generated with hard references so updating this link requires a large code rewrite
    settingURERestDomain = "https://resoapi.utahrealestate.com/reso/odata/Property?"
