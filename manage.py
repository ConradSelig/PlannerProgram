from __future__ import print_function
import pickle
import time
import os.path
import requests
from random import randint
from random import shuffle
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1n4nkoIfEo2_jdrAfykvhABOKlznIOft_3MZXx8ntXM4'
DATA_RANGE = 'Sheet1!$A$1:$YY'

service = ""


class Event:

    def __init__(self, title="", subtitle="", description="", text="", event_date="",
                 last_modified_date="", due_date="", in_time="", duration="", location="", attachments="", path="",
                 contacts="", number="", tags="", todo="", complete=""):
        self.attrs = ["title", "subtitle", "description", "text", "event_date", "creation_date", "last_modified_date",
                      "due_date", "time", "duration", "location", "attachments", "path", "contacts", "number", "tags",
                      "todo", "complete", "id"]
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.text = text
        self.event_date = event_date
        self.creation_date = datetime.now()
        self.last_modified_date = last_modified_date
        self.due_date = due_date
        self.time = in_time
        self.duration = duration
        self.location = location
        self.attachments = attachments
        self.path = path
        self.contacts = contacts
        self.number = number
        self.tags = tags
        self.todo = todo
        self.complete = complete
        self.id = -1

    def compare(self, other):
        local = [str(getattr(self, key)) for key in self.attrs]
        foreign = [str(getattr(other, key)) for key in self.attrs]
        return local == foreign

    def build_from_event(self, values):
        for index, key in enumerate(self.attrs):
            try:
                setattr(self, key, values[index])
            except IndexError:
                setattr(self, key, "")
        return

    def print_all(self):
        for attr in self.attrs:
            print(attr, " = ", getattr(self, attr))
        return

    def print_filled(self):
        for attr in self.attrs:
            if getattr(self, attr) != "":
                print(attr, " = ", getattr(self, attr))
        return

    def get_values(self):
        values = []
        for attr in self.attrs:
            values.append(getattr(self, attr))
        return values

    def set_id(self, new_id):
        self.id = new_id
        return

    def get(self, attr):
        return getattr(self, attr)


class HashMapValue:

    def __init__(self):
        self.key = ""
        self.values = []

    def __str__(self):
        if self.key is not "":
            return str(self.key) + ": " + str(self.values)
        else:
            return "Null: [Null]"

    def set_key(self, key):
        self.key = key

    def add_val(self, value):
        self.values.append(value)
        return

    def get_key(self):
        return self.key

    def get_values(self):
        return self.values


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

    # create the formatting string here, as it cannot be done in-place
    format_string = '{:>' + str(w) + '}'

    # if there is no data, output that
    if not values:
        print('No data found.')
    # else data exists
    else:
        # for each column of data
        for col in headers:
            # output the header row
            print(format_string.format(col + ":"), end="")
        # output newline
        print("")
        # for each line of each event
        for row in values:
            # for each column in that events data
            for col in row:
                # output with the same formatting as the header row
                print(format_string.format(col), end="")
            # output newline
            print("")
    return


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


def update_db(events, old_events):
    # for each event in events (with index/id included)
    for index, event in enumerate(events):
        # try to write the event
        try:
            # if the new version of the event is not the same as the old version
            if not event.compare(old_events[index]):
                # write that event
                write_event(index, event)
        # index error occurs when some fields are out of place
        except IndexError:
            # write the event to the database to avoid data-loss
            print("Caught by Index Error")
            write_event(index, event)

    return


def hash_string(string, table_size):
    # set the index value to 0 as a baseline
    next_map_value = 0
    # for each character in the string
    for char in string:
        # add that characters value to the total
        next_map_value += ord(char)
    # mod that value by the table size
    next_map_value %= table_size
    # return the generated hash value
    return next_map_value


