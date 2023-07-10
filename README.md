
## Project Name: Search Ads 360 Data Reporting Automation

This project aims to automate the process of reporting Search Ads 360 (SA360) data. Python scripts are utilized to efficiently handle the extraction, transformation, and loading (ETL) process.

## Features
### Data Extraction: 
The data extraction script eliminates the manual effort of downloading reports from the SA360 platform. It automates the monthly data pull for report generation, saving valuable time.

### Data Transformation:
The transformation module focuses on formatting the data types, rearranging columns, and renaming them to ensure compatibility with the database. This step prepares the data for seamless integration.

### Data Load:
The data load module automates the loading process to AWS S3 data lake. This enables easy accessibility of the data for reporting purposes using Tableau reporting dashboards through the Amazon Athena connector.

## Benefits
Time-Saving: Automating the data extraction eliminates the need for manual downloading, reducing effort and saving time.
Data Consistency: The transformation process ensures consistent data formatting and compatibility with the database.
Streamlined Reporting: The automated loading process enables quick and easy access to data for reporting in Tableau dashboards through Amazon Athena.

## Requirements
* Python 3.x
* SA360 Account Credentials
* AWS Account Credentials
* Tableau and Amazon Athena Configuration


##  Getting Started

Clone the repository: git clone git@github.com:mamukachikovani/search-ads-360-ETL.git

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

##  Run the tests

Use the credentials in search_ads_360_data_extract.py to generate a report and extract the data in .csv file. 

Use AWS Command Line Interface (AWS CLI) to configure basic settings to interact with AWS:

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

By default, AWS credentials profile file will be located at:

~/.aws/credentials on Linux, macOS, or Unix

C:\Users\USERNAME\.aws\credentials on Windows


Run main.py file to complete the full ETL (Extract, Transform & Load) process

```bash
$ python main.py
```

Feel free to customize and extend the project as per your specific requirements.


