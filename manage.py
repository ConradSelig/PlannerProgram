from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1n4nkoIfEo2_jdrAfykvhABOKlznIOft_3MZXx8ntXM4'
DATA_RANGE = 'Sheet1!$A$1:$YY'


def get_db_values():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=DATA_RANGE).execute()
    values = result.get('values', [])

    return values[0], values[1:], service


def print_data(headers, values, w):

    format_string = '{:>' + str(w) + '}'

    if not values:
        print('No data found.')
    else:
        for col in headers:
            print(format_string.format(col + ":"), end="")
        print("")
        for row in values:
            for col in row:
                print(format_string.format(col), end="")
            print("")
    return


def write_cells(range, values, service):

    body = {
        "values": values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range="Sheet1!" + range,
        valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

    return


def main():
    headers, values, service = get_db_values()
    print_data(headers, values, 10)
    return


if __name__ == '__main__':
    main()
