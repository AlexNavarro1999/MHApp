
import mysql.connector
import os
from data.connect_bbdd import connect_bbdd
from data.generate_files.funct_files import get_tables_and_columns
from data.regex.email_regex_patterns import EmailRegex


def give_email_regex():
    email_regex = EmailRegex
    return email_regex


class Socialmedia:
    def __init__(self, DATA, RESULT_SOCIALMEDIA, EXECUTE_DATE, USER_ID):
        self.DATA_F = DATA
        self.RESULT_SOCIALMEDIA_F = RESULT_SOCIALMEDIA
        self.EXECUTE_DATE_F = EXECUTE_DATE
        self.USER_ID_F = USER_ID
        
    def get_result_socialmedia(self, data):
        result_socialmedia = f"Funcionalidad socialmedia no implementada. Dato introducido: {data}"
        return result_socialmedia

    def ex_socialmedia(self, DATA, RESULT_SOCIALMEDIA, EXECUTE_DATE, USER_ID):
        funct_names = []
        for name in get_tables_and_columns().keys():
            if "_funct" in name:
                funct_names.append(name)
        actual_path = os.path.abspath(__file__)
        file_name = actual_path.replace("_funct.py", "")
        splitted_file_name = file_name.split("\\").pop()
        final_file_name = splitted_file_name + "_funct"
        conn = connect_bbdd()
        cursor = conn.cursor()
        print(get_tables_and_columns().keys())
        try:
            if final_file_name in funct_names:
                cursor.execute(
                    f"INSERT INTO {final_file_name}(data, result_{splitted_file_name}, execute_date, user_id) VALUES (%s, %s, %s, %s)",
                    (DATA, RESULT_SOCIALMEDIA, EXECUTE_DATE, USER_ID))
                conn.commit()
        except mysql.connector.Error as e:
            print("Error en la insercion:", e)
        finally:
            conn.close()


    