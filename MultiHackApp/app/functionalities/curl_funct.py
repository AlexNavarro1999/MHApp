import subprocess
import mysql.connector
import os
from data.connect_bbdd import connect_bbdd
from data.generate_files.funct_files import get_tables_and_columns
from data.regex.url_regex_patterns import UrlRegex

# Diccionarios de headers
client_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US;q=0.8,en;q=0.3',
    'Upgrade-Insecure-Requests': '1'
}

sec_headers = {
    'X-XSS-Protection': 'warning',
    'X-Frame-Options': 'warning',
    'X-Content-Type-Options': 'warning',
    'Strict-Transport-Security': 'error',
    'Content-Security-Policy': 'warning',
    'X-Permitted-Cross-Domain-Policies': 'deprecated',
    'Referrer-Policy': 'warning',
    'Expect-CT': 'deprecated',
    'Permissions-Policy': 'warning',
    'Cross-Origin-Embedder-Policy': 'warning',
    'Cross-Origin-Resource-Policy': 'warning',
    'Cross-Origin-Opener-Policy': 'warning'
}

information_headers = {
    'X-Powered-By': '',
    'Server': '',
    'X-AspNet-Version': '',
    'X-AspNetMvc-Version': ''
}


def give_url_regex():
    url_regex = UrlRegex
    return url_regex


cabeceras_limpias = []


class Curl:
    def __init__(self, DATA, RESULT_CURL, EXECUTE_DATE, USER_ID):
        self.DATA_F = DATA
        self.RESULT_CURL_F = RESULT_CURL
        self.EXECUTE_DATE_F = EXECUTE_DATE
        self.USER_ID_F = USER_ID

    def get_result_curl(self, data):
        resultado = subprocess.run(['curl', '-I', f'{data}'], capture_output=True, text=True)
        cabeceras_obtenidas = resultado.stdout.lower().splitlines()
        result_curl = str(cabeceras_obtenidas)

        return result_curl

    def ex_curl(self, DATA, RESULT_CURL, EXECUTE_DATE, USER_ID):
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
        try:
            if final_file_name in funct_names:
                cursor.execute(
                    f"INSERT INTO {final_file_name}(data, result_{splitted_file_name}, execute_date, user_id) VALUES (%s, %s, %s, %s)",
                    (DATA, RESULT_CURL, EXECUTE_DATE, USER_ID))
                conn.commit()
        except mysql.connector.Error as e:
            print("Error en la insercion:", e)
        finally:
            conn.close()
