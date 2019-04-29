import cht
import copy
import db_conn

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class ResizableWindow:
    def __init__(self, parent, cht):
        self.local_cht = cht

        self.parent = parent
        self.f1_style = ttk.Style()
        self.f1_style.configure('My.TFrame', background="#F0F0F0")
        self.f1 = ttk.Frame(self.parent, style='My.TFrame')
        self.f1.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.results = "Enter a query request to get results to show here."

        # buttons
        self.reload_db = ttk.Button(self.f1, text="Reload Database", cursor="hand1")
        self.save_db = ttk.Button(self.f1, text="Save Database", cursor="hand1")
        self.export_results = ttk.Button(self.f1, text="Export Results", cursor="hand1")
        self.clear_selection = ttk.Button(self.f1, text="Clear Selection", cursor="hand1")
        self.show_cols = ttk.Button(self.f1, text="Show Column Headers", cursor="hand1")
        self.add_row = ttk.Button(self.f1, text="Add New Note", cursor="hand1")
        self.search = ttk.Button(self.f1, text="Search", cursor="hand1", command=self.run_search)
        self.cancel = ttk.Button(self.f1, text="Cancel", cursor="hand1")

        # labels
        self.lbl_selection_options = ttk.Label(self.f1, text="\tSelection Options:")
        self.lbl_max_results = ttk.Label(self.f1, text="Max Results:")
        self.lbl_search_terms = ttk.Label(self.f1, text="Search Terms:")
        self.lbl_TEMP = ttk.Label(self.f1, text="THIS IS A PLACEHOLDER FOR\nCOLUMN SELECTION.")

        # check boxes
        self.manual_entry = ttk.Checkbutton(self.f1, text="Select Columns by Hand")
        self.scan_all = ttk.Checkbutton(self.f1, text="Scan all of the Data")

        # entry fields
        self.options_limit = ttk.Entry(self.f1)
        self.search_terms = ttk.Entry(self.f1)

        # grid building
        # buttons
        self.reload_db.grid(column=0, row=0, columnspan=2, sticky="nsew")
        self.save_db.grid(column=2, row=0, columnspan=2, sticky="nsew")
        self.export_results.grid(column=4, row=0, columnspan=2, sticky="nsew")
        self.clear_selection.grid(column=6, row=0, columnspan=2, sticky="nsew")
        self.show_cols.grid(column=8, row=0, columnspan=2, sticky="nsew")
        self.add_row.grid(column=10, row=0, columnspan=2, sticky="nsew")
        self.search.grid(column=12, row=8, columnspan=2, sticky="", padx=(20, 20))
        self.cancel.grid(column=15, row=8, columnspan=2, sticky="e", padx=(20, 20))

        # labels
        self.lbl_selection_options.grid(column=12, row=0, columnspan=4, sticky="nsew")
        self.lbl_max_results.grid(column=12, row=5, columnspan=2, sticky="nsew")
        self.lbl_search_terms.grid(column=12, row=6, columnspan=4, sticky="nsew")
        self.lbl_TEMP.grid(column=12, row=3, columnspan=4, rowspan=2, sticky="nsew")

        # check boxes
        self.manual_entry.grid(column=12, row=1, columnspan=4, sticky="nsew")
        self.scan_all.grid(column=12, row=2, columnspan=4, sticky="nsew")

        # entry field
        self.options_limit.grid(column=15, row=5, columnspan=1, sticky="ew", padx=(0, 20))
        self.search_terms.grid(column=12, row=7, columnspan=4, sticky="nsew", pady=(0, 20), padx=(20, 20))

        self.xscrollbar = tk.Scrollbar(self.f1, orient=tk.HORIZONTAL)
        self.yscrollbar = tk.Scrollbar(self.f1, orient=tk.VERTICAL)
        self.results_window = tk.Text(self.f1, wrap=tk.NONE, xscrollcommand=self.xscrollbar.set,
                                      yscrollcommand=self.yscrollbar.set, state=tk.NORMAL)
        self.xscrollbar.config(command=self.results_window.xview)
        self.yscrollbar.config(command=self.results_window.yview)

        self.xscrollbar.grid(column=0, row=8, columnspan=11, sticky=(tk.E+tk.W))
        self.yscrollbar.grid(column=11, row=1, rowspan=7, sticky=(tk.N+tk.S))
        self.results_window.grid(column=0, row=1, columnspan=11, rowspan=7)

        self.results_window.insert(tk.END, self.results)

    def update_results_window(self):
        self.results_window.delete("1.0", tk.END)
        self.results_window.insert(tk.END, self.results)
        return

    def run_search(self):
        self.results = ""
        w = 35
        format_string = '{:>' + str(w) + '}'

        for key in [attr for attr in self.local_cht.get_keys() if "__" not in attr]:
            self.results += format_string.format(key.title() + ":")
        self.results += "\n"

        lookup_key = self.search_terms.get()
        for row in cht.hashing.lookup_hash("__words__", lookup_key, self.local_cht.get_map()):
            self.results += self.local_cht[row].get_csv_list(w) + "     \n"
        self.update_results_window()
        return


def main():
    # define service as a global so it does not have to be passed into so many function definitions
    global service
    # get the database, this fills into a header array, a 2D values array, and a service API value.
    header, values, service = db_conn.get_db_values()
    local_cht = cht.classes.CHT(header, values)

    # build new and old array, they are identical to start off with. We use this to compare which events changed at
    # save time to save API calls by only pushing changed events

    print("Starting Hash... (Start Time = ~" + str(datetime.now()) + ")")

    start_time = datetime.now()
    local_cht.add_rows(values, show_print=False)
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

    root = tk.Tk()
    rw = ResizableWindow(root, local_cht)
    root.mainloop()


if __name__ == '__main__':
    main()
