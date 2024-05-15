import re
from data.regex.get_json_file import get_json_data


class DomainRegex:
    def __init__(self, pattern, value):
        self.pattern = pattern
        self.value = value
        self.json_data = get_json_data()

    def check_domain_pattern(self, value):
        value_pattern = None
        for pattern in self.json_data:
            if pattern["name"] == "dominio":
                value_pattern = re.compile(pattern["pattern"])
                break

        if not value_pattern:
            no_pattern = "No hay patrón para el dato introducido"
            return no_pattern

        if not value_pattern.fullmatch(value):
            invalid_format = "Formato no válido"
            return invalid_format

        return True
