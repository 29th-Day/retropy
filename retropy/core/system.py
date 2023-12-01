# libretro.py

from ctypes import *
from enum import IntEnum
from typing import Callable

from .game import retro_game_geometry

# region 3363 - 3514

class retro_system_info(Structure):
    _fields_ = [
        ('library_name', c_char_p),
        ('library_version', c_char_p),
        ('valid_extensions', c_char_p),
        ('need_fullpath', c_bool),
        ('block_extract', c_bool),
    ]

    library_name: bytes
    library_version: bytes
    valid_extensions: bytes
    need_fullpath: bool
    block_extract: bool

class retro_system_content_info_override(Structure):
    _fields_ = [
        ('extensions', c_char_p),
        ('need_fullpath', c_bool),
        ('persistent_data', c_bool),
    ]

    extensions: c_char_p
    need_fullpath: c_bool
    persistent_data: c_bool

# endregion

# region 3629 - 3639

class retro_system_timing(Structure):
    _fields_ = [
        ('fps', c_double),
        ('sample_rate', c_double)
    ]

    fps: c_double
    sample_rate: c_double

class retro_system_av_info(Structure):
    _fields_ = [
        ('geometry', retro_game_geometry),
        ('timing', retro_system_timing)
    ]

    geometry: retro_game_geometry
    timing: retro_system_timing


# endregion
