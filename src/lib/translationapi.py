"""
Provices a replaceable interface to an arbitraty translation api, acts 
as a compat layer between translation module/api and cs:go ATT
"""

import logging
import googletrans
from lib.message import Message
import time


class TranslationAPI():
    """
    Functionality for translating messages
    """
    def __init__(self):
        self.logger = logging.getLogger(name=__class__.__name__)
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
            self.logger.warning("Failed to set target language: %s not allowed.", target_lang)

    def translate(self, message) -> Message:
        """
        Translates a Message() object
        """
        if self.target_lang is None:
            self.logger.warning("Cannot translate message without target language")
            return None
        self.logger.debug("Translating Message: %s", message.m_original_text)

        while message.m_text is None:
            self.__do_translation(message)

        self.logger.debug("Translation Result: %s", message.m_text)
        return message

    def __do_translation(self, message):
        try:
            result = self.translator.translate(message.m_original_text, dest=self.target_lang)
            message.t_dst = self.target_lang
            message.t_src = result.src
            message.m_text = result.text
        # pylint: disable=broad-exception-caught # googletrans module does not provide Exception classes
        except Exception as exception:
            self.logger.warning(exception)
