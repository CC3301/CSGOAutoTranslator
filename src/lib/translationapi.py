"""
Provices a replaceable interface to an arbitraty translation api, acts 
as a compat layer between translation module/api and cs:go ATT
"""

import logging
import googletrans
from lib.message import Message

logging.getLogger(name="TRANSLATIONAPI_google")


class TranslationAPI():
    """
    Functionality for translating messages
    """
    def __init__(self):
        self.target_lang = None
        self.translator = googletrans.Translator()
        self.possible_target_languages = [
            "de",
            "en"
        ]

    # update target lang, but only if it seems kind of valid
    def set_target_lang(self, target_lang):
        """
        Update the target language
        """
        if target_lang in self.possible_target_languages:
            self.target_lang = target_lang
        else:
            logging.warning("Failed to set target language: %s not allowed.", target_lang)

    def translate(self, message) -> Message:
        """
        Translates a Message() object
        """
        if self.target_lang is None:
            logging.warning("Cannot translate message without target language")
            return None
        logging.debug("Translating Message: %s", message.m_text)

        while not message.t_translated:
            self.__do_translation(message)

        logging.debug("Translation Result: %s", message.m_text)
        return message

    def __do_translation(self, message) -> bool:
        try:
            result = self.translator.translate(message.m_text, dest=self.target_lang)
            message.t_dst = self.target_lang
            message.t_src = result.src
            message.m_text = result.text
        # pylint: disable=broad-exception-caught # googletrans module does not provide Exception classes
        except Exception as exception:
            logging.warning(exception)
