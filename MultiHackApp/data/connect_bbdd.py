import mysql.connector


def connect_bbdd():
    """
       Conecta a la base de datos MySQL.

       La función intenta conectarse a una base de datos MySQL ubicada en un servidor remoto
       utilizando los datos de conexión proporcionados. La función devuelve una conexión al
       servidor MySQL.

       Returns:
           mysql.connector.connection.MySQLConnection: Conexión a la base de datos MySQL.

       Raises:
           mysql.connector.Error: Si hay algún error al conectar a la base de datos MySQL.
       """

    try:
        # Datos de conexión a la base de datos MySQL
        host = '127.0.0.1'
        user = 'uhacking'
        password = 'uhacking'
        database = 'hacking'

        # Conectar a la base de datos MySQL
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        return conn

    except mysql.connector.Error as e:
        print("Error de la base de datos", f"Error al conectar a la base de datos MySQL: {e}")

    finally:
        # No cerramos la conexión aquí porque la necesitaremos fuera de la función
        pass


def main():
    """
    Función principal para comprobar la conexión a la base de datos MySQL.
    """
    try:
        # Intentar conectar a la base de datos
        conn = connect_bbdd()

        # Verificar si la conexión se realizó con éxito
        if conn.is_connected():
            print("Conexión a la base de datos MySQL establecida correctamente.")
        else:
            print("La conexión a la base de datos MySQL no se estableció correctamente.")

    except Exception as e:
        print("Ocurrió un error:", e)


if __name__ == "__main__":
    main()
