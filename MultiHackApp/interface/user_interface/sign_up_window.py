import datetime
import sys
import tkinter as tk

from app.user.user_func import User
from data.regex.name_regex_patterns import NameRegex
from data.regex.email_regex_patterns import EmailRegex

# from interface.style import app_styles


def execute_child_window(root):
    """
    Abre una nueva ventana de registro.

    Esta función crea e inicia una instancia de la ventana de registro (SignUpWindow).
    """
    sign_up_window = SignUpWindow(root, id_user=None, name=None, second_name=None, nickname=None, email=None,
                                  password=None, signup_date=None)
    sign_up_window.mainloop()


class SignUpWindow(tk.Toplevel):
    def __init__(self, root, id_user, name, second_name, nickname, email, password, signup_date):
        """
        Inicializa una nueva ventana de registro.

        :param id_user: Identificador único del usuario.
        :param name: Nombre del usuario.
        :param second_name: Apellidos del usuario.
        :param nickname: Apodo (nickname) del usuario.
        :param email: Dirección de correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :param signup_date: Fecha de registro del usuario.
        """
        super().__init__()
        self.root = root
        self.user = User(id_user=id_user, name=name, second_name=second_name, nickname=nickname, email=email,
                         password=password, signup_date=signup_date)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Tamaño de la ventana
        width = 300
        height = 500

        # Obtener las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular la posición de la ventana en el centro de la pantalla
        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)

        # Establecer la geometría de la ventana
        self.geometry(f"{width}x{height}+{x_position}+{y_position}")
        self.title("MHApp // Sign Up")
        # self.configure(background='black')

        # self.style = app_styles.AppStyle()
        self.label_name = tk.Label(self, text="Nombre: ")
        self.label_name.grid(column=1, row=0, padx=10, pady=10)
        # self.label_name.configure(**self.style.style.configure('My.TLabel'))
        self.data_name = tk.StringVar()
        self.entry_name = tk.Entry(self, width=10, textvariable=self.data_name)
        self.entry_name.grid(column=1, row=1, padx=10, pady=10)
        # self.entry_name.configure(**self.style.style.configure('My.TEntry'))
        self.res_label_name = tk.Label(self, text="")
        self.res_label_name.grid(column=2, row=1, padx=10, pady=10)
        # self.res_label_name.configure(**self.style.style.configure('My.TLabel'))

        self.label_secondName = tk.Label(self, text="Apellidos: ")
        self.label_secondName.grid(column=1, row=2, padx=10, pady=10)
        # self.label_secondName.configure(**self.style.style.configure('My.TLabel'))
        self.data_secondName = tk.StringVar()
        self.entry_secondName = tk.Entry(self, width=10, textvariable=self.data_secondName)
        self.entry_secondName.grid(column=1, row=3, padx=10, pady=10)
        # self.entry_secondName.configure(**self.style.style.configure('My.TEntry'))
        self.res_label_secondName = tk.Label(self, text="")
        self.res_label_secondName.grid(column=2, row=3, padx=10, pady=10)
        # self.res_label_secondName.configure(**self.style.style.configure('My.TLabel'))

        self.label_nickname = tk.Label(self, text="Nickname: ")
        self.label_nickname.grid(column=1, row=4, padx=10, pady=10)
        # self.label_nickname.configure(**self.style.style.configure('My.TLabel'))
        self.data_nickname = tk.StringVar()
        self.entry_nickname = tk.Entry(self, width=10, textvariable=self.data_nickname)
        self.entry_nickname.grid(column=1, row=5, padx=10, pady=10)
        # self.entry_nickname.configure(**self.style.style.configure('My.TEntry'))
        self.res_label_nickname = tk.Label(self, text="")
        self.res_label_nickname.grid(column=2, row=5, padx=10, pady=10)
        # self.res_label_nickname.configure(**self.style.style.configure('My.TLabel'))

        self.label_email = tk.Label(self, text="Email: ")
        self.label_email.grid(column=1, row=6)
        # self.label_email.configure(**self.style.style.configure('My.TLabel'))
        self.data_email = tk.StringVar()
        self.entry_email = tk.Entry(self, width=10, textvariable=self.data_email)
        self.entry_email.grid(column=1, row=7, padx=10, pady=10)
        # self.entry_email.configure(**self.style.style.configure('My.TEntry'))
        self.res_label_email = tk.Label(self, text="")
        self.res_label_email.grid(column=2, row=7, padx=10, pady=10)
        # self.res_label_email.configure(**self.style.style.configure('My.TLabel'))

        self.label_password = tk.Label(self, text="Password: ")
        self.label_password.grid(column=1, row=8, padx=10, pady=10)
        # self.label_password.configure(**self.style.style.configure('My.TLabel'))
        self.data_password = tk.StringVar()
        self.entry_password = tk.Entry(self, width=10, textvariable=self.data_password, show="*")
        self.entry_password.grid(column=1, row=9, padx=10, pady=10)
        # self.entry_password.configure(**self.style.style.configure('My.TEntry'))

        self.boton = tk.Button(self, text="Sign up", command=self.sign_up)
        self.boton.grid(column=1, row=10, padx=10, pady=10)
        # self.boton.configure(**self.style.style.configure('My.TButton'))

        self.boton = tk.Button(self, text="Cancel", command=self.cancel_signup)
        self.boton.grid(column=1, row=11, padx=10, pady=10)
        # self.boton.configure(**self.style.style.configure('My.TButton'))

    def sign_up(self):
        """
        Realiza el registro de un nuevo usuario.

        Esta función llama al método 'sign_up' del objeto 'User' para registrar un nuevo usuario
        con los datos proporcionados en la ventana de registro.
        """
        name = self.data_name.get()
        second_name = self.data_secondName.get()
        nickname = self.data_nickname.get()
        email = self.data_email.get()
        password = self.data_password.get()

        name_checked = NameRegex(pattern=None, value=None).check_name_pattern(value=name)
        second_name_checked = NameRegex(pattern=None, value=None).check_name_pattern(value=second_name)
        nickname_checked = NameRegex(pattern=None, value=None).check_name_pattern(value=nickname)
        email_checked = EmailRegex(pattern=None, value=None).check_email_pattern(value=email)

        self.res_label_name.config(text="")
        self.res_label_secondName.config(text="")
        self.res_label_nickname.config(text="")
        self.res_label_email.config(text="")

        if name_checked != True:
            print(f"AQUI1: {nickname_checked}")
            self.res_label_name.config(text=name_checked, fg="red")
        elif second_name_checked != True:
            print(f"AQUI2: {nickname_checked}")
            self.res_label_secondName.config(text=second_name_checked, fg="red")
        elif nickname_checked != True:
            print(f"AQUI3: {nickname_checked}")
            self.res_label_nickname.config(text=nickname_checked, fg="red")
        elif email_checked != True:
            print(f"AQUI4: {nickname_checked}")
            self.res_label_email.config(text=email_checked, fg="red")
        else:
            self.user.sign_up(name, second_name, nickname, email, password, datetime.date.today())
            self.root.deiconify()  # Muestra la ventana de inicio de sesión
            self.destroy()

    def cancel_signup(self):
        self.root.deiconify()
        self.destroy()

    def on_closing(self):
        """
        Función para cerrar la aplicación al completo cuando se cierra la ventana.
        """
        self.destroy()
        # Cierra la aplicación
        sys.exit()
