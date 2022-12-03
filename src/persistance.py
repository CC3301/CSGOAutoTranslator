import json

class Persistance():
    def __init__(self):
        self.last_log_file_locations = []
        self.last_app_appearance = ""
        self.last_color_theme = ""
        self.last_target_lang = ""

        self.file = "/home/ffink/.csgoatt.appstate"

    def save(self):
        data = {
            "last_log_file_locations": self.last_log_file_locations,
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
        data = {}
        try:
            with open(self.file, "r") as f:
                data = json.loads(f.read())
        except Exception as e:
            print(f"failed to read persistant appstate from disk: {e}")
            data = {
                "last_log_file_locations": [],
                "last_app_appearance": "System",
                "last_target_lang": "de",
                "last_color_theme": "blue"
            }

        self.last_app_appearance = data["last_app_appearance"]
        self.last_color_theme = data["last_color_theme"]
        self.last_log_file_locations = data["last_log_file_locations"][0:3]
        self.last_target_lang = data["last_target_lang"]
        