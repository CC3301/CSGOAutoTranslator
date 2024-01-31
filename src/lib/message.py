"""
Provides a Message Type and MessageFilter Class for filtering messages 
received by cs:go loginterface
"""

from datetime import datetime
import time
from enum import Enum

class MessageTypes(Enum):
    ALL  = 0
    TEAM = 1

class Message():
    """
    Message Object for later translation and storing
    """
    def __init__(self, m_sender: str, m_text: str, m_type: str):

        # message related variables
        self.m_sender = m_sender
        self.m_text = None
        self.m_original_text = m_text
        self.m_type = m_type
        self.m_timestamp = time.time()

        # translation related variables
        self.t_dst = None
        self.t_src = None

    def __format_helper_timestamp(self) -> str:
        return str(datetime.fromtimestamp(self.m_timestamp).strftime('%H:%M'))

    def __format_helper_sender(self) -> str:
        if self.m_type is MessageTypes.ALL:
            return f"{self.m_sender} @ ALL"
        else:
            return f"{self.m_sender}"

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
            m_type = MessageTypes.ALL
            sender_text_data = str(line).split(" : ")
            if len(sender_text_data) == 2:
                m_sender, m_text = sender_text_data
                m_text = m_text[:-1]

                if ")" in m_sender:
                    m_sender = m_sender.split(") ")[1]
                    m_text = m_text[1:]
                    m_type = MessageTypes.TEAM
                if "*DEAD*" in m_sender:
                    m_sender = m_sender[7:]

                if " @ " in m_sender:
                    m_sender = m_sender.split("@ ")[0]

                return Message(m_sender, m_text, m_type)
