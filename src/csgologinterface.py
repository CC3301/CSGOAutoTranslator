import time
import threading
import os

from message import Message

class CSGOLogInterface():
    def __init__(self):
        self.path = ""
        self.file = None
        self.message_buffer = []   
        self.reader_thread = None
        self.__running = False

    def set_logpath(self, path):
        self.path = path
        self.file = open(self.path, "r")

    def read(self):
        self.file.seek(0, os.SEEK_END)
        while True:
            try:
                line = str(self.file.readline())
            except ValueError as e:
                break
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def start(self):
        if not self.file:
            return
        self.__running = True
        self.reader_thread = threading.Thread(target=self.__run)
        self.reader_thread.start()

    def stop(self):
        if not self.reader_thread:
            return
        self.__running = False
        self.file.close()
        self.reader_thread.join()

    def __run(self):
        for line in self.read():
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

                self.message_buffer.append(Message(m_sender, m_text, m_type, m_timestamp=time.time()))

    def retrieve(self):
        buffer = self.message_buffer
        self.message_buffer = []
        return buffer
    
    def retrieve_single(self):
        buffer = None
        if self.message_buffer:
            buffer = self.message_buffer[0]
            self.message_buffer.pop(0)
        return buffer
