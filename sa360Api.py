#!/usr/bin/python2.7
"""Search Ads 360 API python script.

Search Ads 360 API script for making authentication, reporting,
and conversion API requests/responses.

Version: 1.0

Prerequsites: python 2.7 and curl.

Usage:
 (1) Run "sa360Api.py --login" to generate api credentials.
 (2) Manually set the generated credential to the DSAPICRED environment
     variable, or append the --cred= option to the following commands.
 (3) Run "sa360Api.py" with the flags --cred, --server, and one of --get,
     --post, or --put. For --post and --put, it reads POST body requests from
     standard input. The script then dumps the API response to standard output.
 (4) Run "sa360Api.py --logout" to invalidate the generated credential.
"""

import json
import optparse
import os
import subprocess
import sys

# The environment variable used to read credentials.
DSAPICRED_ENV = 'DSAPICRED'


def RunCommand(cmd):
  print('running command: ' + str(cmd))
  print('')
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out = p.communicate()
  return out[0]


def Login():
  """Collects tokens needed to access Search Ads 360 APIs via OAuth2.

  Interactively collect a client id, a client secret, and a refresh token for
  accessing the Search Ads 360 API. Users are asked to enter the client id
  and client secret, and walked through the web authentication process to
  generate the refresh token.

  Raises:
    ValueError: response JSON could not be parsed, or has no refresh_token.
  """
  print('')
  print('This script requires setting up a Google API project.')
  print('If you have not done so, follow these instructions:')
  print('1. Visit https://console.developers.google.com')
  print('2. Create a new project and go to "API & auth -> credentials".')
  print('4. Create an OAuth2 client ID.')
  print('5. When picking application type, choose "Installed application", '
         'type "Other".')
  print('6. Enter the cliend id and client secret below:')
  print('')
  cid = input('Client ID: ').strip()
  csc = input('Client secret: ').strip()
  print('')
  print ('Please open the following URL in the browser to authenticate. '
         'When successful, the browser will display a code. '
         'Enter the code below.')
  print('')
  print('https://accounts.google.com/o/oauth2/auth?'
         'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdoubleclicksearch'
         '&redirect_uri=urn:ietf:wg:oauth:2.0:oob'
         '&response_type=code'
         '&access_type=offline'
         '&client_id=' + cid)
  print('')
  code = input('Code: ').strip()
  print('')
  output = RunCommand(['curl', '-s', '--data',
                       'code=' + code +
                       '&client_id=' + cid +
                       '&client_secret=' + csc +
                       '&redirect_uri=urn:ietf:wg:oauth:2.0:oob' +
                       '&grant_type=authorization_code',
                       'https://accounts.google.com/o/oauth2/token'])
  json_output = json.loads(output)
  if 'refresh_token' in json_output:
    print('Login successful.')
    print( '' )
    print ('Set the following credential in the %s environment '
           'variable, or pass it in using the --cred option.' + DSAPICRED_ENV)
    print( '# DSAPI credentials: "client_id,client_secret,refresh_token"')
    print('%s="%s,%s,%s"' % (DSAPICRED_ENV, cid, csc,
                             json_output['refresh_token']))
    print('')
  else:
    raise ValueError('Missing refresh_token in response: %s' + output)


def GetDSApiCredOrDie(options):
  """Return API credentials passed into the script.

  Reads client id, client secret, and refresh token via the --cred flag or the
  DSAPICRED environment variable.

  Args:
    options: Flag values passed into the script.

  Returns:
    The credentials if found.

  Raises:
    Kills the program if no credentials are found.
  """
  if options.cred is not None:
    cred = options.cred
  elif DSAPICRED_ENV in os.environ:
    cred = os.environ[DSAPICRED_ENV].strip()
  else:
    print('Cannot find Search Ads 360 API credentials.')
    sys.exit(-1)
  return cred


