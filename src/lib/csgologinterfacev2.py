import threading
import socket
import time
import sys

from lib.message import Message

import logging

logging.getLogger(name="CSGOLOGINTERFACEv2")
logging.basicConfig(level=logging.DEBUG)

class CSGOLogInterface():
    def __init__(self):
        self.netconport = None
        self.message_buffer = []   
        self.reader_thread = None
        self.sock = None

    def get_socket(self):
        try:
            logging.debug(f"Attempting Connection to CSGO RCON at: 127.0.0.1:{self.netconport}")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('127.0.0.1', int(self.netconport)))
            logging.debug("Connected to CSGO RCON")
        except Exception as e:
            self.sock = False
            logging.error(e)

    def start(self, port):
        logging.debug("Starting v2 CSGOLogInterface")
        self.netconport = port
        self.get_socket()
        if not self.sock:
            logging.error("Failed to start v2 CSGOLogInterface: no socket")
            return
        self.__running = True
        self.reader_thread = threading.Thread(target=self.__run, daemon=True)
        logging.info("Starting CS:GO log filtering and processing")
        self.reader_thread.start()

    def reconnect_to_other_port(self, port):
        self.netconport = port
        logging.debug(f"Reconnecting to CS:GO RCON port: {self.netconport}")
        self.get_socket()

    def stop(self):
        logging.info("Stopping CSGOLogInterface")
        logging.info("Disconnecting from RCON port")
        self.sock.close()

    def __run(self):
        while self.__running:
            line = self.sock.recv(1024)
            logging.debug(f"read from socket: {line}")
            self.__extract_message_from_read_line(line.decode("utf-8"))

    def __extract_message_from_read_line(self, line):
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
