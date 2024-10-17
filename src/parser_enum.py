from enum import Enum, auto


class Parser_Error(Enum):
    NOT_EXIST_FILE = auto()
    FAIL_LOAD_FILE = auto()


class Status(Enum):
    START = "===============================================================================\n[START]"
    END = "[END]"
