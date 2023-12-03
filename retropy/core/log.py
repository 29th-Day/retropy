from enum import Enum
from ctypes import *
from typing import Callable, Any


class LogLevel(Enum):
    """RETRO_LOG_LEVEL"""

    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3


log_printf_t = CFUNCTYPE(None, c_int32, c_char_p)
"""retro_log_printf_t"""


class LogCallback(Structure):
    """retro_log_callback"""

    _fields_ = [
        ("log", log_printf_t),
    ]

    log: Callable[[int, bytes, Any], None]
