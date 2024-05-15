import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import datetime

from app.functionalities import nmap_funct
# from interface.style import app_styles

# Intense scan: nmap -T4 -A -v
# Intense scan plus UDP: nmap -sS -sU -T4 -A -v
# Intense scan, all TCP ports: nmap -p 1-65535 -T4 -A -v
# Intense scan, no ping: nmap -T4 -A -v -Pn
# Ping scan: nmap -sn
# Quick scan: nmap -T4 -F
# Quick scan plus: nmap -sV -T4 -O -F --version-light
# Quick traceroute: nmap -sn --traceroute
# Regular scan: nmap
# Slow comprehensive scan: nmap -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script "default or (discovery and safe)"

class Nmap(ttk.Frame):
    def __init__(self, parent, data, result_nmap, execute_date, user_id):
        super().__init__(parent)
        self.nmap_method_list = []
        self.methods_list = [method for method in dir(nmap_funct.Nmap) if callable(
            getattr(nmap_funct.Nmap, method)) and not method.startswith("__")]
        for method in self.methods_list:
            if "execute_" in method:
                method_name1 = method.replace("execute_", "")
                method_name2 = method_name1.replace("_", " ")
                self.nmap_method_list.append(method_name2)
        self.nmap = nmap_funct.Nmap(DATA=data, RESULT_NMAP=result_nmap, EXECUTE_DATE=execute_date, USER_ID=user_id)

        self.ip_regex = nmap_funct.give_domain_regex()
        self.user_id = user_id
        # self.style = app_styles.AppStyle()

        self.combo = ttk.Combobox(parent, values=self.nmap_method_list)
        self.combo.bind("<<ComboboxSelected>>", self.selection_changed)
        self.combo.grid(column=1, row=0)

        self.data_nmap = tk.StringVar()
        self.data_nmap_entry = tk.Entry(parent, textvariable=self.data_nmap)
        self.data_nmap_entry.grid(column=0, row=0)
        # self.data_nmap_entry.configure(**self.style.style.configure('My.TEntry'))

        self.res_label = tk.Label(parent, text="")
        self.res_label.grid(column=2, row=0)

        self.butt_nmap = tk.Button(parent, text="Execute nmap",
                                   command=self.ex_but_nmap)
        self.butt_nmap.grid(column=0, row=1)
        # self.butt_nmap.configure(**self.style.style.configure('My.TButton'))

        self.st_res_nmap = st.ScrolledText(parent, width=40, height=20)
        self.st_res_nmap.grid(column=0, row=2, padx=10, pady=10)
        # self.st_res_nmap.configure(**self.style.style.configure('My.TScrolledText'))

    def selection_changed(self, event):
        pass

    def get_frame(self):
        return self

    def ex_but_nmap(self):
        selected_method = self.combo.get()
        original_method_name = selected_method.replace(" ", "_")
        for method_name in dir(self.nmap):
            method = getattr(self.nmap, method_name)
            if callable(method) and original_method_name in method_name:
                data = self.data_nmap_entry.get()
                data_checked = self.ip_regex(pattern=None, value=None).check_ip_pattern(value=data)
                if data_checked != True:
                    self.res_label.config(text=data_checked, fg="red")
                else:
                    self.res_label.config(text="")
                    execute_date = datetime.datetime.now()
                    user_id = self.user_id

                    result_nmap = method(data)
                    self.nmap.ex_nmap(data, result_nmap, execute_date, user_id)

                    self.st_res_nmap.delete('1.0', tk.END)
                    if result_nmap:
                        self.st_res_nmap.insert(tk.END, f"Datos: {result_nmap}")
                    else:
                        self.st_res_nmap.insert(tk.END, "Error en el insert de los datos")
