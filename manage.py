from __future__ import print_function

import cht
import time
import copy
import pickle
import os.path
import db_conn
import requests
from random import randint
from random import shuffle
from datetime import datetime


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
    header, values, service = db_conn.get_db_values()
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

    db_conn.update_db(local_cht, old_local_cht)
    return


if __name__ == '__main__':
    main()

'''
attrs = ["title", "subtitle", "description", "text", "event_date", "creation_date", "last_modified_date",
                       "due_date", "time", "duration", "location", "attachments", "path", "contacts", "number", "tags",
                       "todo", "complete", "id"]
'''
