import mysql.connector
import datetime
import os
import shutil
import json
import secrets
from hashlib import pbkdf2_hmac
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from data.connect_bbdd import connect_bbdd
from data.generate_files.funct_files import get_tables_and_columns
from data.regex.only_integers_regex_patterns import OnlyIntegersRegex
from data.regex.name_regex_patterns import NameRegex


def give_name_regex():
    name_regex = NameRegex
    return name_regex


def give_only_integers_regex():
    only_integers_regex = OnlyIntegersRegex
    return only_integers_regex


class User:
    def __init__(self, id_user, name, second_name, nickname, password, email, signup_date):
        """
        Inicializa un objeto de usuario con la información proporcionada.

        :param id_user: Identificador único del usuario.
        :param nickname: Apodo (nickname) del usuario.
        :param password: Contraseña del usuario.
        :param signup_date: Fecha de registro del usuario.
        """
        self.idUser = id_user
        self.nameUser = name
        self.secondNameUser = second_name
        self.nickNameUser = nickname
        self.emailUser = email
        self.passwordUser = password
        self.signupDate = signup_date

    def gen_salt(self):
        # Generar un salt aleatorio seguro usando secrets.token_bytes
        salt = secrets.token_bytes(16)  # Tamaño

        return salt

    def log_in(self, nickname, password):
        """
        Inicia sesión para un usuario con el apodo (nickname) y contraseña dados.

        :param email:
        :param nickname: Apodo (nickname) del usuario para iniciar sesión.
        :param password: Contraseña del usuario para iniciar sesión.
        """
        conn = connect_bbdd()
        cursor = conn.cursor()

        try:
            # Comprobar si el usuario existe
            cursor.execute("SELECT * FROM users WHERE BINARY nickname=%s", (nickname,))
            user = cursor.fetchone()

            if user:
                # Obtener el salt del usuario
                salt = user[6]  # El salt está en la séptima columna (índice 6)

                # Calcular el hash de la contraseña con el salt
                password_byte = password.encode('utf-8')
                size_bytedata = 500_000
                hash_password = pbkdf2_hmac('sha256', password_byte, salt, iterations=200, dklen=size_bytedata)
                hex_password = hash_password.hex()

                # Comprobar si las contraseñas coinciden
                if user[5] == hex_password:  # Suponiendo que la contraseña está en la sexta columna (índice 5)
                    return user
                else:
                    return None
            else:
                return None

        except mysql.connector.Error as e:
            print("Error:", e)
            return None

        finally:
            if conn:
                conn.close()

    def sign_up(self, name, second_name, nickname, email, password, signup_date):
        """
        Registra un nuevo usuario con el apodo (nickname), contraseña y fecha de registro proporcionados.

        :param nickname: Apodo (nickname) para el nuevo usuario.
        :param password: Contraseña para el nuevo usuario.
        :param signup_date: Fecha de registro para el nuevo usuario.
        """
        salt = self.gen_salt()
        password_byte = password.encode('utf-8')
        size_bytedata = 500_000
        hash_password = pbkdf2_hmac('sha256', password_byte, salt, iterations=200, dklen=size_bytedata)
        hex_password = hash_password.hex()
        conn = connect_bbdd()
        cursor = conn.cursor()
        try:
            # Verificar si el nickname ya está en uso
            cursor.execute("SELECT COUNT(*) FROM users WHERE nickname=%s", (nickname,))
            count = cursor.fetchone()[0]

            if count == 0:
                # Realizar el registro
                cursor.execute(
                    "INSERT INTO users(name, second_name, nickname, email, password, salt, signup_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, second_name, nickname, email, hex_password, salt, signup_date))
                conn.commit()
            else:
                print(f"El nickname '{nickname}' ya está en uso. Por favor, elija otro.")
        except mysql.connector.IntegrityError:
            print(f"Error al registrar usuario. Por favor, inténtelo de nuevo.")
        finally:
            conn.close()

    def get_history(self, id_user):
        """
        Obtiene el historial de actividades del usuario.

        :return: Historial de funcionalidades del usuario.
        """
        conn = connect_bbdd()
        cursor = conn.cursor()

        info_tables = get_tables_and_columns()
        list_names = []
        for name, data in info_tables.items():
            if "_funct" in name:
                list_names.append(name)
        resultados = []
        try:
            # Construir la consulta dinámicamente
            query_parts = []
            for funct in list_names:
                funct_name = funct.replace("_funct", "")
                query_part = f'''
                        SELECT id_history_{funct_name}, '{funct_name}' AS funct_{funct_name}, data, result_{funct_name} AS result, execute_date
                        FROM {funct}
                        WHERE user_id = %s
                    '''
                query_parts.append(query_part)

            query = ' UNION '.join(query_parts) + ' ORDER BY execute_date DESC;'

            # Ejecutar la consulta
            cursor.execute(query, (id_user,) * len(list_names))
            resultados = cursor.fetchall()

        except mysql.connector.Error as e:
            print(e)

        finally:
            if conn:
                conn.close()
        return resultados

    def download_history(self, id_history, funct_name, selected_formats, output_folder):
        actual_path = os.getcwd()
        download_files_path = os.path.join(actual_path, 'data', 'download_files')
        conn = connect_bbdd()
        cursor = conn.cursor()

        try:
            query = f'''
                SELECT result_{funct_name}
                FROM {funct_name}_funct
                WHERE user_id = %s AND id_history_{funct_name} = %s
            '''

            cursor.execute(query, (self.idUser, id_history))
            result = cursor.fetchone()

            if result is not None:
                # Obtener la fecha actual en formato YYYYMMDD_HHMMSS
                current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                # Crear el nombre del archivo con el formato: funct_name_YYYYMMDD_HHMMSS.txt
                file_name = f"{funct_name}_{current_datetime}.txt"

                # Crear la ruta completa del archivo
                file_path = os.path.join(download_files_path, file_name)

                # Escribir el resultado en el archivo .txt
                with open(file_path, 'w') as file:
                    file.write(json.dumps({"resultado": result[0]}, indent=4))

                # Verificar y realizar conversiones según los formatos seleccionados
                if selected_formats:
                    for format_option in selected_formats:
                        if format_option == 'CSV':
                            self.convert_to_csv(file_path)
                        elif format_option == 'JSON':
                            self.convert_to_json(file_path)
                        elif format_option == 'PDF':
                            self.convert_to_pdf(file_path)
                try:
                    # Obtener la lista de todos los archivos en la carpeta download_files
                    all_files = os.listdir(download_files_path)

                    # Copiar y pegar todos los archivos en la carpeta seleccionada por el usuario
                    for file_name in all_files:
                        source_file_path = os.path.join(download_files_path, file_name)
                        destination_file_path = os.path.join(output_folder, file_name)
                        shutil.copy(source_file_path, destination_file_path)

                    for file_name in all_files:
                        file_path = os.path.join(download_files_path, file_name)
                        os.remove(file_path)

                except Exception as e:
                    print(f"Error durante la operación de copiar y pegar: {e}")

            else:
                print("No se encontraron resultados para la consulta.")

        except mysql.connector.Error as e:
            print(e)

        finally:
            if conn:
                conn.close()

    def convert_to_csv(self, txt_file_path):
        try:
            with open(txt_file_path, 'r') as txt_file:
                txt_content = txt_file.read()

            # Realizar la conversión a CSV
            csv_content = "\n".join([",".join(line.split()) for line in txt_content.split('\n')])

            # Crear el nombre del archivo con el formato: funct_name_YYYYMMDD_HHMMSS.csv
            csv_file_name = os.path.splitext(txt_file_path)[0] + ".csv"

            # Crear la ruta completa del archivo CSV
            csv_file_path = os.path.join(os.path.dirname(txt_file_path), csv_file_name)

            # Escribir el resultado en el archivo .csv
            with open(csv_file_path, 'w', newline='') as csv_file:
                csv_file.write(csv_content)

        except Exception as e:
            print(f"Error durante la conversión a CSV: {e}")

    def convert_to_json(self, txt_file_path):
        try:
            # Leer el contenido del archivo de texto
            with open(txt_file_path, 'r') as txt_file:
                txt_content = txt_file.read()

            # Convertir el contenido a un objeto Python (por ejemplo, una lista o un diccionario)
            # Aquí, se asume que el contenido es una cadena JSON válida
            json_data = json.loads(txt_content)

            # Crear un nuevo archivo con extensión .json y escribir el contenido en formato JSON
            json_file_path = txt_file_path.replace('.txt', '.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)

        except Exception as e:
            print(f"Error durante la conversión a JSON: {e}")

    def convert_to_pdf(self, txt_file_path):
        try:
            # Leer el contenido del archivo de texto
            with open(txt_file_path, 'r') as txt_file:
                txt_content = txt_file.readlines()

            # Crear un nuevo archivo con extensión .pdf y escribir el contenido en formato PDF
            pdf_file_path = txt_file_path.replace('.txt', '.pdf')
            pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=letter)

            y_position = 750  # Ajusta la posición vertical según tus necesidades
            line_height = 12  # Ajusta el espaciado entre líneas según tus necesidades

            for line in txt_content:
                pdf_canvas.drawString(100, y_position, line.strip())
                y_position -= line_height

            pdf_canvas.save()

        except Exception as e:
            print(f"Error durante la conversión a PDF: {e}")
