import re
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
        self.clear = ttk.Button(self.f1, text="Clear", cursor="hand1", command=self.clear_all)

        # labels
        self.lbl_selection_options = ttk.Label(self.f1, text="\tSelection Options:")
        self.lbl_max_results = ttk.Label(self.f1, text="Max Results:")
        self.lbl_search_terms = ttk.Label(self.f1, text="Search Terms:")
        self.lbl_TEMP = ttk.Label(self.f1, text="THIS IS A PLACEHOLDER FOR\nCOLUMN SELECTION.")

        # check boxes
        self.manual_entry_value = tk.IntVar()
        self.manual_entry_value.set(0)
        self.scan_all_value = tk.IntVar()
        self.scan_all_value.set(0)
        self.add_mode_value = tk.IntVar()
        self.add_mode_value.set(0)
        self.manual_entry = ttk.Checkbutton(self.f1, text="Select Columns by Hand", cursor="hand1",
                                            variable=self.manual_entry_value)
        self.scan_all = ttk.Checkbutton(self.f1, text="Scan all of the Data", cursor="hand1",
                                        variable=self.scan_all_value)
        self.add_mode = ttk.Checkbutton(self.f1, text="Use Additive Searching", cursor="hand1",
                                        variable=self.add_mode_value)

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
        self.search.grid(column=12, row=9, columnspan=2, sticky="", padx=(20, 20))
        self.clear.grid(column=15, row=9, columnspan=2, sticky="e", padx=(20, 20))

        # labels
        self.lbl_selection_options.grid(column=12, row=0, columnspan=4, sticky="nsew")
        self.lbl_max_results.grid(column=12, row=5, columnspan=2, sticky="nsew")
        self.lbl_search_terms.grid(column=12, row=6, columnspan=4, sticky="nsew")
        self.lbl_TEMP.grid(column=12, row=3, columnspan=4, rowspan=2, sticky="nsew")

        # check boxes
        self.manual_entry.grid(column=12, row=1, columnspan=4, sticky="nsew")
        self.scan_all.grid(column=12, row=2, columnspan=4, sticky="nsew")
        self.add_mode.grid(column=12, row=7, columnspan=4, sticky="nsew")

        # entry field
        self.options_limit.grid(column=15, row=5, columnspan=1, sticky="ew", padx=(0, 20))
        self.search_terms.grid(column=12, row=8, columnspan=4, sticky="nsew", pady=(0, 20), padx=(20, 20))

        self.xscrollbar = tk.Scrollbar(self.f1, orient=tk.HORIZONTAL)
        self.yscrollbar = tk.Scrollbar(self.f1, orient=tk.VERTICAL)
        self.results_window = tk.Text(self.f1, wrap=tk.NONE, xscrollcommand=self.xscrollbar.set,
                                      yscrollcommand=self.yscrollbar.set, state=tk.NORMAL)
        self.xscrollbar.config(command=self.results_window.xview)
        self.yscrollbar.config(command=self.results_window.yview)

        self.xscrollbar.grid(column=0, row=9, columnspan=11, sticky=(tk.E+tk.W))
        self.yscrollbar.grid(column=11, row=1, rowspan=8, sticky=(tk.N+tk.S))
        self.results_window.grid(column=0, row=1, columnspan=11, rowspan=8)

        self.results_window.insert(tk.END, self.results)

    def update_results_window(self):
        self.results_window.delete("1.0", tk.END)
        self.results_window.insert(tk.END, self.results)
        return

    def clear_all(self):
        self.results = "Enter a query request to get results to show here."
        self.search_terms.delete(0, "end")
        self.manual_entry_value.set(0)
        self.scan_all_value.set(0)
        self.add_mode_value.set(0)

        self.update_results_window()

    def run_search(self):
        local_results = []
        new_local_results = []
        self.results = ""

        w = 35
        format_string = '{:>' + str(w) + '}'

        # add header row to results string
        for key in [attr for attr in self.local_cht.get_keys() if "__" not in attr]:
            self.results += format_string.format(key.title() + ":")
        self.results += "\n"

        lookup_keys = self.search_terms.get()
        lookup_keys = lookup_keys.split(",")

        if self.add_mode_value.get() == 1:  # additive search mode
            for lookup_key in lookup_keys:
                for row in cht.hashing.lookup_hash("__words__", lookup_key, self.local_cht.get_map()):
                    local_results.append(self.local_cht[row].get_csv_list(w) + "     \n")

            try:
                max_results = int(self.options_limit.get())
            except ValueError:
                max_results = len(local_results) + 1

            print(local_results)
            print(max_results)

            for result in local_results:
                if result not in new_local_results and len(new_local_results) < max_results:
                    new_local_results.append(result)

            for result in new_local_results:
                self.results += result

        else:  # intersective search mode

            # block appends all results from each key into a 2D list
            for lookup_key in lookup_keys:
                next_keys_vals = []
                for row in cht.hashing.lookup_hash("__words__", lookup_key, self.local_cht.get_map()):
                    next_keys_vals.append(self.local_cht[row].get_csv_list(w) + "     \n")
                local_results.append(next_keys_vals)

            # block checks to make sure if each result is in all result rows
            check_list = []
            new_local_results = []
            for result in local_results[0]:
                check_list = []
                for row in local_results[1:]:
                    check_list.append(False)
                    for item in row:
                        if item == result:
                            check_list[-1] = True
                if all(check_list):
                    new_local_results.append(result)

            # block only allows for the options_limit (or all if no limit)
            for index, result in enumerate(new_local_results):
                if str.isdigit(self.options_limit.get()):
                    if index < self.options_limit.get():
                        self.results += result
                else:
                    self.results += result

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
