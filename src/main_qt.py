"""
GUI and Logic-Glue for CS:GO Autotranslator
"""

import sys
import logging
import signal
from PyQt6 import uic, QtWidgets, QtGui, QtCore

from lib.persistance import Persistance
from lib.csgologinterfacev2 import CSGOLogInterface
from lib.translationapi import TranslationAPI
from lib.message import Message


class CSGOAutoTranslate(QtWidgets.QMainWindow):
    """
    Main class for CS:GO AutoTranslator
    """
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(name=__class__.__name__)
        self.logger.info("Loading UI")
        try:
            uic.loadUi("ui/main.ui", self)
        except (uic.exceptions.NoSuchClassError,
                uic.exceptions.NoSuchWidgetError,
                uic.exceptions.UnsupportedPropertyError,
                uic.exceptions.WidgetPluginError
            ) as exception:
            self.logger.fatal(exception)
            sys.exit(1)
        self.logger.info("Loaded UI-File")

        self.translated_chat_message_model = QtGui.QStandardItemModel()
        self.original_chat_message_model = QtGui.QStandardItemModel()

        self.translated_chat_message_model.setHorizontalHeaderLabels(
            ["Translation", "Timestamp", "Player", "Message"]
        )
        self.original_chat_message_model.setHorizontalHeaderLabels(
            ["Translation", "Timestamp", "Player", "Message"]
        )

        self.translated_chat_table_view.setModel(self.translated_chat_message_model)
        self.original_chat_table_view.setModel(self.original_chat_message_model)

        self.__setup_helpers()
        self.__connect_handlers()

        self.connection_state_label.setText(self.csloginterface.netconport)
        self.target_translation_language_combobox.addItems(
            self.translationapi.possible_target_languages
        )

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
        self.message_refresh_timer = QtCore.QTimer(self)
        self.message_refresh_timer.setInterval(500)
        self.message_refresh_timer.timeout.connect(self.__poll_new_messages)
        self.message_refresh_timer.start()

    def __connect_handlers(self) -> None:
        self.actionQuit.triggered.connect(self.__quit_gui)
        self.flush_chatboxes_button.clicked.connect(self.__flush_chatboxes)
        self.csgo_rcon_port_input.returnPressed.connect(self.__update_csgo_rcon_port)
        self.target_translation_language_combobox.currentTextChanged.connect(
            self.__update_target_translation_language
        )

        # Signal Handlers
        signal.signal(signal.SIGINT, self.__handler_sigint)

    def closeEvent(self, event: QtGui.QCloseEvent):
        """
        Handles pressing of the 'close' button in the window bar
        """
        event.accept()
        self.__quit_gui()

    def __handler_sigint(self, signum: int, frame: str) -> None:
        self.logger.debug("Exiting on signal: %x (%s)", signum, frame)
        self.__quit_gui()

    def __quit_gui(self) -> None:
        self.logger.info("Exiting Application")
        self.destroy()
        self.persistance.save()
        sys.exit(0)

    def __flush_chatboxes(self) -> None:
        self.original_chat_message_model.clear()
        self.translated_chat_message_model.clear()
        self.translated_chat_message_model.setHorizontalHeaderLabels(
            ["Translation", "Timestamp", "Player", "Message"]
        )
        self.original_chat_message_model.setHorizontalHeaderLabels(
            ["Translation", "Timestamp", "Player", "Message"]
        )

    def __poll_new_messages(self) -> None:
        messages: [] = self.csloginterface.retrieve()
        count: int = len(messages)
        if count != 0:
            for message in messages:
                self.__append_message(self.translationapi.translate(message))
            self.logger.debug("Got %x new messages", count)

    def __append_message(self, message: Message) -> None:
        if message is not None:
            self.translated_chat_message_model.appendRow(
                QtGui.QStandardItem(i) for i in message.format_translated_table()
            )
            self.original_chat_message_model.appendRow(
                QtGui.QStandardItem(i) for i in message.format_original_table()
            )
            self.original_chat_message_model.index(
                self.original_chat_message_model.rowCount(),
                self.original_chat_message_model.columnCount()
            )


    def __update_target_translation_language(self, target_lang: str) -> None:
        self.logger.info("New Target Language: %s", target_lang)
        self.translationapi.set_target_lang(target_lang)
        self.persistance.last_target_lang = target_lang

    def __update_csgo_rcon_port(self) -> None:
        rcon_port = self.csgo_rcon_port_input.text()
        self.csloginterface.reconnect_to_other_port(rcon_port)
        self.persistance.last_rcon_port = rcon_port
        self.connection_state_label.setText(self.csloginterface.netconport)

    def start_gui(self) -> None:
        """
        Starts the GUI main loop
        """
        self.logger.info("Starting main GUI")
        self.show()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    window = CSGOAutoTranslate()
    window.start_gui()
    sys.exit(app.exec())
