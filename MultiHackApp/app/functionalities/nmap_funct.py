import mysql.connector
import os
import subprocess
from data.connect_bbdd import connect_bbdd
from data.generate_files.funct_files import get_tables_and_columns
from data.regex.ip_regex_patterns import IpRegex


def give_domain_regex():
    ip_regex = IpRegex
    return ip_regex


class Nmap:
    def __init__(self, DATA, RESULT_NMAP, EXECUTE_DATE, USER_ID):
        self.DATA_F = DATA
        self.RESULT_NMAP_F = RESULT_NMAP
        self.EXECUTE_DATE_F = EXECUTE_DATE
        self.USER_ID_F = USER_ID

    def execute_intense_scan(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -T4 -A -v {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)

        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_intense_scan_plus_udp(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -sS -sU -T4 -A -v {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)

        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_intense_scan_all_ports(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -p 1-65535 -T4 -A -v {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)

        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_intense_scan_no_ping(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -T4 -A -v -Pn {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_ping_scan(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -sn {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_quick_scan(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -T4 -F {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_quick_scan_plus(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -sV -T4 -O -F --version-light {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_quick_traceroute(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -sn --traceroute {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_regular_scan(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def execute_slow_comprehensive_scan(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = (f'nmap -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script "default or '
                        f'(discovery and safe)" {data}')

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def get_result_nmap(self, data):
        # Comando nmap a ejecutar
        result_nmap = None
        nmap_command = f"nmap -sV -sS -A -O {data}"

        # Ejecutar el comando y capturar la salida
        try:
            # Ejecutar el comando y capturar la salida
            result_nmap = subprocess.check_output(nmap_command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            # En caso de error, imprimir el mensaje de error
            print("Error en la ejecución de nmap:", e)
        return result_nmap

    def ex_nmap(self, DATA, RESULT_NMAP, EXECUTE_DATE, USER_ID):
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
                    (DATA, RESULT_NMAP, EXECUTE_DATE, USER_ID))
                conn.commit()
        except mysql.connector.Error as e:
            print("Error en la insercion:", e)
            print("Codigo de error:", e.errno)
            print("Mensaje de error:", e.msg)
        finally:
            conn.close()
