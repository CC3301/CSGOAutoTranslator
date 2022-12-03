class Options():
    def __init__(self):
        self.target_languages = ['de', 'en', 'ru', 'ja', 'tr']
        self.gui_config  = {
            "appearance_mode": "Dark",
            "default_color_theme": "blue",
            "default_window_size": "800x400"
        }

        # refresh interval of csgo chat messages
        self.refresh_interval = 1000