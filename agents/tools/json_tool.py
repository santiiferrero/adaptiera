import json

def leer_json(path):
    with open(path) as f:
        return json.load(f)
