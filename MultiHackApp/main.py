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

"""
APAÑO DE INICIO DE SESIÓN CON VERIFICACIÓN DE EMAIL:
1_El usuario inicia sesión.
2_Si las credenciales son correctas, la app muestra un correo temporal y un código.
3_El usuario debe mandar un correo electrónico con el código al correo temporal desde su correo personal.
4_La app verifica el código y el email del usuario, si algo no coincide, se deniega el inicio de sesión.
* ¿Encriptación del correo electrónico del usuario en la bbdd?
--------------------------------------------------------------------------------------------------------------------
MEJORAS:
    -DESCARGA DE ARCHIVOS: Se generan los formatos csv, pdf y json a partir del txt, pero es necesario que el contenido
        del txt esté en formato json para realizar dicha conversión. A la hora de generar el resto de archivos los datos
        se muestran en formato json.
    -NMAP: Que una vez se seleccione lo que se quiere obtener te ponga que nmap(mostrando los atributos del comando)
        se ejecuta.
    -CURL: Añadir una opción para que se comprueben si están las cabeceras de seguridad. Dejar de usar pycurl y usar
        solo request con subprocess.
--------------------------------------------------------------------------------------------------------------------
Convertir a ejecutable e instalable.
--------------------------------------------------------------------------------------------------------------------
FUNCIONALIDADES SIMPLES:
    - Añadir geolocalización de ip como funcionalidad.

FUNCIONALIDADES COMPLEJAS:
    - Comprobar si un correo está registrado en distintas webs, y en el caso de que así sea, sacar información de la 
      cuenta de usuario a través de dicho correo. Librería Requests y headers.
"""
