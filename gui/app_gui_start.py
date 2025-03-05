# Importaciones de módulos estándar y terceros
import os
import tkinter as tk
from tkinter import font as tkFont
import ctypes
import customtkinter
from config_manager import load_config
from .gui_red_theme import APPGUIRED
from .gui_blue_theme import APPGUIBLUE
from .gui_green_theme import APPGUIGREEN

# Función para cargar una fuente personalizada usando la API de Windows
def load_custom_font(font_path):
    FR_PRIVATE = 0x10
    FR_NOT_ENUM = 0x20
    path = os.path.abspath(font_path)
    res = ctypes.windll.gdi32.AddFontResourceExW(ctypes.c_wchar_p(path), FR_PRIVATE | FR_NOT_ENUM, 0)
    if res == 0:
        print("Error adding font from:", path)
    return res

# Inicializa la fuente personalizada y retorna el objeto font de tkinter
def init_custom_font():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    font_path = os.path.join("assets", "fonts", "segoe-ui-black.ttf")
    load_custom_font(font_path)
    custom_font = tkFont.Font(root=root, family="Segoe UI Black", size=16)
    root.destroy()
    return custom_font

# Carga e inicializa la fuente personalizada
custom_font = init_custom_font()

# Función principal para iniciar la aplicación con el tema configurado
def start_app():
    config = load_config()
    theme = config.get("theme", "blue").lower()
    if theme == "red":
        app = APPGUIRED()
    elif theme == "green":
        app = APPGUIGREEN()
    else:
        app = APPGUIBLUE()
    app.mainloop()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    start_app()
