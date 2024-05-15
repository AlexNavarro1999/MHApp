import os
from data.generate_files.funct_files import get_tables_and_columns


def gen_tabs_files():
    info_tables = get_tables_and_columns()
    actual_path = os.getcwd()
    proyect_dir = str(actual_path).replace("\data\generate_files", "")

    for key, info in info_tables.items():
        if "_funct" in key:
            attr_names = ""
            param_names = ""
            file_name = key.replace("_funct", "")
            camel_tab_names = file_name.replace("_", "")
            path_file = os.path.join(proyect_dir, 'interface', 'tabs', f'{file_name}_tab.py')
            if not os.path.exists(path_file):
                for i, column in enumerate(info):
                    attr_names += f'''self.{column}_T = {column}\n'''
                    param_names += f'''{column}={column.lower()}, '''
                    param_names_trimmed = param_names[:-2]
                    code = f'''
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import datetime

from app.functionalities import {file_name}_funct
# from interface.style import app_styles


class {camel_tab_names.capitalize()}(ttk.Frame):
    def __init__(self, parent, {", ".join(info_tables[key][1:-1]).lower()}, user_id):
        super().__init__(parent)
        self.{camel_tab_names} = {file_name}_funct.{camel_tab_names.capitalize()}({param_names_trimmed[param_names_trimmed.find(",") + 2:]})

        self.user_id = user_id
        # self.style = app_styles.AppStyle()

        self.data_{file_name} = tk.StringVar()
        self.data_{file_name}_entry = tk.Entry(parent, textvariable=self.data_{file_name})
        self.data_{file_name}_entry.grid(column=0, row=0)
        # self.data_{file_name}_entry.configure(**self.style.style.configure('My.TEntry'))
        
        self.res_label = tk.Label(parent, text="")
        self.res_label.grid(column=2, row=0)

        self.butt_{file_name} = tk.Button(parent, text="Execute {file_name}",
                                                         command=self.ex_but_{camel_tab_names})
        self.butt_{file_name}.grid(column=0, row=1)
        # self.butt_{file_name}.configure(**self.style.style.configure('My.TButton'))

        self.st_res_{camel_tab_names} = st.ScrolledText(parent, width=40, height=20)
        self.st_res_{camel_tab_names}.grid(column=0, row=2, padx=10, pady=10)
        # self.st_res_{camel_tab_names}.configure(**self.style.style.configure('My.TScrolledText'))

    def get_frame(self):
        return self

    def ex_but_{camel_tab_names}(self):
        data = self.data_{file_name}_entry.get()
        execute_date = datetime.datetime.now()
        user_id = self.user_id

        result_{file_name} = self.{camel_tab_names}.get_result_{file_name}(data)
        self.{camel_tab_names}.ex_{file_name}(data, result_{file_name}, execute_date, user_id)

        self.st_res_{camel_tab_names}.delete('1.0', tk.END)
        if result_{file_name}:
            self.st_res_{camel_tab_names}.insert(tk.END, f"Datos: {{result_{file_name}}}")
        else:
            self.st_res_{camel_tab_names}.insert(tk.END, "Error en el insert de los datos")
'''
                    with open(path_file, 'w') as file:
                        file.write(code)
            else:
                print(f"El archivo {path_file} ya existe. No se ha creado ni escrito nada.")


if __name__ == "__main__":
    gen_tabs_files()
