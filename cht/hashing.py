from cht import classes


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
    hash_map = [classes.HashMapValue() for _ in range(table_size)]

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
