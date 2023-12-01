from ctypes import *
from typing import Callable








class retro_game_info(Structure):
    _fields_ = [
        ("path", c_char_p),
        ("data", c_char_p),
        ("size", c_size_t),
        ("meta", c_char_p)
    ]

    path: bytes
    data: bytes
    size: int
    meta: bytes



class retro_log_callback(Structure):
    _fields_ = [
        ("log", c_void_p)
    ]

    log: Callable

class retro_audio_buffer_status_callback(Structure):
    _fields_ = [
        ("callback", c_void_p)
    ]

    callback: Callable
