from data.connect_bbdd import connect_bbdd
from data.generate_files import funct_files, tabs_files
from interface.user_interface import log_in_window


def main():
    """
    Función principal del programa.

    Esta función realiza las siguientes acciones:
    1. Crea la base de datos llamando a la función 'create_bbdd.create_bbdd()'.
    2. Crea las tablas en la base de datos llamando a la función 'create_tables.create_tables()'.
    3. Ejecuta la ventana de inicio de sesión llamando a 'log_in_window.execute_log_in_window()'.
    """
    connect_bbdd()
    funct_files.gen_functs_files()
    tabs_files.gen_tabs_files()
    log_in_window.execute_log_in_window(id_user=None, name=None, second_name=None, nickname=None, email=None,
                                        password=None, signup_date=None)


if __name__ == "__main__":
    main()
