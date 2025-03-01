from config_manager import load_config
from .gui_red_theme import APPGUIRED
from .gui_blue_theme import APPGUIBLUE
from .gui_green_theme import APPGUIGREEN

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
