import googletrans

import logging

logging.getLogger(name="TRANSLATIONAPI_google")


class TranslationAPI():
    def __init__(self):
        self.target_lang = None
        self.translator = googletrans.Translator()
        self.possible_target_languages = [
            "de",
            "en"
        ]

    # update target lang, but only if it seems kind of valid
    def set_target_lang(self, target_lang):
        self.target_lang = target_lang
    
    def translate(self, message):
        if self.target_lang == None:
            logging.warn("Cannot translate message without target language")
            return None
        logging.debug(f"Translating Message: {message.m_text}")

        while not message.t_translated:
            self.__do_translation(message)

        logging.debug(f"Translation Result: {message.m_text}")
        return message
    
    def __do_translation(self, message) -> bool:
        try:
            result = self.translator.translate(message.m_text, dest=self.target_lang)
            message.t_dst = self.target_lang
            message.t_src = result.src
            message.m_text = result.text
            message.t_translated = True
        except Exception as e:
            logging.warn(e)
            message.t_translated = False