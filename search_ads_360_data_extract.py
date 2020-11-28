"""
created on Tue Dec  3 13:49:12 2019
@author: mamuka.chikovani


# -*- coding: utf-8 -*-
"""
import httplib2
from apiclient.discovery import build
from oauth2client import GOOGLE_TOKEN_URI
from oauth2client.client import OAuth2Credentials, HttpAccessTokenRefreshError
import time
import json
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# import pandas as pd
import pprint

#def create_credentials(client_id, client_secret, refresh_token):
def create_credentials():
  """Create Google OAuth2 credentials.
  
  Args:
    client_id: Client id of a Google Cloud console project.
    client_secret: Client secret of a Google Cloud console project.
    refresh_token: A refresh token authorizing the Google Cloud console project
      to access the DS data of some Google user.
  Returns:
    OAuth2Credentials
    
  """
  client_id = 'your_client_id'
  client_secret = 'your_client_secret'
  refresh_token = '123456789'
  #access_token = 'client_secret.json'
  
  return OAuth2Credentials(access_token=None,
                           client_id=client_id,
                           client_secret=client_secret,
                           refresh_token=refresh_token,
                           token_expiry=None,
                           token_uri=GOOGLE_TOKEN_URI,
                           user_agent=None)
  

def get_service(credentials):
  """Set up a new Doubleclicksearch service.
  Args:
    credentials: An OAuth2Credentials generated with create_credentials, or
    flows in the oatuh2client.client package.
  Returns:
    An authorized Doubleclicksearch serivce.
  """
  # Use the authorize() function of OAuth2Credentials to apply necessary credential
  # headers to all requests.
  http = credentials.authorize(http = httplib2.Http())

  # Construct the service object for the interacting with the Search Ads 360 API.
  service = build('doubleclicksearch', 'v2', http=http)
  return service


def request_report(service):
  """Request sample report and print the report ID that DS returns. See Set Up Your Application.
  Args:
    service: An authorized Doubleclicksearch service.
  Returns:
    The report id.
    
  """
  
  month_start_date = datetime.today().replace(day=1)

  start_date = month_start_date - relativedelta(months=1)
  end_date = month_start_date - timedelta(days=1)
  
    
  request = service.reports().request(
      body=
      {
        "reportScope": {
            "agencyId": "your_agancy_id", 
            "advertiserId": "your_agancy_id",
             },
        "reportType": "account",
        "columns": [
            
                
               # { "columnName": "date" },
           
           
              
            # { "columnName": "advertiser" },
            { "columnName": "account" },
            
            

            
            
            
           # { "columnName": "impr" },
            #{ "columnName": "clicks" },
            { "columnName": "cost" },
            {"savedColumnName":'key action'}     #GA Goal Completion

           

        
          ],
                
                
                # update this part
         "timeRange" : {
            "startDate" : datetime.strftime(start_date, '%Y-%m-%d'),
            "endDate" : datetime.strftime(end_date, '%Y-%m-%d')
          },
         # "filters": [
         #   {
           ##   "column" : { "columnName": "Campaign" },
           #   "operator" : "containsSubstring",
             # "values" : [
              #  "http://www.foo.com",
               # "http://www.bar.com"
              #]
            #}
          #],

          "downloadFormat": "csv",
          "maxRowsPerFile": 6000000,
          "statisticsCurrency": "agency",
          #"verifySingleTimeZone": "false",
          #"includeRemovedEntities": "false"
        }
  )

  json_data = request.execute()
  
  pprint.pprint(json_data)
     
  return json_data['id']

 # df = pd.DataFrame(json_data)
  




def poll_report():
  """Poll the API with the reportId until the report is ready, up to ten times.
  Args:
    service: An authorized Doubleclicksearch service.
    report_id: The ID DS has assigned to a report.
  """
  
  credentials = create_credentials()
  service = get_service(credentials)
  report_id = request_report(service)
  
  print(report_id)
                             
  
  for _ in range(10):
    try:
      request = service.reports().get(reportId=report_id)
      json_data = request.execute()
      if json_data['isReportReady']:
        pprint.pprint('The report is ready.')

        # For large reports, DS automatically fragments the report into multiple
        # files. The 'files' property in the JSON object that DS returns contains
        # the list of URLs for file fragment. To download a report, DS needs to
        # know the report ID and the index of a file fragment.
        for i in range(len(json_data['files'])):
          pprint.pprint('Downloading fragment ' + str(i) + ' for report ' + report_id)
          download_files(service, report_id, str(i)) # See Download the report.
        return

      else:
        pprint.pprint('Report is not ready. I will try again.')
        time.sleep(10)
    except HttpError as e:
      error = json.loads(e.content)['error']['errors'][0]

      # See Response Codes
      pprint.pprint('HTTP code %d, reason %s' % (e.resp.status, error['reason']))
      break



  
def download_files(service, report_id, report_fragment):
  """Generate and print sample report.
  Args:
    service: An authorized Doubleclicksearch service.
    report_id: The ID DS has assigned to a report.
    report_fragment: The 0-based index of the file fragment from the files array.
  """
  f = open('keytruda_lenvima_consumer_report' + '.csv', 'wb')
  request = service.reports().getFile(reportId=report_id, reportFragment=report_fragment)
  f.write(request.execute())
  f.close() 
  
 
  return f
  
def main():
    creds = create_credentials()
    service = get_service(creds)
    request_report(service)
    poll_report()

if __name__ == '__main__':
  main()
        


    
