class KeyVal:
    key = ""
    val = []

    def __init__(self, key, val):
        self.key = key
        self.val = val

    def get_key(self):
        return self.key

    def get_val(self):
        return self.val


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
    strings = [KeyVal("Calc 1", [0]),
               KeyVal("Calc 2", [1]),
               KeyVal("Calc 3", [2]),
               KeyVal("Calc 4", [7]),
               KeyVal("Tech Comm 1", [3]),
               KeyVal("CSC 215", [4]),
               KeyVal("CSC 150", [5]),
               KeyVal("CSC 215", [8]),
               KeyVal("CSC 215", [9]),
               KeyVal("CSC 251", [10]),
               KeyVal("CSC 251", [6])]

    table_size = len(strings)
    # fill the hash_map with empty arrays so index errors do not occur
    hash_map = [[] for _ in range(table_size)]

    next_map_value = 0

    # for each string in list
    for key_val in strings:

        # get the hash value for the next key
        next_map_value = hash_string(key_val.key, table_size)

        # if the hash value index is available, fill it with the data
        if len(hash_map[next_map_value]) is 0:
            hash_map[next_map_value].append([key_val.key, key_val.val])
        # else check if they valid key is in that spot, and append the value to that spot
        elif hash_map[next_map_value][0][0] is key_val.key:
            hash_map[next_map_value][0][1].append(key_val.val[0])
        # else an open fill is needed
        else:
            # add one to the index
            i = next_map_value + 1
            # while i is in the table range
            while i <= table_size:
                # if reaching end of table range, reset to start of hash table
                if i >= table_size:
                    i = 0
                # if the next spot is open, fill it with the data
                if len(hash_map[i]) is 0:
                    hash_map[i].append([key_val.key, key_val.val])
                    break
                # else check if the next spots key is the current key, and append the value to that spot
                elif hash_map[i][0][0] is key_val.key:
                    hash_map[i][0][1].append(key_val.val[0])
                    break
                # add one to index to check for the next spot
                i += 1

    print(hash_map)
    return


if __name__ == '__main__':
    main()
