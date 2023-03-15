from datetime import datetime

class Message():
    def __init__(self, m_sender: str, m_text: str, m_type: str, m_timestamp: str, t_dst: str=None, t_src: str=None):

        # message related variables
        self.m_sender = m_sender
        self.m_text = m_text
        self.m_original_text = m_text
        self.m_type = m_type
        self.m_timestamp = m_timestamp

        # translation related variables
        self.t_dst = t_dst
        self.t_src = t_src
        self.t_translated = False

    def __format_helper_timestamp(self) -> str:
        return str(datetime.fromtimestamp(self.m_timestamp).strftime('%H:%M'))
    
    def __format_helper_sender(self) -> str:
        return f"{self.m_sender} @ {self.m_type.upper()}"
      
    def format_original_table(self) -> list[str]:
        return [self.t_src, self.__format_helper_timestamp(), self.__format_helper_sender(), self.m_original_text]
    def format_translated_table(self) -> list[str]:
        return [f"{self.t_src.upper()} -> {self.t_dst.upper()}", self.__format_helper_timestamp(), self.__format_helper_sender(), self.m_text]