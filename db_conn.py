import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
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


def write_cells(db_range, values, service):

    # body is a dictionary used by the Google Sheets API and must be formatted like this
    body = {
        "values": values
    }
    # call the API and write the values to the specified range
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range="Sheet1!" + db_range,
        valueInputOption='RAW', body=body).execute()
    # print how many cells were updated in the process
    print('{0} cells updated.'.format(result.get('updatedCells')))

    return


def write_event(event_index, event, service):
    # set the creation date of the event being writen to the string version of the creation date
    setattr(event, "creation_date", str(getattr(event, "creation_date")))
    # body is a dictionary used by the Google Sheets API and must be formatted like this
    body = {
        "values": [event.get_values()]
    }
    # build the cell range to write the event to
    cell_range = "A" + str(event_index + 2) + ":S" + str(event_index + 2)
    # call the API and write the values to the specified range
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range="Sheet1!" + cell_range,
        valueInputOption='RAW', body=body).execute()
    # print out which event was updated
    print("Event Updated: ID = " + str(event.get("id")))
    return


def update_db(local_cht, old_local_cht, service):
    old_local_cht_row = ""
    # for each event in events (with index/id included)
    for index, event in enumerate(local_cht.rows):
        # try to write the event
        try:
            # if the new version of the event is not the same as the old version
            if not event.compare(old_local_cht.rows[index]):
                # write that event
                write_event(index, event, service)
        # index error occurs when some fields are out of place
        except IndexError or AttributeError:
            # write the event to the database to avoid data-loss
            write_event(index, event, service)

    return