# Gardner Policy Institute API Utility</h1>
#### Author: Willem van der Schans</h4>
#### Commissioner: Gardner Policy Institute </h4>
#### Description: A Python utility for generating API requests from ConstructionMonitor.com, Utah Real Estate.com, Realtor.com, and the US Census APIs </h4>

## Notes

1. No functionality for macOS or Linux has been developed or is planned for the future.
2. Documentation is available within the repository.

## VERSION INFO
1. Python=3.10
2. pandas~=1.5.2
3. requests~=2.28.1
4. beautifulsoup4~=4.11.1
5. pysimplegui~=4.60.4
6. cryptography~=38.0.1
7. pillow~=9.2.0

_Note: All dependencies are included in the Windows installer_

# Authentication Requirements
Authentication Keys are needed for utahrealestate.com and constructionmonitor.com

The program provides a safe way to store and use authentication keys

# Changelog

## Initial release
### Version: 1.0.0
### Date: 2023-04-08

#### Core Functionality

    1. Optimized support for ConstructionMonitor.com, 
        Utah Real Estate.com, Realtor.com, and the US Census APIs
    2. Optimized support for generating API requests based on custom input parameters

#### User InterFace

    1. Optimized ui multithreading for faster processing
    2. Simplified user interface for better usability and user experience

#### File Functionality

    1. Added file browsing support to enhance appending accessibility

#### Logging and Error Handling

    1. Enhanced logging capabilities for code transparency and easy maintenance

    2. Enhanced error handling and exception reporting to prevent hard locks 
        while using the programs.

#### Security

    1. Enhanced security measures for handling sensitive user data using 
        locally generated keys

#### GUI

    1. Improved user interface threading for better usability and error handling

#### Other

    1. Fixed bugs and issues found in QA

## Version: 0.9.5
#### Date: 2023-04-05
	
	Improved documentation and code readability for easier use and maintenance
    Fixed bugs and issues found in QA

## Version: 0.9.0 
#### Date: 2023-03-16

	Enhanced Mainloop and interaction with spawned threads allowing for multiple API requests to be completed in sequence.
	Initial Github Commit

## Version: 0.8.0 
#### Date: 2023-03-12
	
	Added new utility functions for data cleaning, and appending

## Version: 0.7.0 
#### Date: 2023-03-02

	Implemented secure storage of authorization keys using an Authorization Utility and encryption


## Version: 0.6.0 
#### Date: 2023-02-25

	Enhanced GUI Utility Improvements. 
		- Descriptive processing pop-ups
		- Warning popups
		- MultiThreading
		- Completion Time Estimation

## Version: 0.5.0 
#### Date: 2023-02-15

	Added GUI to utility to enhance end-user accesibility.

## Version: 0.4.0 
#### Date: 2022-12-07

    Enhanced data processing and analysis functions for more accurate results
		1. Added support for appending to existing new documents to existing CSV files
		2. Added support for storing pulled data in CSV files
    Improved user interface for better usability and user experience

## Version: 0.3.0 
#### Date: 2022-11-15

	Added support for interacting with Realtor.com 
	Added support for interacting with ffiec.cfpb.gov [census] API.

## Version: 0.2.0 
#### Date: 2022-11-03	

	Improved batch processing for interacting with the ConstructionMonitor.com API
	Improved batch processing for interacting with the Utah Real Estate.com API

## Version: 0.1.0
#### Date: 2022-10-25

	Added support for interacting with the ConstructionMonitor.com API

## Version: 0.0.0
#### Date: 2022-10-15

	Added Support for UtahRealEstate.com
    Added new utility functions for data processing and manipulation
    Added documentation for all functions and classes
    Improved support for interacting with the US Census API	


# License
This software is licensed under Apache License, Version 2.0, January 2004 as found on http://www.apache.org/licenses/