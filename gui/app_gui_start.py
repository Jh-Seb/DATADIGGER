import os
import tkinter as tk
from tkinter import font as tkFont
import customtkinter
from config_manager import load_config
from .gui_red_theme import APPGUIRED
from .gui_blue_theme import APPGUIBLUE
from .gui_green_theme import APPGUIGREEN

root = tk.Tk()
root.withdraw()
font_path = os.path.join("assets", "fonts", "segoe-ui-black.ttf")
try:
    segoe_font = tkFont.Font(file=font_path, size=16)
except Exception as e:
    print("Error loading font:", e)
root.destroy()

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
