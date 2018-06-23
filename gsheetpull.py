from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import os
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags.noauth_local_webserver = True
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/appsactivity-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
APPLICATION_NAME = 'showtime3'


cwd = os.getcwd()
dirlist = os.listdir(cwd)
foundpath = False
foundfile = False
for i in dirlist:
    if 'client_secret_' in i:
        with open(i, 'r') as f:
            client_secret_pathname = f.readline().rstrip()
        foundpath = True
if foundpath:
    dirlist2 = os.listdir(client_secret_pathname)
    for i in dirlist2:
        if 'client_secret_' in i:
            CLIENT_SECRET_FILE = client_secret_pathname + i
            foundfile = True
if not foundfile:
    CLIENT_SECRET_FILE = 'client_secret_12345'

found_sheets = False
for i in dirlist2:
    if 'sheet' in i:
        sheetid = i
        found_sheets = True

abssheetid = client_secret_pathname + sheetid
with open(abssheetid) as s:
    sheetnames = json.load(s)

master_list_sheet = sheetnames['master_list_sheet']
tester_list_sheet = sheetnames['tester_list_sheet']


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'appsactivity-python-showtime.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        print('Storing credentials to ' + credential_path)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def sheetpull():
    credentials = get_credentials()
    print ('Credential get: ', credentials)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    spreadsheet_id = master_list_sheet
    rangeName = 'A2:C'
    result = service.spreadsheets().values().get \
        (spreadsheetId=spreadsheet_id, range=rangeName).execute()
    values = result.get('values', [])
    return (values)


def sheetpush(tracks, path):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    if path == 'live':
        spreadsheet_id = master_list_sheet
        sheetname = 'Master List'
    else:
        spreadsheet_id = tester_list_sheet
        sheetname = 'Tester'

    range_name = 'Sheet1'
    values = tracks
    body = {
        'values': values
    }
    value_input_option = 'RAW'

    result = list(service.spreadsheets().values()).append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print(('Pushed songs to {0}'.format(sheetname)))

    return (values)

def sheetquery(month_name, path):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    if path == 'live':
        spreadsheet_id = master_list_sheet
    else:
        spreadsheet_id = tester_list_sheet

    rangeName = 'C2:C'
    result = list(service.spreadsheets().values()).get \
        (spreadsheetId=spreadsheet_id, range=rangeName).execute()
    values = result.get('values', [])
    for i in values:
        if month_name in i:
            return True
    return False

if __name__ == "__main__":
    print ('\n\n\n')
    get_credentials()
    a = sheetpull()
    print (len(a))
