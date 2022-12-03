import os
import time
from datetime import datetime
import googletrans

from csgologinterface import CSGOLogInterface
from options import Options
from translationapi import TranslationAPI

import tkinter
import customtkinter

class CSGOAutoTranslateGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.opts = Options()
        self.translationapi = TranslationAPI()
        self.loginterface = CSGOLogInterface()

    def gui_config(self):
        customtkinter.set_appearance_mode(self.opts.gui_config["appearance_mode"])
        customtkinter.set_default_color_theme(self.opts.gui_config["default_color_theme"])

        self.geometry(self.opts.gui_config["default_window_size"])

        self.__gui_construct()


    def __gui_construct(self):
        self.title("CS:GO Chat Translator")
        self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.live_chatbox = customtkinter.CTkTextbox(master=self, state="disabled")
        self.live_chatbox.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="nsew")

        # target language selection
        self.target_lang_select_box = customtkinter.CTkComboBox(master=self, values=self.opts.target_languages)
        self.target_lang_select_box.grid(row=1, column=0, padx=(20, 0), pady=20, sticky="ew")

        self.update_target_language_button = customtkinter.CTkButton(master=self, command=self.update_translation_api_target_lang, text="Update Target Language")
        self.update_target_language_button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        # log file selection
        self.cslogpath_open_button = customtkinter.CTkButton(master=self, text="Select CS:GO Console Log File", command=self.open_select_cslogpath)
        self.cslogpath_open_button.grid(row=1, column=2, padx=(0, 20), pady=20, sticky="ew")

    def update_translation_api_target_lang(self):
        self.translationapi.set_target_lang(self.target_lang_select_box.get())

    def open_select_cslogpath(self):
        self.cslogpath_select = customtkinter.CTkInputDialog(text="Enter the ABSOLUTE Path to your CS:GO Console log file: ", title="Select CS:GO Logfile")
        path = self.cslogpath_select.get_input()
        if path == "":
            return
        try:
            self.loginterface.set_logpath(path)
            self.loginterface.start()
        except FileNotFoundError as e:
            self.error_popup(e)

    def error_popup(self, error_messsage):
        error_window = customtkinter.CTkToplevel(self)
        error_window.geometry("400x200")
        error_window.title("ERROR")

        label = customtkinter.CTkLabel(master=error_window, text=error_messsage)
        label.pack()

        okbutton = customtkinter.CTkButton(master=error_window, text="OK", command=error_window.destroy)
        okbutton.pack()

    def refresh_translations(self):
        for message in self.loginterface.retrieve():
            message = self.translationapi.translate(message)
            self.live_chatbox.configure(state="normal")
            self.live_chatbox.insert("end", f"({str(message.m_type).upper()})\t[{datetime.fromtimestamp(message.m_timestamp).strftime('%H:%M')}] {message.m_sender}: {message.m_text} ({message.t_src} -> {message.t_dst})\n")
            self.live_chatbox.yview_moveto(1)
            self.live_chatbox.configure(state="disabled")

        self.after(self.opts.refresh_interval, self.refresh_translations)

    def run(self):
        self.after(self.opts.refresh_interval, self.refresh_translations)
        self.update_translation_api_target_lang()
        self.mainloop()
        self.loginterface.stop()


if __name__ == "__main__":
    gui = CSGOAutoTranslateGUI()
    gui.gui_config()
    gui.run()
