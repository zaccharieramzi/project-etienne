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

    def get_reference_words(self):
        return self.values

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


class FirstWindow(tk.Frame):
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
        self.column_menu = None

    def column_widget_teardown(self):
        if self.column_menu is not None:
            self.column_menu.destroy()
            self.column_validation.destroy()


    def create_column_widget(self):
        self.column_widget_teardown()
        columns = self.file.get_columns()
        self.selected_column = columns[0]
        selected_column_var = tk.StringVar(self)
        selected_column_var.set(str(self.selected_column))
        def change_selected_column(*args):
            self.selected_column = [c for c in columns if str(c) == selected_column_var.get()][0]
        selected_column_var.trace("w", change_selected_column)
        self.column_menu = ttk.Combobox(self, textvariable=selected_column_var)
        self.column_menu['values'] = [str(c) for c in columns]
        self.column_menu.pack(side=tk.TOP)
        self.column_validation = tk.Button(self)
        self.column_validation['text'] = 'Validate column'
        self.column_validation['command'] = self.validate_column
        self.column_validation.pack(side=tk.TOP)

    def validate_column(self):
        self.master.destroy()
        root = tk.Tk()
        root.title("Typos checker")
        app = SecondWindow(master=root, column=self.selected_column)
        app.mainloop()

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


class SecondWindow(tk.Frame):
    def __init__(self, column, master=None):
        super().__init__(master)
        self.master = master
        self.column = column
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self,
            text=self.master.wm_title(),
            font=tkFont.Font(weight='bold'),
        )
        self.title_label.pack(side="top")
        self.reference_words = WordFrame(master=self, words=self.column.get_reference_words())
        self.closest_match = WordFrame(master=self, words=self.column.get_reference_words())
        self.typos = WordFrame(master=self, words=[])
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side=tk.BOTTOM)

class WordFrame(tk.Frame):
    def __init__(self, words, master=None):
        super().__init__(master)
        self.master = master
        self.words = words
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self,
            text="Reference words",
            font=tkFont.Font(weight='bold'),
        )
        self.title_label.pack(side="top")
        self.word_buttons = []
        for word in self.words:
            word_button = tk.Button(self, text=word, command=lambda: print(word))
            word_button.pack(side=tk.TOP)
            self.word_buttons.append(word_button)


def main():
    root = tk.Tk()
    root.title("Typos checker")
    app = FirstWindow(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
