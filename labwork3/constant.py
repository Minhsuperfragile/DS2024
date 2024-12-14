from enum import Enum

# Constants for signals and buffer size
SIGNALSIZE = 64
BUFFERSIZE = 1024
FILE_NAME_TAG = 1
FILE_CHUNK_TAG = 2
SIGNAL_TAG = 3
ERROR_TAG = 4

class Signal(Enum):
    SEND_A_FILE = b'SEND_A_FILE'
    REQUEST_A_FILE = b'REQUEST_A_FILE'
    DONE = b'DONE'
    ERROR = b'ERROR'
    PING = b'PING'
    PONG = b'PONG'