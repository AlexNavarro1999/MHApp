import os
from data.connect_bbdd import connect_bbdd


def get_tables_and_columns():
    try:
        # Intentar conectar a la base de datos
        conn = connect_bbdd()

        # Inicializar el cursor
        cursor = conn.cursor()

        # Obtener el nombre de las tablas
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()

        # Crear un diccionario para almacenar la información de las tablas y columnas
        tables_and_columns = {}

        # Iterar sobre las tablas
        for (tabla,) in tablas:
            # Obtener el nombre de las columnas de la tabla
            cursor.execute("SHOW COLUMNS FROM " + tabla)
            columnas = cursor.fetchall()

            # Almacenar el nombre de la tabla y sus columnas en el diccionario
            tables_and_columns[tabla] = [columna[0] for columna in columnas]

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

        return tables_and_columns

    except Exception as e:
        print("Ocurrió un error:", e)


def gen_functs_files():
    """
    Genera archivos de funcionalidades para cada tabla 'history_' en la base de datos.
    Cada archivo contendrá una clase con atributos dinámicamente generados basados en las columnas de la tabla.
    """
    info_tables = get_tables_and_columns()
    print(type(info_tables))
    actual_path = os.getcwd()
    proyect_dir = str(actual_path).replace("\data\generate_files", "")

    for key, info in info_tables.items():
        if "_funct" in key:
            attr_names = ""
            file_name = key.replace("_funct", "")
            camel_funct_names = file_name.replace("_", "")
            path_file = os.path.join(proyect_dir, 'app', 'functionalities', f'{file_name}_funct.py')
            if not os.path.exists(path_file):
                for i, column in enumerate(info):
                    if i > 0:
                        attr_names += f'''self.{column}_F = {column}\n        '''
                    code = f'''
import mysql.connector
import os
from data.connect_bbdd import connect_bbdd
from data.generate_files.funct_files import get_tables_and_columns


class {camel_funct_names.capitalize()}:
    def __init__(self, {", ".join(info_tables[key][1:])}):
        {attr_names}
    def get_result_{file_name}(self, data):
        result_{file_name} = f"Funcionalidad {camel_funct_names} no implementada. Dato introducido: {{data}}"
        return result_{file_name}

    def ex_{file_name}(self, {", ".join(info_tables[key][1:])}):
        funct_names = []
        for name in get_tables_and_columns().keys():
            if "_funct" in name:
                funct_names.append(name)
        actual_path = os.path.abspath(__file__)
        file_name = actual_path.replace("_funct.py", "")
        splitted_file_name = file_name.split("\\\\").pop()
        final_file_name = splitted_file_name + "_funct"
        conn = connect_bbdd()
        cursor = conn.cursor()
        print(get_tables_and_columns().keys())
        try:
            if final_file_name in funct_names:
                cursor.execute(
                    f"INSERT INTO {{final_file_name}}(data, result_{{splitted_file_name}}, execute_date, user_id) VALUES (%s, %s, %s, %s)",
                    ({", ".join(info_tables[key][1:])}))
                conn.commit()
        except mysql.connector.Error as e:
            print("Error en la insercion:", e)
        finally:
            conn.close()


    '''
                    with open(path_file, 'w') as file:
                        file.write(code)
            else:
                print(f"El archivo {path_file} ya existe. No se ha creado ni escrito nada.")
