
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import datetime

from app.functionalities import curl_funct
# from interface.style import app_styles


class Curl(ttk.Frame):
    def __init__(self, parent, data, result_curl, execute_date, user_id):
        super().__init__(parent)
        self.curl = curl_funct.Curl(DATA=data, RESULT_CURL=result_curl, EXECUTE_DATE=execute_date, USER_ID=user_id)

        self.url_regex = curl_funct.give_url_regex()
        self.user_id = user_id
        # self.style = app_styles.AppStyle()

        self.data_curl = tk.StringVar()
        self.data_curl_entry = tk.Entry(parent, textvariable=self.data_curl)
        self.data_curl_entry.grid(column=0, row=0)
        # self.data_curl_entry.configure(**self.style.style.configure('My.TEntry'))
        
        self.res_label = tk.Label(parent, text="")
        self.res_label.grid(column=2, row=0)

        self.butt_curl = tk.Button(parent, text="Execute curl",
                                                         command=self.ex_but_curl)
        self.butt_curl.grid(column=0, row=1)
        # self.butt_curl.configure(**self.style.style.configure('My.TButton'))

        self.st_res_curl = st.ScrolledText(parent, width=40, height=20)
        self.st_res_curl.grid(column=0, row=2, padx=10, pady=10)
        # self.st_res_curl.configure(**self.style.style.configure('My.TScrolledText'))

    def get_frame(self):
        return self

    def ex_but_curl(self):
        data = self.data_curl_entry.get()

        data_checked = self.url_regex(pattern=None, value=None).check_url_pattern(value=data)
        if data_checked != True:
            self.res_label.config(text=data_checked, fg="red")
        else:
            self.res_label.config(text="")
            execute_date = datetime.datetime.now()
            user_id = self.user_id

            result_curl = self.curl.get_result_curl(data)
            self.curl.ex_curl(data, result_curl, execute_date, user_id)

            self.st_res_curl.delete('1.0', tk.END)
            if result_curl:
                self.st_res_curl.insert(tk.END, f"Datos: {result_curl}")
            else:
                self.st_res_curl.insert(tk.END, "Error en el insert de los datos")
