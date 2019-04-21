from datetime import datetime
from cht import hashing
from cht import output


class CHT:

    def __init__(self, keys, values):
        self.keys = keys
        self.raw_values = values
        self.rows = []
        self.hash_map_dict = {key: [] for key in keys}

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.rows[key]
        return self.hash_map_dict[key]

    def __setitem__(self, key, value):
        self.hash_map_dict[key] = value
        return

    def __len__(self):
        return len(self.rows)

    def add_row(self, row, hash=True, show_print=True):
        self.add_rows([row], hash, show_print)
        return

    def add_rows(self, rows, hash=True, show_print=True):
        for row in rows:
            temp_row = Row(self.keys)
            temp_row.build_from_event(row)
            self.rows.append(temp_row)
        for row in self.rows:
            if row.get("id") == -1 or row.get("id") == "":
                for new_id, id_row in enumerate(self.rows):
                    id_row.set_id(new_id)
                break
        if hash:
            if show_print:
                print("Building Cubic Hash Table...")
            for i, key in enumerate(self.keys):
                if show_print:
                    output.progress_bar(i, len(self.keys) - 1)
                self.hash_map_dict[key] = hashing.build_hash_table(self, key)
        return

    def get_map(self):
        return self.hash_map_dict


class Row:

    def __init__(self, attrs):
        self.attrs = attrs
        for key in attrs:
            setattr(self, key, "")
        self.id = -1

    def compare(self, other):
        local = [str(getattr(self, key)) for key in self.attrs]
        foreign = [str(getattr(other, key)) for key in self.attrs]
        return local == foreign

    def build_from_event(self, values):
        for index, key in enumerate(self.attrs):
            try:
                if key == "id":
                    setattr(self, key, int(values[index]))
                else:
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
