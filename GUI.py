import tkinter as tk
from tkinter import ttk


class ResizableWindow:
    def __init__(self, parent):
        self.parent = parent
        self.f1_style = ttk.Style()
        self.f1_style.configure('My.TFrame', background='#334353')
        self.f1 = ttk.Frame(self.parent, style='My.TFrame')

        self.temp_var = 0

        self.f1.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))  # added sticky
        self.namelbl = ttk.Label(self.f1, text="Simple Adder\nNewline Test")
        self.value_label = ttk.Label(self.f1, text=self.temp_var, width=10, anchor=tk.CENTER)
        self.add_field = ttk.Entry(self.f1)

        self.add = ttk.Button(self.f1, text="Add", command=self.add_var, cursor="hand1")
        self.exit = ttk.Button(self.f1, text="Exit", command=parent.destroy, cursor="hand1")

        self.f1.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))  # added sticky
        self.namelbl.grid(column=0, row=0, columnspan=4, sticky=tk.N)  # added sticky, padx
        self.add_field.grid(column=0, row=1, columnspan=2, sticky=tk.W)  # added sticky, pady, padx
        self.value_label.grid(column=2, row=1, columnspan=2, sticky=tk.E)
        self.add.grid(column=0, row=2, columnspan=2, sticky=(tk.S, tk.W))
        self.exit.grid(column=2, row=2, columnspan=2, sticky=(tk.S, tk.E))

        # added resizing configs
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.f1.columnconfigure(0, weight=3)
        self.f1.columnconfigure(1, weight=3)
        self.f1.columnconfigure(2, weight=3)
        self.f1.columnconfigure(3, weight=1)
        self.f1.columnconfigure(4, weight=1)
        self.f1.rowconfigure(1, weight=1)

    def add_var(self):
        self.temp_var += int(self.add_field.get())
        self.value_label.configure(text=str(self.temp_var))
        print(self.temp_var)
        return


def main():
    root = tk.Tk()
    rw = ResizableWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
