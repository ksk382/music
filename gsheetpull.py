from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import os


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
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

APPLICATION_NAME = 'Google Sheets API Python Quickstart'

flags = None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    print ('credential_dir: ', credential_dir)
    if not os.path.exists(credential_dir):
        print ('making credential_dir')
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')
    print ('Credential path exists: ', os.path.exists(credential_path))

    #if not os.path.exists(credential_path):
    #    os.makedirs(credential_path)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        print(('Storing credentials to ' + credential_path))

    return credentials

def sheetpull():
    credentials = get_credentials()
    print ('Credential get: ', credentials)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    spreadsheet_id = '1VF5G3eGW_X4EuDb3r_3_KWRc4vv7c_0w081wXqpEMQo'
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
        spreadsheet_id = '1VF5G3eGW_X4EuDb3r_3_KWRc4vv7c_0w081wXqpEMQo'
        sheetname = 'Master List'
    else:
        spreadsheet_id = '1qAiAQuXlFWEIJUnUgODjdCPPikmrryil1elSYtPCHME'
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
        spreadsheet_id = '1VF5G3eGW_X4EuDb3r_3_KWRc4vv7c_0w081wXqpEMQo'
    else:
        spreadsheet_id = '1qAiAQuXlFWEIJUnUgODjdCPPikmrryil1elSYtPCHME'

    rangeName = 'C2:C'
    result = list(service.spreadsheets().values()).get \
        (spreadsheetId=spreadsheet_id, range=rangeName).execute()
    values = result.get('values', [])
    for i in values:
        if month_name in i:
            return True
    return False

if __name__ == "__main__":
    get_credentials()
    sheetpull()
