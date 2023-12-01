# libretro.h

from enum import IntEnum
from ctypes import *
from typing import Callable, Any

# region 2390 - 2407

class RETRO_LOG_LEVEL(IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

retro_log_printf_t = CFUNCTYPE(None, c_int32, c_char_p)

class retro_log_callback(Structure):
    _fields_ = [
        ('log', retro_log_printf_t),
    ]

    log: Callable[[int, bytes, Any], None]

# endregion
