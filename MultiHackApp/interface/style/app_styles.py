from tkinter import ttk


class AppStyle:
    def __init__(self):
        self.style = ttk.Style()

        self.style.configure('My.TButton', foreground='white', font=('Consolas', 10), background='black')
        self.style.configure('My.TCombobox', foreground='white', font=('Consolas', 10), background='black')
        self.style.configure('My.TLabel', foreground='white', font=('Consolas', 10), background='black')

        # Configuración del fondo para TNotebook
        self.style.configure('TNotebook', background='black')
        self.style.configure('TNotebook.Tab', background='black', foreground='white')

        self.style.configure('My.TFrame', background='black')
        self.style.configure('My.TScrolledText', foreground='white', font=('Consolas', 10), background='black')
        self.style.configure('My.TCheckbutton', foreground='white', font=('Consolas', 10), background='black')
        self.style.configure('My.TEntry', foreground='white', font=('Consolas', 10), background='black')


app_styles = AppStyle
