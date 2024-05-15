import json
import os


def get_json_data():
    project_path = os.getcwd()
    print(project_path)
    path_json_file = os.path.join(project_path, 'data', 'regex')
    print(path_json_file)
    json_file = None
    regex_patterns = None
    for file in os.listdir(path_json_file):
        if file.endswith(".json"):
            json_file = os.path.join(path_json_file, file)
            break
    if json_file:
        with open(json_file, "r", encoding="utf-8") as json_file:
            json_content = json.load(json_file)
            regex_patterns = json_content["regex_patterns"]
    else:
        print("Archivo JSON no encontrado.")
    return regex_patterns
