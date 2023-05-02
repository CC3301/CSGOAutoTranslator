"""
Provides a Message Type and MessageFilter Class for filtering messages 
received by cs:go loginterface
"""

from datetime import datetime
import time

class Message():
    """
    Message Object for later translation and storing
    """
    def __init__(self, m_sender: str, m_text: str, m_type: str):

        # message related variables
        self.m_sender = m_sender
        self.m_text = m_text
        self.m_original_text = m_text
        self.m_type = m_type
        self.m_timestamp = time.time()

        # translation related variables
        self.t_dst = None
        self.t_src = None

    def __format_helper_timestamp(self) -> str:
        return str(datetime.fromtimestamp(self.m_timestamp).strftime('%H:%M'))

    def __format_helper_sender(self) -> str:
        return f"{self.m_sender} @ {self.m_type.upper()}"

    def format_original_table(self) -> list[str]:
        """
        Return a string formatted to fit into the "original" chat tab
        """
        return [
            self.t_src,
            self.__format_helper_timestamp(),
            self.__format_helper_sender(),
            self.m_original_text
        ]

    def format_translated_table(self) -> list[str]:
        """
        Return a string formatted to fit into the "translated" chat tab
        """
        return [
            f"{self.t_src.upper()} -> {self.t_dst.upper()}",
            self.__format_helper_timestamp(),
            self.__format_helper_sender(),
            self.m_text
        ]


class MessageFilter():
    """
    Filters Raw lines coming from cs:go's console. Filters out relevant chat messages
    """
    def __init__(self):
        pass

    def filter_message(self, line: str) -> Message:
        """
        Filter a line received by cs:go
        """
        if " : " in line:
            m_type = "all"
            m_sender, m_text = str(line).split(" : ")
            m_text = m_text[:-1]

            if ")" in m_sender: 
                m_sender = m_sender.split(") ")[1]
                m_text = m_text[1:]
                m_type = "team"
            if "*DEAD*" in m_sender:
                m_sender = m_sender[7:]

            if " @ " in m_sender:
                m_sender = m_sender.split("@ ")[0]

        return Message(m_sender, m_text, m_type)
