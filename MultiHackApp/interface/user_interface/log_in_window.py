import sys
import tkinter as tk

from app.user.user_func import User
from interface.user_interface import sign_up_window
from interface import main_window
# from interface.style.app_styles import AppStyle
from data.regex.name_regex_patterns import NameRegex


def execute_log_in_window(id_user, name, second_name, nickname, password, email, signup_date):
    """
    Abre una nueva ventana de inicio de sesión.
    Esta función crea e inicia una instancia de la ventana de inicio de sesión (LogInWindow).

    :param email:
    :param name:
    :param second_name:
    :param id_user: Identificador único del usuario.
    :param nickname: Apodo (nickname) del usuario.
    :param password: Contraseña del usuario.
    :param signup_date: Fecha de registro del usuario.
    """
    log_in_window = LogInWindow(id_user=id_user, name=name, second_name=second_name, nickname=nickname, email=email,
                                password=password, signup_date=signup_date)
    log_in_window.log_in_window.mainloop()


class LogInWindow:
    def __init__(self, id_user, name, second_name, nickname, email, password, signup_date):
        """
        Inicializa una nueva ventana de inicio de sesión.

        :param id_user: Identificador único del usuario.
        :param nickname: Apodo (nickname) del usuario.
        :param password: Contraseña del usuario.
        :param signup_date: Fecha de registro del usuario.
        """
        self.user = User(id_user, name, second_name, nickname, email, password, signup_date)
        self.log_in_window = tk.Tk()
        # self.style = AppStyle()

        # Tamaño de la ventana
        width = 300
        height = 350

        self.log_in_window.grid_columnconfigure(0, weight=1)
        self.log_in_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Obtener las dimensiones de la pantalla
        screen_width = self.log_in_window.winfo_screenwidth()
        screen_height = self.log_in_window.winfo_screenheight()

        # Calcular la posición de la ventana en el centro de la pantalla
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)

        # Establecer la geometría de la ventana
        self.log_in_window.geometry(f"{width}x{height}+{x_position}+{y_position}")

        self.log_in_window.title("MHApp // Log In")
        # self.log_in_window.configure(background='black')

        self.label_nickname = tk.Label(self.log_in_window, text="Nickname: ")
        self.label_nickname.grid(column=0, row=0, sticky=tk.NSEW, padx=110, pady=10)
        # self.label_nickname.configure(**self.style.style.configure('My.TLabel'))
        self.data_nickname = tk.StringVar()
        self.data_nickname_entry = tk.Entry(self.log_in_window, width=10, textvariable=self.data_nickname)
        self.data_nickname_entry.grid(column=0, row=1, sticky=tk.NSEW, padx=110, pady=10)
        # self.data_nickname_entry.configure(**self.style.style.configure('My.TEntry'))

        self.label_password = tk.Label(self.log_in_window, text="Contraseña: ")
        self.label_password.grid(column=0, row=2, sticky=tk.NSEW, padx=110, pady=10)
        # self.label_password.configure(**self.style.style.configure('My.TLabel'))
        self.data_password = tk.StringVar()
        self.data_password_entry = tk.Entry(self.log_in_window, width=10, textvariable=self.data_password, show="*")
        self.data_password_entry.grid(column=0, row=3, sticky=tk.NSEW, padx=110, pady=10)
        # self.data_password_entry.configure(**self.style.style.configure('My.TEntry'))

        self.log_in_butt = tk.Button(self.log_in_window, text="Iniciar sesión", command=self.log_in)
        self.log_in_butt.grid(column=0, row=4, sticky=tk.NSEW, padx=110, pady=10)
        # self.log_in_butt.configure(**self.style.style.configure('My.TButton'))

        self.go_signup_butt = tk.Button(self.log_in_window, text="Registrarse", command=self.go_signup)
        self.go_signup_butt.grid(column=0, row=5, sticky=tk.NSEW, padx=110, pady=10)
        # self.go_signup_butt.configure(**self.style.style.configure('My.TButton'))

        self.res_label_frame = tk.Frame(self.log_in_window)
        self.res_label_frame.grid(column=0, row=7)
        self.res_label_frame.configure(width=300)

        self.res_label = tk.Label(self.res_label_frame, text="",
                                  wraplength=width - 200)
        self.res_label.pack(fill=tk.X, padx=1, pady=1)
        # self.res_label.configure(**self.style.style.configure('My.TLabel'))

    def log_in(self):
        """
        Inicia sesión para el usuario con los datos proporcionados.
        """
        nickname = self.data_nickname.get()
        password = self.data_password.get()
        nickname_checked = NameRegex(pattern=None, value=None).check_name_pattern(value=nickname)
        # Si se cambia al recomendado interpreta el resultado del método como booleano y falla.
        if nickname_checked != True:
            self.res_label.config(text=nickname_checked, fg="red")
        else:
            usuario = self.user.log_in(nickname, password)
            if usuario:
                self.log_in_window.withdraw()
                main_window.iniciar_interfaz_grafica(usuario)
            else:
                self.res_label.config(text="Credenciales incorrectas", fg="red")

    def go_signup(self):
        """
        Abre la ventana de registro.
        """
        self.log_in_window.withdraw()
        sign_up_window.execute_child_window(root=self.log_in_window)

    def verify_user(self):
        pass

    def on_closing(self):
        """
        Función para cerrar la aplicación al completo cuando se cierra la ventana.
        """
        self.log_in_window.destroy()
        # Cierra la aplicación
        sys.exit()
