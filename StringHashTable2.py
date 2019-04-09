class Event:

    def __init__(self, title, section, random):
        self.title = title
        self.section = section
        self.ID = 0
        self.random = random

    def __str__(self):
        return str(self.title) + " " + str(self.section) + ", " + str(self.random)

    def set_id(self, ID):
        self.ID = ID

    def get_title(self):
        return self.title

    def get_section(self):
        return self.section

    def get_id(self):
        return self.ID


class HashMapValue:

    def __init__(self):
        self.title = ""
        self.values = []

    def __str__(self):
        if self.title is not "":
            return str(self.title) + ": " + str(self.values)
        else:
            return "Null: [Null]"

    def set_title(self, title):
        self.title = title

    def add_val(self, value):
        self.values.append(value)
        return

    def get_title(self):
        return self.title

    def get_values(self):
        return self.values


def hash_string(string, table_size):
    next_map_value = 0
    # for each character in the string
    for char in string:
        # add that characters value to the total
        next_map_value += ord(char)
    # mod that value by the table size
    next_map_value %= table_size
    # return the generated hash value
    return next_map_value


def main():

    event_list = [Event("Calc", 1, "Not the Best"),
                  Event("Calc", 1, "But I did pass"),
                  Event("Calc", 2, "Is quite difficult"),
                  Event("Calc", 2, "Who knows what will happen"),
                  Event("CSC", 215, "An interesting class"),
                  Event("CSC", 215, "(Finally)"),
                  Event("CSC", 251, "Worst class I've taken since middle school."),
                  Event("Tech Comm", 1, "Boooooring"),
                  Event("Tech Comm", 2, "Pretty much the same thing just a second time.")]
    for index, event in enumerate(event_list):
        event.set_id(index)
    table_size = len(event_list)
    hash_map = [HashMapValue() for _ in range(table_size)]

    # for each string in list
    for event in event_list:

        # get the hash value for the next key
        next_hash_value = hash_string(event.get_title(), table_size)

        # if the hash value index is available, fill it with the data
        if hash_map[next_hash_value].get_title() == "":
            hash_map[next_hash_value].set_title(event.get_title())
            hash_map[next_hash_value].add_val(event.ID)
        # else check if they valid key is in that spot, and append the value to that spot
        elif hash_map[next_hash_value].get_title() == event.get_title():
            hash_map[next_hash_value].add_val(event.ID)
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
                if hash_map[i].get_title() == "":
                    hash_map[i].set_title(event.get_title())
                    hash_map[i].add_val(event.ID)
                    break
                # else check if the next spots key is the current key, and append the value to that spot, and break
                elif hash_map[i].get_title() == event.get_title():
                    hash_map[i].add_val(event.ID)
                    break
                # add one to index to check for the next spot
                i += 1

    for next_hash in hash_map:
        print(next_hash)

    lookup_string = input("Enter Class Title: ")
    key_hash = hash_string(lookup_string, table_size)
    for ID in hash_map[key_hash].get_values():
        print(event_list[ID])

    return


if __name__ == '__main__':
    main()
