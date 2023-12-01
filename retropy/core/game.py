# libretro.h

from ctypes import *
from enum import IntEnum
from typing import Callable

# region 2937 - 3080

# DISK (NOT IMPLEMENTED)

# endregion

# region 3516 - 3627

class retro_game_info_ext(Structure):
    _fields_ = [
        ('full_path', c_char_p),
        ('archive_path', c_char_p),
        ('archive_file', c_char_p),
        ('dir', c_char_p),
        ('name', c_char_p),
        ('ext', c_char_p),
        ('meta', c_char_p),
        ('data', c_void_p),
        ('size', c_size_t),
        ('file_in_archive', c_bool),
        ('persistent_data', c_bool),
    ]

    full_path: bytes
    archive_path: bytes
    archive_file: bytes
    dir: bytes
    name: bytes
    ext: bytes
    meta: bytes
    data: c_void_p
    size: c_size_t
    file_in_archive: c_bool
    persistent_data: c_bool

class retro_game_geometry(Structure):
    _fields_ = [
        ('base_width', c_uint),
        ('base_height', c_uint),
        ('max_width', c_uint),
        ('max_height', c_uint),
        ('aspect_ratio', c_float)
    ]

    base_width: c_uint
    base_height: c_uint
    max_width: c_uint
    max_height: c_uint
    aspect_ratio: c_float

# endregion

# region 3867 - 3881

class retro_game_info(Structure):
    _fields_ = [
        ('path', c_char_p),
        ('data', c_void_p),
        ('size', c_size_t),
        ('meta', c_char_p),
    ]

    path: bytes
    data: c_void_p
    size: int
    meta: bytes

# endregion