def build_hash_table(items, key_name):

    print("Building Hash Table")

    table_size = len(items)
    hash_map = [HashMapValue() for _ in range(table_size)]

    # for each string in list
    for item in items:

        # get the hash value for the next key
        next_hash_value = hash_string(item.get(key_name), table_size)

        # if the hash value index is available, fill it with the data
        if hash_map[next_hash_value].get_key() == "":
            hash_map[next_hash_value].set_key(item.get(key_name))
            try:
                # append the ID, if no ID exists, a value error is thrown for invalid statement int("")
                hash_map[next_hash_value].add_val(int(item.get("id")))
            except ValueError:
                hash_map[next_hash_value].add_val(-1)
        # else check if they valid key is in that spot, and append the value to that spot
        elif hash_map[next_hash_value].get_key() == item.get(key_name):
            hash_map[next_hash_value].add_val(int(item.get("id")))
        # else an open fill is needed
        else:
            # add one to the index
            i = next_hash_value + 1
            # while i is in the table range
            while i <= table_size:
                # if reaching end of table range, reset to start of hash table
                if i >= table_size:
                    i = 0
                # if the next spot is open, fill it with the data and break from open fill
                if hash_map[i].get_key() == "":
                    hash_map[i].set_key(item.get(key_name))
                    hash_map[i].add_val(int(item.get("id")))
                    break
                # else check if the next spots key is the current key, and append the value to that spot, and break
                elif hash_map[i].get_key() == item.get(key_name):
                    hash_map[i].add_val(int(item.get("id")))
                    break
                # add one to index to check for the next spot
                i += 1

    return hash_map


def main():
    # define service as a global so it does not have to be passed into so many function definitions
    global service
    # get the database, this fills into a header array, a 2D values array, and a service API value.
    header, values, service = get_db_values()
    # output the data (formatted)
    print_data(header, values, 35)

    old_events = []
    events = []
    keys = getattr(Event(), "attrs")
    hash_map_dict = {key: [] for key in keys}

    # build new and old array, they are identical to start off with. We use this to compare which events changed at
    # save time to save API calls by only pushing changed events
    for row in values:
        events.append(Event())
        old_events.append(Event())
        events[-1].build_from_event(row)
        old_events[-1].build_from_event(row)
        if old_events[-1].get("id") != "":
            old_events[-1].set_id(int(old_events[-1].get("id")))

    for event in events:
        if event.get("id") == -1 or event.get("id") == "":
            print("Event detected with no ID, rebuilding IDs")
            for new_id, id_event in enumerate(events):
                id_event.set_id(new_id)
            break
    else:
        print("No missing IDs detected.")

    hash_map_dict["title"] = build_hash_table(events, "title")
    for index, next_hash in enumerate(hash_map_dict["title"]):
        print(index, next_hash)

    lookup_string = input("Enter Row Title: ")
    while lookup_string != "":

        key_index = hash_string(lookup_string, len(hash_map_dict["title"]))
        origin_index = key_index
        while hash_map_dict["title"][key_index].get_key() != lookup_string:
            key_index += 1
            if key_index == origin_index:
                print("No Data Found for that Entry")
                ID = -1
                break
            if key_index >= len(hash_map_dict["title"]):
                # -1 so next index tried is 0
                key_index = -1

        if ID != -1:
            for ID in hash_map_dict["title"][key_index].get_values():
                print(events[ID].print_filled())
                print("")

        lookup_string = input("Enter Row Title: ")

    '''
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
        events.append(Event(title="Test " + str(randint(0, i)),
                            todo="T" if randint(0, 1) == 1 else "F",
                            complete="T" if randint(0, 1) == 1 else "F",
                            number="" if randint(0, 2) == 1 else randint(0, 10),
                            description=words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)],
                            text=words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)] + " " + words[randint(0, len(words) - 1)],
                            duration=randint(0, 50),
                            location=locations[randint(0, len(locations) - 1)],
                            subtitle=classes[randint(0, len(classes) - 1)]
                            ))
        events[i].set_id(i)
        time.sleep(0.25)
    '''

    update_db(events, old_events)
    return


if __name__ == '__main__':
    main()
