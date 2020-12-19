##  Project Descreption
  
This project is an automation for Search Ads 360 data reporting.  The scripts efficiently automate the extraction, tranformation & load process.
The data extraction script eliminates the need for manual report download, saving time through automating a monthly report data pull. The next module of the project transforms the downloaded report.  It focuses on formating the data types, rearranging and renaming the columns for database compatability.
The final module, the data load, automates the import to the AWS s3 bucket (the data lake).  The data is then easily accessible for Tableau reporting dashboards

##  Getting Started

In order to use this package, you first need to go through the following steps:

##  Installation

Install the packages listed in requirements.txt in a virtualenv .

###  Mac/Linux
  
```bash
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install -r requirements.txt
```
  
###  Windows

```
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install requirements.txt
```

###  Supported Python Versions

Python >= 3.5


##  Create a project and set up authorization
  
Follow the instructions described below to create a project in Google API Console and retrieve credentials to make API calls.

https://developers.google.com/search-ads/v2/authorizing

##  Running the tests

Use the credentials in search_ads_360_data_extract.py to generate a report and extract the data in .csv file. 

Set credentials in the AWS credentials profile file on your local system, located at:

~/.aws/credentials on Linux, macOS, or Unix

C:\Users\USERNAME\.aws\credentials on Windows


Run main.py file to complete the full ETL (Extract, Transform & Load) process

```bash
$ python main.py
```




