# shared_state.py
import json
import os

titulo = None
parrafos = None
secciones = None

archive = "extracto_wikipedia.json"

def cargar():
    if os.path.exists(archive):
        with open(archive, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {}

def guardar(estado):
    with open(archive, "w", encoding="utf-8") as file:
        json.dump(estado, file, indent=4, ensure_ascii=False)

estado = cargar()

def set_titulo(value):
    estado["titulo"] = value
    guardar(estado)
    
def get_titulo():
    return estado.get("titulo", None)

def get_parrafos():
    return estado.get("parrafos", {})

def set_parrafos(value):
    estado["parrafos"] = value
    guardar(estado)
