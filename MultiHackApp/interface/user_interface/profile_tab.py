import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import filedialog
import os

from app.user.user_func import User
from app.user import user_func
# from interface.style import app_styles


class UserProfile(ttk.Frame):
    def __init__(self, parent, id_user, name, second_name, nickname, email, password, signup_date):
        super().__init__(parent)
        self.user = User(id_user=id_user, name=name, second_name=second_name, nickname=nickname, email=email,
                         password=password, signup_date=signup_date)
        self.history_result = self.user.get_history(id_user)
        # self.style = app_styles.AppStyle()
        self.configure(style='My.TFrame')

        self.name_regex = user_func.give_name_regex()
        self.integers_regex = user_func.give_only_integers_regex()

        self.code_funct_label = tk.Label(parent, text="History code:")
        self.code_funct_label.grid(column=0, row=0, sticky="nsew")
        # self.code_funct_label.configure(**self.style.style.configure('My.TLabel'))
        self.data_id_history = tk.IntVar(parent)
        self.data_id_history_entry = tk.Entry(parent, textvariable=self.data_id_history)
        self.data_id_history_entry.grid(column=1, row=0, sticky="nsew")
        # self.data_id_history_entry.configure(**self.style.style.configure('My.TEntry'))
        self.res_code_label = tk.Label(parent, text="")
        self.res_code_label.grid(column=1, row=1, sticky="nsew")

        self.history_name_label = tk.Label(parent, text="Functionality name:")
        self.history_name_label.grid(column=3, row=0, sticky="nsew")
        # self.history_name_label.configure(**self.style.style.configure('My.TLabel'))
        self.data_funct_name = tk.StringVar(parent)
        self.data_funct_name_entry = tk.Entry(parent, textvariable=self.data_funct_name)
        self.data_funct_name_entry.grid(column=4, row=0, sticky="nsew")
        # self.data_funct_name_entry.configure(**self.style.style.configure('My.TEntry'))
        self.res_hname_label = tk.Label(parent, text="")
        self.res_hname_label.grid(column=4, row=1, sticky="nsew")

        # Variables de control para los checkboxes
        self.txt = tk.StringVar(parent, "TXT")
        self.csv = tk.StringVar(parent, "CSV")
        self.json = tk.StringVar(parent, "JSON")
        self.pdf = tk.StringVar(parent, "PDF")

        # Crear los checkboxes
        self.checkbox1 = tk.Checkbutton(parent, text="TXT", variable=self.txt, onvalue="TXT", offvalue=0)
        self.checkbox2 = tk.Checkbutton(parent, text="CSV", variable=self.csv, onvalue="CSV", offvalue=0)
        self.checkbox3 = tk.Checkbutton(parent, text="JSON", variable=self.json, onvalue="JSON", offvalue=0)
        self.checkbox4 = tk.Checkbutton(parent, text="PDF", variable=self.pdf, onvalue="PDF", offvalue=0)

        self.checkbox1.grid(column=6, row=0, sticky="nsew")
        # self.checkbox1.configure(**self.style.style.configure('My.TCheckbutton'))
        self.checkbox2.grid(column=7, row=0, sticky="nsew")
        # self.checkbox2.configure(**self.style.style.configure('My.TCheckbutton'))
        self.checkbox3.grid(column=8, row=0, sticky="nsew")
        # self.checkbox3.configure(**self.style.style.configure('My.TCheckbutton'))
        self.checkbox4.grid(column=9, row=0, sticky="nsew")
        # self.checkbox4.configure(**self.style.style.configure('My.TCheckbutton'))

        self.butt_download = tk.Button(parent, text="Download", command=self.download)
        self.butt_download.grid(column=10, row=0, sticky="nsew")
        # self.butt_download.configure(**self.style.style.configure('My.TButton'))

        self.butt_show = tk.Button(parent, text="Show History", command=self.show_history)
        self.butt_show.grid(column=12, row=0, sticky="nsew")
        # self.butt_show.configure(**self.style.style.configure('My.TButton'))

        # Crear un widget ScrolledText
        self.history_result_text = st.ScrolledText(parent, wrap=tk.WORD)
        self.history_result_text.grid(column=0, row=5, columnspan=13, sticky="nsew")
        # self.history_result_text.configure(**self.style.style.configure('My.TScrolledText'))

    def show_history(self):
        self.history_result = self.user.get_history(self.user.idUser)
        self.history_result_text.delete('1.0', tk.END)

        # Crear una cadena de texto para mostrar la información del historial sin la columna result_{funct}
        display_text = ""
        for result in self.history_result:
            if isinstance(result, tuple):
                dict_result = {}
                field_names = ["code", "functionality", "data", "result", "execute date"]

                for i, res in enumerate(result):
                    if field_names[i] != 'result':
                        dict_result[field_names[i]] = res

                # Utilizar el diccionario para construir la cadena de texto
                formatted_result = " - ".join([f"{field}: {value}" for field, value in dict_result.items()])
                display_text += formatted_result + "\n"
            else:
                display_text += f"{result}\n"

        # Insertar la información en el widget ScrolledText
        self.history_result_text.insert(tk.END, display_text)

        # Deshabilitar la interacción del usuario con el widget
        # self.history_result_text.configure(state=tk.DISABLED)

    def download(self):
        id_history = self.data_id_history_entry.get()
        funct_name = self.data_funct_name_entry.get()
        id_history_checked = self.integers_regex(pattern=None, value=None).check_integers_pattern(value=id_history)
        funct_name_checked = self.name_regex(pattern=None, value=None).check_name_pattern(value=funct_name)

        if id_history_checked != True:
            self.res_code_label.config(text=id_history_checked, fg="red")
        elif funct_name_checked != True:
            self.res_code_label.config(text="")
            self.res_hname_label.config(text=funct_name_checked, fg="red")
        else:
            self.res_code_label.config(text="")
            self.res_hname_label.config(text="")
            selected_options = [self.txt.get(), self.csv.get(), self.json.get(), self.pdf.get()]
            print("Selected options:", selected_options)
            if id_history and funct_name:
                file_path = filedialog.askdirectory(title="Seleccione la carpeta para guardar archivos")
                print("Ubicación seleccionada:", file_path)
                self.user.download_history(id_history, funct_name, selected_options, file_path)
            else:
                print("Por favor, ingrese el código del historial y el nombre de la funcionalidad.")

    def get_frame(self):
        return self
