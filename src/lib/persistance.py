"""
Provices persistance for settings made in CS:GO AutoTranslator Software
"""

import json
import logging

class Persistance():
    """
    Handles persistance functionality for application settings
    """
    def __init__(self):
        self.last_rcon_port: int = 0
        self.last_app_appearance = ""
        self.last_color_theme = ""
        self.last_target_lang = ""

        self.file = "/home/ffink/.csgoatt.appstate"

    def save(self):
        """
        Saves appstate file to disk
        """
        logging.info("Saving persistant appstate to disk")
        data = {
            "last_rcon_port": self.last_rcon_port,
            "last_target_lang": self.last_target_lang
        }
        try:
            with open(self.file, "w", encoding='utf-8') as file:
                file.write(json.dumps(data))
        except OSError as exception:
            print(f"failed to save persistent state to disk: {exception}")

    def read(self):
        """
        Reads the saved appstate file from disk, if it fails, return
        default values
        """
        logging.info("Reading persistant appstate from disk")
        data = {}
        try:
            with open(self.file, "r", encoding='utf-8') as file:
                data = json.loads(file.read())
        except OSError:
            logging.warning("Failed to read appstate, reverting to default values")
            data = {
                "last_rcon_port": "2121",
                "last_target_lang": "de",
            }
        finally:
            self.last_rcon_port      = data["last_rcon_port"]
            self.last_target_lang    = data["last_target_lang"]
            