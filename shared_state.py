import json
import os

# Variables globales para almacenar datos
titulo = None
parrafos = None
secciones = None

# Nombre del archivo en el que se guardara toda la información
archive = "extracto_wikipedia.json"

# Función para cargar el estado desde el archivo JSON
def cargar():
    if os.path.exists(archive): #Verifica si el archivo extiste
        with open(archive, "r", encoding="utf-8") as file:
            return json.load(file) # Se carga y devuelve el contenido del archivo JSON
    else:
        return {} # Si el archivo no existe, devuelve un diccionario vacio

# Función para guardar el estado en el archivo JSON
def guardar(estado):
    with open(archive, "w", encoding="utf-8") as file:
        json.dump(estado, file, indent=4, ensure_ascii=False)

# Se carga el estado inicial del archivo JSON
estado = cargar()

# Función para establecer el título en el estado y guardarlo
def set_titulo(value):
    estado["titulo"] = value
    guardar(estado)

# Función para obtener el rítulo almacenado en el estado
def get_titulo():
    return estado.get("titulo", None)

# Función para establecer los párrafos en el estado y guardarlos
def set_parrafos(value):
    estado["parrafos"] = value
    guardar(estado)

# Función para obtnener los párrafos almacenados en el estado
def get_parrafos():
    return estado.get("parrafos", {})
