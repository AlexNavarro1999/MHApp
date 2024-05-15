
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import datetime

from app.functionalities import socialmedia_funct
# from interface.style import app_styles


class Socialmedia(ttk.Frame):
    def __init__(self, parent, data, result_socialmedia, execute_date, user_id):
        super().__init__(parent)
        self.socialmedia = socialmedia_funct.Socialmedia(DATA=data, RESULT_SOCIALMEDIA=result_socialmedia, EXECUTE_DATE=execute_date, USER_ID=user_id)

        self.email_regex = socialmedia_funct.give_email_regex()

        self.user_id = user_id
        # self.style = app_styles.AppStyle()

        self.data_socialmedia = tk.StringVar()
        self.data_socialmedia_entry = tk.Entry(parent, textvariable=self.data_socialmedia)
        self.data_socialmedia_entry.grid(column=0, row=0)
        # self.data_socialmedia_entry.configure(**self.style.style.configure('My.TEntry'))

        self.res_label = tk.Label(parent, text="")
        self.res_label.grid(column=2, row=0)

        self.butt_socialmedia = tk.Button(parent, text="Execute socialmedia",
                                                         command=self.ex_but_socialmedia)
        self.butt_socialmedia.grid(column=0, row=1)
        # self.butt_socialmedia.configure(**self.style.style.configure('My.TButton'))

        self.st_res_socialmedia = st.ScrolledText(parent, width=40, height=20)
        self.st_res_socialmedia.grid(column=0, row=2, padx=10, pady=10)
        # self.st_res_socialmedia.configure(**self.style.style.configure('My.TScrolledText'))

    def get_frame(self):
        return self

    def ex_but_socialmedia(self):
        data = self.data_socialmedia_entry.get()
        data_checked = self.email_regex(pattern=None, value=None).check_email_pattern(value=data)
        if data_checked != True:
            self.res_label.config(text=data_checked, fg="red")
        else:
            self.res_label.config(text="")

            execute_date = datetime.datetime.now()
            user_id = self.user_id

            result_socialmedia = self.socialmedia.get_result_socialmedia(data)
            self.socialmedia.ex_socialmedia(data, result_socialmedia, execute_date, user_id)

            self.st_res_socialmedia.delete('1.0', tk.END)
            if result_socialmedia:
                self.st_res_socialmedia.insert(tk.END, f"Datos: {result_socialmedia}")
            else:
                self.st_res_socialmedia.insert(tk.END, "Error en el insert de los datos")
