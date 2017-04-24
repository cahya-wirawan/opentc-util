import os
import sys
import logging
import socket
import struct
import yaml


def setup_logging(
        config_directories=None,
        config_file=None,
        default_level=logging.INFO,
        default_filename="logging.yml"
):
    """Setup logging configuration

    """
    config_found = False
    config_file_path = None
    if config_file:
        config_file_path = config_file
        if os.path.isfile(config_file_path) and os.access(config_file_path, os.R_OK):
            config_found = True
    else:
        for directory in config_directories:
            if directory is None:
                continue
            config_file_path = os.path.join(directory, default_filename)
            if os.path.isfile(config_file_path) and os.access(config_file_path, os.R_OK):
                config_found = True
                break
    if config_found:
        with open(config_file_path, 'rt') as ymlfile:
            config = yaml.safe_load(ymlfile.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def setup_config(
        config_directories=None,
        config_file=None,
        default_filename="opentc.yml"
):
    """Setup configuration

    """
    config_found = False
    config_file_path = None
    if config_file:
        config_file_path = config_file
        if os.path.isfile(config_file_path) and os.access(config_file_path, os.R_OK):
            config_found = True
    else:
        for directory in config_directories:
            if directory is None:
                continue
            config_file_path = os.path.join(directory, default_filename)
            if os.path.isfile(config_file_path) and os.access(config_file_path, os.R_OK):
                config_found = True
                break
    if config_found:
        with open(config_file_path, 'rt') as ymlfile:
            config = yaml.safe_load(ymlfile.read())
        return config
    else:
        print("The configuration file is not found.")
        exit(1)


class SimpleSocket(object):
    max_data_size = 4096

    def __init__(self, address=None, port=None):
        self.logger = logging.getLogger(__name__)
        self._timeout = None
        self._address = address
        self._port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self._address, self._port))
        except ConnectionError as err:
            self.logger.error("{} to {}:{}".format(err, self._address, self._port, err))
            sys.exit()

    def close(self):
        self.logger.debug("Closing main socket")
        self._close_connection()

    def _close_connection(self):
        self.socket.close()

    def send(self, data):
        size = len(data)
        packed_header = struct.pack('=I', size)
        self.socket.sendall(packed_header + data)

    def receive(self):
        packed_header = self.socket.recv(4)
        (size, ) = struct.unpack('=I', packed_header)
        if size == 0 or size > self.max_data_size:
            return None
        data = self.socket.recv(size)
        return data