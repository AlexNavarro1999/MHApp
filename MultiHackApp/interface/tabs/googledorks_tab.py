import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import datetime

from app.functionalities import googledorks_funct


# from interface.style import app_styles



class Googledorks(ttk.Frame):
    def __init__(self, parent, data, result_googledorks, execute_date, user_id):
        super().__init__(parent)
        self.dork_method_list = []
        self.methods_list = [method for method in dir(googledorks_funct.Googledorks) if callable(
            getattr(googledorks_funct.Googledorks, method)) and not method.startswith("__")]
        for method in self.methods_list:
            if "search_" in method:
                method_name1 = method.replace("search_", "")
                method_name2 = method_name1.replace("_", " ")
                self.dork_method_list.append(method_name2)
        self.googledorks = googledorks_funct.Googledorks(DATA=data, RESULT_GOOGLEDORKS=result_googledorks,
                                                         EXECUTE_DATE=execute_date, USER_ID=user_id)

        self.domain_regex = googledorks_funct.give_domain_regex()
        self.user_id = user_id
        # self.style = app_styles.AppStyle()

        self.combo = ttk.Combobox(parent, values=self.dork_method_list)
        self.combo.bind("<<ComboboxSelected>>", self.selection_changed)
        self.combo.grid(column=1, row=0)
        # self.combo.configure(**self.style.style.configure('My.TCombobox'))

        self.data_googledorks = tk.StringVar()
        self.data_googledorks_entry = tk.Entry(parent, textvariable=self.data_googledorks)
        self.data_googledorks_entry.grid(column=0, row=0)
        # self.data_googledorks_entry.configure(**self.style.style.configure('My.TEntry'))

        self.res_label = tk.Label(parent, text="")
        self.res_label.grid(column=2, row=0)

        self.butt_googledorks = tk.Button(parent, text="Execute googledorks", command=self.ex_but_googledorks)
        self.butt_googledorks.grid(column=0, row=1)
        # self.butt_googledorks.configure(**self.style.style.configure('My.TButton'))

        self.st_res_googledorks = st.ScrolledText(parent, width=40, height=20)
        self.st_res_googledorks.grid(column=0, row=2, padx=10, pady=10)
        # self.st_res_googledorks.configure(**self.style.style.configure('My.TScrolledText'))

    def selection_changed(self, event):
        pass

    def get_frame(self):
        return self

    def ex_but_googledorks(self):
        selected_method = self.combo.get()
        original_method_name = selected_method.replace(" ", "_")
        for method_name in dir(self.googledorks):
            method = getattr(self.googledorks, method_name)
            if callable(method) and original_method_name in method_name:
                data = self.data_googledorks_entry.get()
                data_checked = self.domain_regex(pattern=None, value=None).check_domain_pattern(value=data)
                if data_checked != True:
                    self.res_label.config(text=data_checked, fg="red")
                else:
                    self.res_label.config(text="")
                    execute_date = datetime.datetime.now()
                    user_id = self.user_id

                    result_googledorks = method(data)
                    self.googledorks.ex_googledorks(data, result_googledorks, execute_date, user_id)

                    self.st_res_googledorks.delete('1.0', tk.END)
                    if result_googledorks:
                        self.st_res_googledorks.insert(tk.END, f"Datos: {result_googledorks}")
                    else:
                        self.st_res_googledorks.insert(tk.END, "Error en el insert de los datos")
