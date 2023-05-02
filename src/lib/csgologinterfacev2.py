"""
Provides interfacing with the cs:go rcon console
"""

import threading
import socket
import logging

from lib.message import MessageFilter


logging.getLogger(name="CSGOLOGINTERFACEv2")

class CSGOLogInterface():
    """
    Handles Interfacing with CS:GO's TCP log message stream
    """
    def __init__(self):
        self.netconport = None
        self.message_buffer = []
        self.message_filter = MessageFilter()
        self.reader_thread = None
        self.sock = None
        self.__no_read = False
        self.__running = False

    def is_connected(self):
        """
        Returns the current state of the connection to CS:GO
        """
        return bool(self.sock)

    def get_socket(self):
        """
        Tries to connect to cs:go's tcp socket
        """
        try:
            logging.debug("Attempting Connection to CSGO RCON at: 127.0.0.1: %s", {self.netconport})
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('127.0.0.1', int(self.netconport)))
            logging.debug("Connected to CSGO RCON")
        except socket.error as exception:
            self.sock = False
            logging.error(exception)

    def start(self, port):
        """
        Start the receiver thread
        """
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
        """
        Reconnect to a different CS:GO rcon port
        """
        self.__no_read = True
        self.netconport = port
        logging.debug("Reconnecting to CS:GO RCON port: %s", {self.netconport})
        self.get_socket()
        if not self.sock:
            logging.fatal("Re-Connect to 127.0.0.1:%s failed.", {self.netconport})
        else:
            self.__no_read = False

    def stop(self):
        """
        Stop the interface and disconnect from cs:go rcon
        """
        logging.info("Stopping CSGOLogInterface")
        logging.info("Disconnecting from RCON port")
        self.__running = False
        self.__no_read = True
        self.sock.close()
        self.reader_thread.join()

    def __run(self):
        while self.__running:
            if self.__no_read:
                continue
            line = self.sock.recv(1024)
            self.message_buffer.append(self.message_filter.filter_message(line.decode("utf-8")))

    def retrieve(self):
        """
        Returns all messages currently in the buffer
        """
        buffer = self.message_buffer
        self.message_buffer = []
        return buffer

    def retrieve_single(self):
        """
        Returns a single message from the buffer
        """
        buffer = None
        if self.message_buffer:
            buffer = self.message_buffer[0]
            self.message_buffer.pop(0)
        return buffer
