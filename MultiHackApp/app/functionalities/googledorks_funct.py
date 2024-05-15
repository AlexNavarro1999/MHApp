import mysql.connector
import os
from googlesearch import search
from data.connect_bbdd import connect_bbdd
from data.generate_files.funct_files import get_tables_and_columns
from data.regex.domain_regex_patterns import DomainRegex


def give_domain_regex():
    domain_regex = DomainRegex
    return domain_regex


class Googledorks:
    def __init__(self, DATA, RESULT_GOOGLEDORKS, EXECUTE_DATE, USER_ID):
        self.DATA_F = DATA
        self.RESULT_GOOGLEDORKS_F = RESULT_GOOGLEDORKS
        self.EXECUTE_DATE_F = EXECUTE_DATE
        self.USER_ID_F = USER_ID

    def search_subdomains(self, data):
        subdomains = []
        for link in search(f"site:{data} -www", start=0, pause=0):
            subdomains.append(link)
            print(link)
        subdomains_str = ",".join(subdomains)
        print(subdomains_str)
        return subdomains_str

    def search_emails(self, data):
        emails = []
        for link in search(f"site:{data} intext:@granpiso.com", pause=0):
            emails.append(link)
            print(link)
        emails_str = ",".join(emails)
        print(emails_str)
        return emails_str

    def search_associated_files(self, data):
        associated_files = []
        file_types = ["pdf", "csv", "xls", "json", "txt", "docx", "rtf"]
        query = f"site:{data} filetype:{' OR filetype:'.join(file_types)}"
        for link in search(query, start=0, pause=0):
            associated_files.append(link)
        associated_files_str = ",".join(associated_files)
        print(associated_files_str)
        return associated_files_str

    """def get_result_googledorks(self, data):
        result_googledorks = f"Funcionalidad googledorks no implementada. Dato introducido: {data}"
        return result_googledorks"""

    def ex_googledorks(self, DATA, RESULT_GOOGLEDORKS, EXECUTE_DATE, USER_ID):
        print(f"RESULT GOOGLE DORKS: {RESULT_GOOGLEDORKS}")
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
                print(f"RESULT GOOGLE DORKS: {RESULT_GOOGLEDORKS}")
                cursor.execute(
                    f"INSERT INTO {final_file_name}(data, result_{splitted_file_name}, execute_date, user_id) VALUES (%s, %s, %s, %s)",
                    (DATA, RESULT_GOOGLEDORKS, EXECUTE_DATE, USER_ID))
                conn.commit()
        except mysql.connector.Error as e:
            print("Error en la insercion:", e)
        finally:
            conn.close()
