import os
import time
from datetime import datetime
import googletrans

from csgologinterface import CSGOLogInterface
from options import Options
from translationapi import TranslationAPI

from persistance import Persistance

import tkinter
import customtkinter

class CSGOAutoTranslateGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.opts = Options()
        self.translationapi = TranslationAPI()
        self.loginterface = CSGOLogInterface()
        self.persistance = Persistance()
        self.persistance.read()

    def gui_config(self):
        customtkinter.set_appearance_mode(self.persistance.last_app_appearance)
        customtkinter.set_default_color_theme(self.persistance.last_color_theme)

        self.geometry(f"{self.opts.gui_config['default_window_width']}x{self.opts.gui_config['default_window_height']}")
        self.minsize(1100, 580)

        self.__gui_construct()
        self.gui_post_construct_config()

    def gui_post_construct_config(self):
        pass

    def full_redraw(self):
        self.__gui_construct()

    def __gui_construct(self):
        self.title("CS:GO Auto Translator")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CS:GO AutoTranslator", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #---------------------------------------------------------------------#
        # Configure app appearance
        #---------------------------------------------------------------------#

        # make appearance mode configurable
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set(self.persistance.last_app_appearance)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(0, 20))

        # make color theme configurable
        self.color_theme_label = customtkinter.CTkLabel(self.sidebar_frame, text="Color Theme:", anchor="w")
        self.color_theme_label.grid(row=3, column=0, padx=20, pady=(0, 0))
        self.color_theme_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["blue", "dark-blue", "green"],
                                                                       command=self.change_color_theme_event)
        self.color_theme_optionmenu.set(self.persistance.last_color_theme)
        self.color_theme_optionmenu.grid(row=4, column=0, padx=20, pady=(0, 20))

        #---------------------------------------------------------------------#
        # CSGO Log and Translation settings
        #---------------------------------------------------------------------#

        # target language selection
        self.target_lang_select_box_label = customtkinter.CTkLabel(self.sidebar_frame, text="Translate to:", anchor="w")
        self.target_lang_select_box_label.grid(row=5, column=0, padx=20, pady=(0, 0))
        self.target_lang_select_box = customtkinter.CTkOptionMenu(self.sidebar_frame, values=self.opts.target_languages,
                                                                       command=self.update_translation_api_target_lang)
        self.target_lang_select_box.set(self.persistance.last_target_lang)
        self.target_lang_select_box.grid(row=6, column=0, padx=20, pady=(0, 20))

        # log file selection
        self.cslogpath_label = customtkinter.CTkLabel(self.sidebar_frame, text="CSGO Console Log:", anchor="w")
        self.cslogpath_label.grid(row=7, column=0, padx=20, pady=(0, 0))
        self.cslogpath_select_box = customtkinter.CTkOptionMenu(self.sidebar_frame, values=self.persistance.last_log_file_locations[::-1] + ["Open file.."],
                                                                       command=self.set_cslogpath, dynamic_resizing=False)
        if self.persistance.last_log_file_locations:
            self.cslogpath_select_box.set(self.persistance.last_log_file_locations[0])
        else:
            self.cslogpath_select_box.set("Open file..")
        self.cslogpath_select_box.grid(row=8, column=0, padx=20, pady=(0, 20))

        #---------------------------------------------------------------------#
        # Action buttons
        #---------------------------------------------------------------------#
        self.clear_chatboxes_button = customtkinter.CTkButton(self.sidebar_frame, text="Flush Chatbox", anchor="sw", command=self.__gui_construct_make_chatboxes)
        self.clear_chatboxes_button.grid(row=9, column=0, padx=20, pady=(0, 20), sticky="s")

        self.__gui_construct_make_chatboxes()

    def __gui_construct_make_chatboxes(self):
        #---------------------------------------------------------------------#
        # Log message textbox
        #---------------------------------------------------------------------#
        self.live_chat_tabview = customtkinter.CTkTabview(self)
        self.live_chatbox_trans_tab = self.live_chat_tabview.add("Translated Chat")
        self.live_chatbox_orig_tab = self.live_chat_tabview.add("Original Chat")

        self.live_chatbox_trans = customtkinter.CTkTextbox(self.live_chatbox_trans_tab, state="disabled", font=customtkinter.CTkFont(size=12, family="Liberation Mono"), width=800, height=460)
        self.live_chatbox_trans.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.live_chatbox_orig = customtkinter.CTkTextbox(self.live_chatbox_orig_tab, state="disabled", font=customtkinter.CTkFont(size=12, family="Liberation Mono"), width=800, height=460)
        self.live_chatbox_orig.grid(row=0, column=1, padx=20, pady=(10, 10))

        self.live_chat_tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew", rowspan=2)
        self.live_chat_tabview.set("Translated Chat")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.persistance.last_app_appearance = new_appearance_mode

    def change_color_theme_event(self, new_color_theme: str):
        customtkinter.set_default_color_theme(new_color_theme)
        self.persistance.last_color_theme = new_color_theme
        self.full_redraw()

    def update_translation_api_target_lang(self, new_target_lang: str):
        self.translationapi.set_target_lang(new_target_lang)
        self.persistance.last_target_lang = new_target_lang

    def set_cslogpath(self, cslogpath: str):
        if cslogpath == "Open file..":
            cslogpath = self.open_select_cslogpath()

        if cslogpath == "":
            return
        try:
            self.loginterface.set_logpath(cslogpath)
            self.loginterface.start()
            self.persistance.last_log_file_locations.append(cslogpath)
            if len(self.persistance.last_log_file_locations) > 3:
                self.persistance.last_log_file_locations.pop(0)
        except FileNotFoundError as e:
            self.error_popup(e)

    def open_select_cslogpath(self):
        self.cslogpath_select = customtkinter.CTkInputDialog(text="Enter the ABSOLUTE Path to your CS:GO Console log file: ", title="Select CS:GO Logfile")
        return self.cslogpath_select.get_input()

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

            self.live_chatbox_orig.configure(state="normal")
            self.live_chatbox_orig.insert("end", f"({str(message.m_type).upper()})\t({message.t_src})       [{datetime.fromtimestamp(message.m_timestamp).strftime('%H:%M')}] {message.m_sender}: {message.m_original_text}\n")
            self.live_chatbox_orig.yview_moveto(1)
            self.live_chatbox_orig.configure(state="disabled")

            self.live_chatbox_trans.configure(state="normal")
            self.live_chatbox_trans.insert("end", f"({str(message.m_type).upper()})\t({message.t_src} -> {message.t_dst}) [{datetime.fromtimestamp(message.m_timestamp).strftime('%H:%M')}] {message.m_sender}: {message.m_text}\n")
            self.live_chatbox_trans.yview_moveto(1)
            self.live_chatbox_trans.configure(state="disabled")

        self.after(self.opts.refresh_interval, self.refresh_translations)

    def run(self):
        self.after(self.opts.refresh_interval, self.refresh_translations)
        self.update_translation_api_target_lang("de")
        self.set_cslogpath(self.cslogpath_select_box.get())
        self.mainloop()
        self.loginterface.stop()
        self.persistance.save()


if __name__ == "__main__":
    gui = CSGOAutoTranslateGUI()
    gui.gui_config()
    gui.run()
