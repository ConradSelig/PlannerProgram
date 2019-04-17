from datetime import datetime


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
