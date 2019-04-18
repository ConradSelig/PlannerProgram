from datetime import datetime


class CHT:

    def __init__(self, keys, values):
        self.keys = keys
        self.raw_values = values
        self.rows = []
        self.hash_map_dict = {key: [] for key in keys}

    def __getitem__(self, key):
        return self.hash_map_dict[key]

    def __get__(self, instance, owner):
        return self.owner

    def __setitem__(self, key, value):
        self.hash_map_dict[key] = value
        return

    def __len__(self):
        return len(self.hash_map_dict)

    def append(self, row):
        temp_row = Row(self.keys)
        temp_row.build_from_event(row)
        self.rows.append(temp_row)
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
