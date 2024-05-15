import sys
import tkinter as tk
from tkinter import ttk
import os
import inspect
from importlib import import_module
from interface.user_interface import profile_tab

# from interface.style import app_styles

# from ttkbootstrap import Style


def get_profile_tab():
    profile_tab_imp = inspect.getmembers(profile_tab, inspect.isclass)
    class_profile_tab = profile_tab_imp[1][1]
    profile_params = inspect.signature(class_profile_tab).parameters
    null_profile_params = {name: None for name in list(profile_params.keys())[2:]}
    return class_profile_tab, null_profile_params


def iniciar_interfaz_grafica(usuario):
    """
    Inicia la interfaz gráfica principal de la aplicación.

    :param usuario: Objeto que representa al usuario que ha iniciado sesión.
    """
    menu_window = MainWindow(usuario)
    menu_window.mainloop()


class MainWindow(tk.Frame, tk.Toplevel):
    def __init__(self, usuario):
        """
        Inicia la ventana principal de la aplicación.

        :param usuario: Objeto que representa al usuario que ha iniciado sesión.
        """
        super().__init__()

        self.params = None
        self.imported_modules = []
        project_path = os.getcwd()
        # Obtenemos la ruta de los archivos en /tabs/
        self.actual_path = os.path.dirname(os.path.abspath(__file__))
        self.tabs_files_path = os.path.join(self.actual_path, 'tabs')
        self.path = os.listdir(self.tabs_files_path)

        self.menu_window = tk.Tk()
        self.menu_window.title(f"MHApp // User: {usuario[3]}")
        self.menu_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.style = app_styles.AppStyle()

        # Tamaño de la ventana
        width = 1366
        height = 768

        self.menu_window.grid_columnconfigure(0, weight=1)
        self.menu_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Obtener las dimensiones de la pantalla
        screen_width = self.menu_window.winfo_screenwidth()
        screen_height = self.menu_window.winfo_screenheight()

        # Calcular la posición de la ventana en el centro de la pantalla
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)

        # Establecer la geometría de la ventana
        self.menu_window.geometry(f"{width}x{height}+{x_position}+{y_position}")

        self.notebook = ttk.Notebook(self.menu_window)
        self.notebook.place(x=0, y=0, width=screen_width, height=screen_height)
        # self.notebook.configure(self.style.style.configure('My.TNotebook'))

        # Tab extra para el perfil del usuario
        self.profile_tab = ttk.Frame(self.notebook)
        # self.profile_tab.configure(self.style.style.configure('My.TFrame'))

        self.notebook.add(self.profile_tab, text="Profile")

        return_profile = get_profile_tab()
        instance_class_profile_tab = return_profile[0](self.profile_tab, usuario[0], **return_profile[1])
        instance_class_profile_tab.get_frame()

        # Recorremos los archivos que hay en /tabs/
        for file in self.path:
            # Sacamos el nombre de cada archivo sin extensión
            filename_no_ext = os.path.splitext(os.path.basename(file))[0]
            # Cogemos solo los archivos que queremos
            if filename_no_ext != '__init__' and filename_no_ext != '__pycache__':
                # Creamos un tab por cada archivo obtenido
                self.new_tab = ttk.Frame(self.notebook)
                # Importamos de forma dinámica esos archivos y los guardamos en una lista
                imported_module = import_module(f'interface.tabs.{filename_no_ext}')
                self.imported_modules.append(imported_module)
                # Recorremos los módulos importados
                for module in self.imported_modules:
                    # Si el nombre del arhivo sin extensión está en el módulo seleccionado
                    if filename_no_ext in str(module):
                        final_filename = filename_no_ext.replace("tab", "")
                        # Añadimos el tab previamente creado al notebook
                        self.notebook.add(self.new_tab, text=final_filename.replace("_", " ").capitalize())
                        # self.new_tab.configure(style='My.TFrame')
                        # Comprobamos si el módulo contiene una clase
                        info = inspect.getmembers(module, inspect.isclass)
                        # Sacamos el nombre de la clase (objeto tipo clase)
                        final_class = info[0][1]
                        # Sacamos los parámetros de esa clase
                        params = inspect.signature(final_class).parameters
                        """Los establecemos como nulos excepto el primero, que le pasamos el tab creado, 
                        y el último, que le pasamos el id_usuario del objeto usuario"""
                        null_params = {name: None for name in list(params.keys())[1:-1]}
                        # Los widgets generados en la clase se introducen en el tab correspondiente creado
                        params_to_pass = {'parent': self.new_tab, **null_params, 'user_id': usuario[0]}
                        instance_class = final_class(**params_to_pass)
                        instance_class.get_frame()

    def on_closing(self):
        """
        Función para cerrar la aplicación al completo cuando se cierra la ventana.
        """
        self.destroy()
        # Cierra la aplicación
        sys.exit()
