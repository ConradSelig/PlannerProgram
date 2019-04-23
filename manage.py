from __future__ import print_function

import cht
import time
import copy
import pickle
import os.path
import requests
from random import randint
from random import shuffle
from datetime import datetime
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1n4nkoIfEo2_jdrAfykvhABOKlznIOft_3MZXx8ntXM4'
DATA_RANGE = 'Sheet1!$A$1:$YY'

service = ""


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


def write_cells(db_range, values):

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


def write_event(event_index, event):
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


def update_db(local_cht, old_local_cht):
    old_local_cht_row = ""
    # for each event in events (with index/id included)
    for index, event in enumerate(local_cht.rows):
        # try to write the event
        try:
            # if the new version of the event is not the same as the old version
            if not event.compare(old_local_cht.rows[index]):
                # write that event
                write_event(index, event)
        # index error occurs when some fields are out of place
        except IndexError or AttributeError:
            # write the event to the database to avoid data-loss
            write_event(index, event)

    return


def get_new_row_vals(attrs):
    values = []
    for attr in attrs:
        if "__" not in attr:
            next_val = input("Enter value for " + attr.title() + " or ' ' for no value: ")
            if next_val == " ":
                next_val = ""
            values.append(next_val)
    return values


def main():
    # define service as a global so it does not have to be passed into so many function definitions
    global service
    # get the database, this fills into a header array, a 2D values array, and a service API value.
    header, values, service = get_db_values()
    local_cht = cht.classes.CHT(header, values)
    # output the data (formatted)
    cht.output.print_table_data(local_cht, 35)

    # build new and old array, they are identical to start off with. We use this to compare which events changed at
    # save time to save API calls by only pushing changed events

    print("Starting Hash... (Start Time = ~" + str(datetime) + ")")

    start_time = datetime.now()
    local_cht.add_rows(values)
    end_time = datetime.now()

    duration = end_time - start_time
    print("Hash Complete. (End Time = " + str(end_time) + ")")
    print("Time hash took to complete: " + str(duration))
    print("Words Hashed:", len(local_cht.words))
    big_o, omega, theta = local_cht.get_efficiency()
    print("Cubic Hash Table Efficiency: ")
    print("\tO(" + str(big_o) + ") <- Worst")
    print("\tΩ(" + str(omega) + ") <- Best")
    print("\tΘ(" + str(round(theta, 2)) + ") <- Average")

    old_local_cht = copy.deepcopy(local_cht)

    print("Keys: ", local_cht.keys)
    while True:
        lookup_key = input("Enter Key to Begin Lookup or type ADD to add a row: ").lower()
        if lookup_key == "":
            lookup_key = "__words__"
        if lookup_key == "add":
            # local_cht.add_row(get_new_row_vals(local_cht.keys))
            local_cht.add_row(["Custom Title", "Data Structures", "Some New Values", "Totally Original Words", "", "", "", "", "", "42", "Placer", "", "", "", "0", "", "T", "F", ""])
        else:
            break
    lookup_string = input("Enter Row Title: ")
    while lookup_key != "" and lookup_string != "":

        for row in cht.hashing.lookup_hash(lookup_key, lookup_string, local_cht.get_map()):
            print("\n\n")
            local_cht[row].print_filled()

        print("Keys: ", local_cht.keys)
        while True:
            lookup_key = input("Enter Key to Begin Lookup or type ADD to add a row: ").lower()
            if lookup_key == "":
                lookup_key = "__words__"
            if lookup_key == "add":
                # local_cht.add_row(get_new_row_vals(local_cht.keys))
                local_cht.add_row(["Custom Title", "Data Structures", "Some New Values", "Totally Original Words", "", "", "", "", "", "42", "Placer", "", "", "", "0", "", "T", "F", ""])
            else:
                break
        lookup_string = input("Enter Row Title: ")


    print("Getting Words...")
    words_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = requests.get(words_url)
    words = response.content.splitlines()
    words = [b.decode("utf-8") for b in words]

    classes = ["Calc 1", "Calc 2", "Calc 2", "Tech Comm 1", "Tech Comm 2", "CSC 150", "CSC 215", "CSC 251"]
    locations = ["CB", "CM", "EEP", "Paleo", "CBEC", "MI", "McLaury"]

    # fill with 100 semi-random events
    for i in range(100):
        print("Building Next Event...", i + 1)
        local_cht.add_row(["Test " + str(randint(0, i)),
                           classes[randint(0, len(classes) - 1)],
                           words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)],
                           words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)],
                           "", "", "", "", "", randint(0, 50), locations[randint(0, len(locations) - 1)], "", "", "",
                           "" if randint(0, 2) == 1 else randint(0, 10), "", "T" if randint(0, 1) == 1 else "F",
                           "T" if randint(0, 1) == 1 else "F", -1], do_hash=False)
        time.sleep(0.25)

    local_cht.do_hash()

    update_db(local_cht, old_local_cht)
    return


if __name__ == '__main__':
    main()

'''
attrs = ["title", "subtitle", "description", "text", "event_date", "creation_date", "last_modified_date",
                       "due_date", "time", "duration", "location", "attachments", "path", "contacts", "number", "tags",
                       "todo", "complete", "id"]
'''
