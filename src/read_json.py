import json


class JSON_Reader:
    def __init__(self):
        pass

    def read_json_file(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data
