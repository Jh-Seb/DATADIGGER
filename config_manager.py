import json, os
CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        config = {"theme": "blue", "reports_directory": ""}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        return config
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def update_config(theme=None, reports_directory=None):
    config = load_config()
    if theme is not None:
        config["theme"] = theme
    if reports_directory is not None:
        config["reports_directory"] = reports_directory
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    return config
