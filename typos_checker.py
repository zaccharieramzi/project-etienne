from pathlib import Path

import pandas as pd

class ExcelFile:
    def __init__(self, filename):
        self.path = Path(filename)
        self.df = pd.read_excel(self.path, engine='openpyxl')

    def get_columns(self):
        columns = [
            ExcelColumn(name, values)
            for name, values in self.df.iteritems()
        ]
        return columns

class ExcelColumn:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

class ReferenceWord:
    def __init__(self, word):
        self.word = word
        self.min_similarity_fully_checked = 1.0

    def is_fully_checked_for_sim(self, sim):
        return sim >= self.min_similarity_fully_checked


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self,
            text=self.master.wm_title(),
            font=tkFont.Font(weight='bold'),
        )
        self.title_label.pack(side="top")
        self.browse = tk.Button(self)
        self.browse["text"] = "Browse files"
        self.browse["command"] = self.browse_files
        self.browse.pack(side="top")

        self.file_label = tk.Label(
            self,
            text="No file selected",
        )
        self.file_label.pack(side=tk.TOP)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side=tk.BOTTOM)


    def create_column_widget(self):
        columns = self.file.get_columns()
        selected_column_var = tk.StringVar(self)
        selected_column_var.set(str(columns[0]))
        def change_selected_column(*args):
            print(selected_column_var.get())
        selected_column_var.trace("w", change_selected_column)
        self.column_menu = ttk.Combobox(self, textvariable=selected_column_var)
        self.column_menu['values'] = [str(c) for c in columns]
        self.column_menu.pack(side=tk.TOP)
        self.column_validation = tk.Button(self)
        self.column_validation['text'] = 'Validate column'
        self.column_validation['command'] = self.say_hi
        self.column_validation.pack(side=tk.TOP)

    def say_hi(self):
        print("hi there, everyone!")

    def browse_files(self):
        filename = filedialog.askopenfilename(
            initialdir="~",
            title="Select a File",
            filetypes=(("Excel files", "*.xlsx*"),),
        )
        if filename:
            self.file_label["text"] = f'File selected: {filename}'
            self.file = ExcelFile(filename)
            self.create_column_widget()


def main():
    root = tk.Tk()
    root.title("Typos checker")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
