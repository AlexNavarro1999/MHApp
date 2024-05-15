# Importar la biblioteca Geocoder
import geocoder
import mysql.connector
import os
from data.connect_bbdd import connect_bbdd
from data.generate_files.funct_files import get_tables_and_columns
from data.regex.ip_regex_patterns import IpRegex


def give_ip_regex():
    ip_regex = IpRegex
    return ip_regex


class Geolocation:
    def __init__(self, DATA, RESULT_GEOLOCATION, EXECUTE_DATE, USER_ID):
        self.DATA_F = DATA
        self.RESULT_GEOLOCATION_F = RESULT_GEOLOCATION
        self.EXECUTE_DATE_F = EXECUTE_DATE
        self.USER_ID_F = USER_ID
        
    def get_result_geolocation(self, data):
        # Asignar la dirección IP a una variable
        ip = geocoder.ip("213.13.156.134")

        # Obtener información geográfica detallada
        info_geografica = ip.geojson['features'][0]['properties']

        # Almacenar la información geográfica detallada en un diccionario
        datos_geograficos = {
            "País": info_geografica.get('country', 'N/A'),
            "Región": info_geografica.get('region', 'N/A'),
            "Ciudad": info_geografica.get('city', 'N/A'),
            "Código postal": info_geografica.get('postal', 'N/A'),
            "Latitud": ip.latlng[0],
            "Longitud": ip.latlng[1],
            "ISP": info_geografica.get('org', 'N/A'),
            "Zona horaria": info_geografica.get('timezone', 'N/A')
        }
        result_geolocation = str(datos_geograficos)
        return result_geolocation

    def ex_geolocation(self, DATA, RESULT_GEOLOCATION, EXECUTE_DATE, USER_ID):
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
                    (DATA, RESULT_GEOLOCATION, EXECUTE_DATE, USER_ID))
                conn.commit()
        except mysql.connector.Error as e:
            print("Error en la insercion:", e)
        finally:
            conn.close()


    