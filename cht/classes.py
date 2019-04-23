from datetime import datetime
from cht import hashing
from cht import output
import re


class CHT:

    def __init__(self, keys, values):
        self.keys = keys + ["__words__"]
        self.raw_values = values
        self.rows = []
        self.words = []
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

    def __dir__(self):
        return self.keys

    def add_row(self, row, do_hash=True, show_print=True):
        self.add_rows([row], do_hash, show_print)
        return

    def add_rows(self, rows, do_hash=True, show_print=True):
        for row in rows:
            temp_row = Row(self.keys)
            temp_row.build_from_event(row)
            self.rows.append(temp_row)
            for new_word in temp_row.get_words():
                self.words.append(Word(new_word, temp_row.get("id")))
        for row in self.rows:
            if row.get("id") == -1 or row.get("id") == "":
                for new_id, id_row in enumerate(self.rows):
                    id_row.set_id(new_id)
                break
        if do_hash:
            if show_print:
                print("Building Cubic Hash Table...")
            for i, key in enumerate(self.keys):
                if show_print:
                    output.progress_bar(i, len(self.keys))
                self.hash_map_dict[key] = hashing.build_hash_table(self, key)
            if show_print:
                output.progress_bar(len(self.keys), len(self.keys))

        return

    def get_map(self):
        return self.hash_map_dict

    def get_efficiency(self):
        big_o = 0  # Worst
        omega = ""  # Best
        theta = 0  # Average
        total_hashed_lists = 0
        total_hashed_words = 0

        for key in self.keys:
            for hash_map_val in self.hash_map_dict[key]:
                if len(hash_map_val.values) > big_o:
                    big_o = len(hash_map_val.values)
                if isinstance(omega, str) or (len(hash_map_val.values) < omega and len(hash_map_val.values) != 0):
                    omega = len(hash_map_val.values)

        for hash_map_val in self.hash_map_dict["__words__"]:
            if len(hash_map_val.values) > 0:
                total_hashed_lists += 1
                total_hashed_words += len(hash_map_val.values)

        theta = total_hashed_words / total_hashed_lists

        return big_o, omega, theta


class Word:

    def __init__(self, word, word_id):
        self.word = word
        self.id = word_id

    def get(self, attr):
        if attr == "id":
            return self.id
        return self.word


class Row:

    def __init__(self, attrs):
        self.attrs = attrs
        for key in attrs:
            setattr(self, key, "")
        self.id = -1

    def __dir__(self):
        return self.attrs

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

    def get_words(self):
        words = ""
        for attr in self.attrs:
            words += str(getattr(self, attr)) + " "
        words = re.sub("[!\"#$%&'()*+,\\-./:;<=>?@[\\]^_`{|}~]", "", words)
        return words.split()


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
