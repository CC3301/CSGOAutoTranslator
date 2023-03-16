import json

import logging
logging.getLogger()
#logging.basicConfig(level=logging.DEBUG)

class Persistance():
    def __init__(self):
        self.last_rcon_port: int = 0
        self.last_app_appearance = ""
        self.last_color_theme = ""
        self.last_target_lang = ""

        self.file = "/home/ffink/.csgoatt.appstate"

    def save(self):
        logging.info("Saving persistant appstate from disk")
        data = {
            "last_rcon_port": self.last_rcon_port,
            "last_app_appearance": self.last_app_appearance,
            "last_color_theme": self.last_color_theme,
            "last_target_lang": self.last_target_lang
        }
        try:
            with open(self.file, "w") as f:
                f.write(json.dumps(data))
        except Exception as e:
            print(f"failed to save persistent state to disk: {e}")

    def read(self):
        logging.info("Reading persistant appstate from disk")
        data = {}
        try:
            with open(self.file, "r") as f:
                data = json.loads(f.read())
        except Exception as e:
            logging.warn("Failed to read appstate, reverting to default values")
            data = {
                "last_rcon_port": "2121",
                "last_app_appearance": "System",
                "last_target_lang": "de",
                "last_color_theme": "blue"
            }
        finally:
            self.last_app_appearance = data["last_app_appearance"]
            self.last_color_theme    = data["last_color_theme"]
            self.last_rcon_port      = data["last_rcon_port"]
            self.last_target_lang    = data["last_target_lang"]
            