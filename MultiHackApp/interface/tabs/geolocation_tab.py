
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import datetime

from app.functionalities import geolocation_funct
# from interface.style import app_styles


class Geolocation(ttk.Frame):
    def __init__(self, parent, data, result_geolocation, execute_date, user_id):
        super().__init__(parent)
        self.geolocation = geolocation_funct.Geolocation(DATA=data, RESULT_GEOLOCATION=result_geolocation,
                                                         EXECUTE_DATE=execute_date, USER_ID=user_id)

        self.ip_regex = geolocation_funct.give_ip_regex()
        self.user_id = user_id
        # self.style = app_styles.AppStyle()

        self.data_geolocation = tk.StringVar()
        self.data_geolocation_entry = tk.Entry(parent, textvariable=self.data_geolocation)
        self.data_geolocation_entry.grid(column=0, row=0)
        # self.data_geolocation_entry.configure(**self.style.style.configure('My.TEntry'))
        
        self.res_label = tk.Label(parent, text="")
        self.res_label.grid(column=2, row=0)

        self.butt_geolocation = tk.Button(parent, text="Execute geolocation",
                                                         command=self.ex_but_geolocation)
        self.butt_geolocation.grid(column=0, row=1)
        # self.butt_geolocation.configure(**self.style.style.configure('My.TButton'))

        self.st_res_geolocation = st.ScrolledText(parent, width=40, height=20)
        self.st_res_geolocation.grid(column=0, row=2, padx=10, pady=10)
        # self.st_res_geolocation.configure(**self.style.style.configure('My.TScrolledText'))

    def get_frame(self):
        return self

    def ex_but_geolocation(self):
        data = self.data_geolocation_entry.get()

        data_checked = self.ip_regex(pattern=None, value=None).check_ip_pattern(value=data)
        if data_checked != True:
            self.res_label.config(text=data_checked, fg="red")
        else:
            execute_date = datetime.datetime.now()
            user_id = self.user_id

            result_geolocation = self.geolocation.get_result_geolocation(data)
            self.geolocation.ex_geolocation(data, result_geolocation, execute_date, user_id)

            self.st_res_geolocation.delete('1.0', tk.END)
            if result_geolocation:
                self.st_res_geolocation.insert(tk.END, f"Datos: {result_geolocation}")
            else:
                self.st_res_geolocation.insert(tk.END, "Error en el insert de los datos")
