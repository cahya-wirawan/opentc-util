import os
import time
import logging
import json
from opentc.util import SimpleSocket


class Client(object):
    max_chunk_size = 1024

    def __init__(self, address='localhost', port=3333):
        self.address = address
        self.port = port

    def command(self, command=None):
        logger = logging.getLogger(__name__)
        simple_socket = None
        try:
            simple_socket = SimpleSocket(address=self.address, port=self.port)
            simple_socket.send(command.encode('utf-8'))
            response = simple_socket.receive()
            logger.debug("command Received: {}".format(response))
            return response
        except ConnectionError as err:
            logger.error("OS error: {0}".format(err))
            raise
        finally:
            simple_socket.close()

    def ping(self):
        logger = logging.getLogger(__name__)
        simple_socket = None
        try:
            mid = str(time.time())
            command = "PING:{}\n".format(mid)
            simple_socket = SimpleSocket(address=self.address, port=self.port)
            simple_socket.send(command.encode('utf-8'))
            logger.debug("Ping send mid: {}".format(mid))
            response = None
            while response is None:
                response = simple_socket.receive()
            logger.debug("Ping response: {}, mid sent: {}".format(response, mid))
            return response
        except ConnectionError as err:
            logger.error("OS error: {0}".format(err))
            raise
        finally:
            simple_socket.close()

    def md5_file(self, file_name=None):
        # This function is just for testing purpose
        logger = logging.getLogger(__name__)
        simple_socket = None
        try:
            statinfo = os.stat(file_name)
            simple_socket = SimpleSocket(address=self.address, port=self.port)
            if statinfo is not None:
                command = "MD5_FILE:{}\n".format(file_name)
                simple_socket.send(command.encode('utf-8'))
                response = simple_socket.receive()
                logger.debug("Client Received: {}".format(response))
                return response
            else:
                return None
        except OSError as err:
            logger.error("OS error: {0}".format(err))
        finally:
            simple_socket.close()

    def md5_stream(self, data=None):
        # This function is just for testing purpose
        logger = logging.getLogger(__name__)
        simple_socket = None
        try:
            command = "MD5_STREAM\n"
            simple_socket = SimpleSocket(address=self.address, port=self.port)
            simple_socket.send(command.encode('utf-8'))
            data_len = len(data)
            start_pos = 0
            end_pos = self.max_chunk_size
            while start_pos < data_len:
                end_pos = min(end_pos, data_len)
                simple_socket.send(data[start_pos:end_pos])
                start_pos += self.max_chunk_size
                end_pos += self.max_chunk_size
            simple_socket.send(b'')
            response = simple_socket.receive()
            logger.debug("Client Received: {}".format(response))
            return response
        except OSError as err:
            logger.error("OS error: {0}".format(err))
        finally:
            simple_socket.close()

    def predict_stream(self, data=None):
        logger = logging.getLogger(__name__)
        simple_socket = None
        try:
            mid = str(time.time())
            command = "PREDICT_STREAM:{}\n".format(mid)
            simple_socket = SimpleSocket(address=self.address, port=self.port)
            simple_socket.send(command.encode('utf-8'))
            data_len = len(data)
            start_pos = 0
            end_pos = self.max_chunk_size
            while start_pos < data_len:
                end_pos = min(end_pos, data_len)
                simple_socket.send(data[start_pos:end_pos])
                start_pos += self.max_chunk_size
                end_pos += self.max_chunk_size
            simple_socket.send(b'')
            response = simple_socket.receive()
            response_str = json.loads(response.decode('utf-8'))
            logger.debug("Client Received: {}, mid sent: {}".format(response, mid))
            if response_str["mid"] == mid:
                return response
            else:
                return None
        except OSError as err:
            logger.error("OS error: {0}".format(err))
        finally:
            simple_socket.close()

    def predict_file(self, file_name=None):
        logger = logging.getLogger(__name__)
        simple_socket = None
        try:
            mid = str(time.time())
            simple_socket = SimpleSocket(address=self.address, port=self.port)
            statinfo = os.stat(file_name)
            if statinfo is not None:
                command = "PREDICT_FILE:{}:{}\n".format(mid, file_name)
                simple_socket.send(command.encode('utf-8'))
                response = simple_socket.receive()
                logger.debug("Client Received: {}, mid sent: {}".format(response, mid))
                return response
            else:
                return None
        except OSError as err:
            logger.error("OS error: {0}".format(err))
        finally:
            simple_socket.close()

    def set_classifier(self, classifier=None, value=None):
        logger = logging.getLogger(__name__)
        simple_socket = None
        try:
            command = "SET_CLASSIFIER:{}:{}\n".format(classifier, value)
            simple_socket = SimpleSocket(address=self.address, port=self.port)
            simple_socket.send(command.encode('utf-8'))
            response = simple_socket.receive()
            logger.debug("Client Received: {}".format(response))
            return response
        except OSError as err:
            logger.error("OS error: {0}".format(err))
        finally:
            simple_socket.close()
