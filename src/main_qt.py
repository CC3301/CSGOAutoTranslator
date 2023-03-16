from PyQt5 import uic, QtWidgets, QtGui, QtCore
import sys

from lib.persistance import Persistance
from lib.csgologinterfacev2 import CSGOLogInterface
from lib.translationapi import TranslationAPI
from lib.message import Message

import logging
logging.getLogger(name="CSGOAutoTranslate")
logging.basicConfig(level=logging.DEBUG)

class CSGOAutoTranslate(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(CSGOAutoTranslate, self).__init__()

        logging.info("Loading UI")
        try:
            uic.loadUi("ui/main.ui", self)
        except Exception as e:
            logging.fatal(e)
            sys.exit(1)
        logging.info("Loaded UI-File")

        self.translated_chat_message_model = QtGui.QStandardItemModel()
        self.original_chat_message_model = QtGui.QStandardItemModel()

        self.translated_chat_message_model.setHorizontalHeaderLabels(["Translation", "Timestamp", "Player", "Message"])
        self.original_chat_message_model.setHorizontalHeaderLabels(["Translation", "Timestamp", "Player", "Message"])

        self.translated_chat_table_view.setModel(self.translated_chat_message_model)
        self.original_chat_table_view.setModel(self.original_chat_message_model)

        self.__setup_helpers()
        self.__connect_handlers()

        self.connection_state_label.setText(self.csloginterface.connection_state)
        self.target_translation_language_combobox.addItems(self.translationapi.possible_target_languages)

    def __setup_helpers(self) -> None:
        self.persistance = Persistance()
        self.persistance.read()
        self.csloginterface = CSGOLogInterface()
        self.csloginterface.start(self.persistance.last_rcon_port)
        self.translationapi = TranslationAPI()
        self.translationapi.set_target_lang(self.persistance.last_target_lang)

        self.csgo_rcon_port_input.setText(self.persistance.last_rcon_port)
        self.target_translation_language_combobox.setCurrentText(self.persistance.last_target_lang)

        # message polling timer
        self.messageRefreshTimer = QtCore.QTimer(self)
        self.messageRefreshTimer.setInterval(500)
        self.messageRefreshTimer.timeout.connect(self.__poll_new_messages)
        self.messageRefreshTimer.start()

    def __connect_handlers(self) -> None:
        self.actionQuit.triggered.connect(self.__quit_gui)
        self.flush_chatboxes_button.clicked.connect(self.__flush_chatboxes)
        self.csgo_rcon_port_input.returnPressed.connect(self.__update_csgo_rcon_port)
        self.target_translation_language_combobox.currentTextChanged.connect(self.__update_target_translation_language)

    def __quit_gui(self) -> None:
        logging.info("Exiting Application")
        self.destroy()
        self.persistance.save()
        sys.exit(0)

    def __flush_chatboxes(self) -> None:
        self.original_chat_message_model.clear()
        self.translated_chat_message_model.clear()

    def __poll_new_messages(self) -> None:
        for m in self.csloginterface.retrieve():
            self.__append_message(self.translationapi.translate(m))

    def __append_message(self, message: Message) -> None:
        if message != None:
            self.translated_chat_message_model.appendRow(QtGui.QStandardItem(i) for i in message.format_translated_table())
            self.original_chat_message_model.appendRow(QtGui.QStandardItem(i) for i in message.format_original_table())

    def __update_target_translation_language(self, s) -> None:
        self.translationapi.set_target_lang(s)
        self.persistance.last_target_lang = s
        logging.info(f"Changed Target language to: {s}")

    def __update_csgo_rcon_port(self) -> None:
        rcon_port = self.csgo_rcon_port_input.text()
        self.csloginterface.reconnect_to_other_port(rcon_port)
        self.persistance.last_rcon_port = rcon_port
        self.connection_state_label.setText(self.csloginterface.connection_state)

    def startGUI(self) -> None:
        logging.info("Starting main GUI")
        self.show()        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CSGOAutoTranslate()
    window.startGUI()
    sys.exit(app.exec())