def GetAccessTokenOrDie(options):
  """Generates a fresh access token using credentials passed into the script.

  Args:
    options: Flag values passed into the script.

  Returns:
    A fresh access token.

  Raises:
    ValueError: response JSON could not be parsed, or has no access_token.
  """
  cred = GetDSApiCredOrDie(options)
  [cid, csc, refresh_token] = cred.split(',')
  query_string_template = ('refresh_token=%s&client_id=%s&client_secret=%s'
                           '&grant_type=refresh_token')
  output = RunCommand(['curl', '--data',
                       query_string_template % (refresh_token, cid, csc),
                       'https://accounts.google.com/o/oauth2/token'])
  json_output = json.loads(output)
  if 'access_token' in json_output:
    return json_output['access_token']
  else:
    raise ValueError('missing access_token in response: %s' + output)


def Logout(options):
  """Revoke the refresh token passed into the script.

  Args:
    options: Flag values passed into the script.
  """
  ds3_token = GetDSApiCredOrDie(options)
  [_, _, refresh_token] = ds3_token.split(',')
  RunCommand(['curl', 'https://accounts.google.com/o/oauth2/revoke?token='
              + refresh_token])


def RunREST(options):
  """Executes a Search Ads 360 API call.

  Args:
    options: Flag values passed into the script. Used to determine credentials,
      the api URL, and whether to make a post, get or put call.

  Returns:
    The raw json returned by the API.
  """
  access_token = GetAccessTokenOrDie(options)

  if options.post:
    http_command = ['-X', 'POST', '--data', '@-']
  elif options.put:
    http_command = ['-X', 'PUT', '--data', '@-']
  else:
    http_command = ['-X', 'GET']

  output = RunCommand(['curl', '-L']
                      + http_command
                      + (['-v'] if options.verbose else [])
                      + ['-H', 'Authorization: Bearer ' + access_token,
                         '-H', 'Content-Type: application/json',
                         '-H', 'X-User-IP: 127.0.0.1',
                         options.server])
  print(output)


def Main(argv):
  """The main program.

  Calls Login, Logout or RunREST depending on the command line arguments.

  Args:
    argv: Command line arguments.
  """
  parser = optparse.OptionParser()
  parser.add_option(
      '--login', dest='login', action='store_true', default=False,
      help='Generates a refresh token that does not expire over time.')
  parser.add_option(
      '--logout', dest='logout', action='store_true', default=False,
      help='Invalidates a refresh token.')
  parser.add_option(
      '--cred', dest='cred', action='store', type='string',
      help=('Specifies the Search Ads 360 API credentials, in the format of '
            '"client_id,client_secret,refresh_token".'
            'This overrides the %s environment variable.' + DSAPICRED_ENV))
  parser.add_option(
      '--server', dest='server', action='store', type='string',
      default='https://www.googleapis.com/doubleclicksearch/v2/reports/',
      help=('The full url that specifies the Google API host, API name, '
            'API version, and API method. E.g., '
            'https://www.googleapis.com/doubleclicksearch/v2/reports/'))
  parser.add_option('--post', dest='post', action='store_true',
                    default=True,
                    help='Make a post request by reading the body from stdin')
  parser.add_option('--put', dest='put', action='store_true',
                    default=False,
                    help='Make a put request by reading the body from stdin')
  parser.add_option('--get', dest='post', action='store_false',
                    default=False,
                    help='Make a get request.')
  parser.add_option('--verbose', dest='verbose', action='store_true',
                    default=False,
                    help='Use curl verbose flag.')

  (options, _) = parser.parse_args(argv)
  if options.login:
    Login()
  elif (options.cred is None) and (DSAPICRED_ENV not in os.environ):
    print('')
    print ('Search Ads 360 API credentials not set.  Please run the script '
           'with --login to generate credentials and set it in the %s'
           'environment variable or pass in the credentials using the '
           '--cred option. ' + DSAPICRED_ENV)
    print('')
    parser.print_help()
  elif options.logout:
    Logout(options)
  else:
    RunREST(options)

if __name__ == '__main__':
  Main(sys.argv)
  