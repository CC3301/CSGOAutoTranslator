import googletrans
from message import Message


class TranslationAPI():
    def __init__(self):
        self.target_lang = None
        self.translator = googletrans.Translator()

    # update target lang, but only if it seems kind of valid
    def set_target_lang(self, target_lang):
        self.target_lang = target_lang
    
    def translate(self, message):
        if self.target_lang == None:
            return
        result = self.translator.translate(message.m_text, dest=self.target_lang)
        message.t_dst = self.target_lang
        message.t_src = result.src
        message.m_text = result.text

        return message