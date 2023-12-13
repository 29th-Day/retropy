from ctypes import *
from enum import IntEnum
from typing import Callable


class GameInfoExt(Structure):
    """retro_game_info_ext"""

    _fields_ = [
        ("full_path", c_char_p),
        ("archive_path", c_char_p),
        ("archive_file", c_char_p),
        ("dir", c_char_p),
        ("name", c_char_p),
        ("ext", c_char_p),
        ("meta", c_char_p),
        ("data", c_void_p),
        ("size", c_size_t),
        ("file_in_archive", c_bool),
        ("persistent_data", c_bool),
    ]

    full_path: bytes
    archive_path: bytes
    archive_file: bytes
    dir: bytes
    name: bytes
    ext: bytes
    meta: bytes
    data: c_void_p
    size: int
    file_in_archive: bool
    persistent_data: bool


class GameGeometry(Structure):
    """retro_game_geometry"""

    _fields_ = [
        ("base_width", c_uint),
        ("base_height", c_uint),
        ("max_width", c_uint),
        ("max_height", c_uint),
        ("aspect_ratio", c_float),
    ]

    base_width: int
    base_height: int
    max_width: int
    max_height: int
    aspect_ratio: float


class GameInfo(Structure):
    """retro_game_info"""

    _fields_ = [
        ("path", c_char_p),
        ("data", c_void_p),
        ("size", c_size_t),
        ("meta", c_char_p),
    ]

    path: bytes
    data: c_void_p
    size: int
    meta: bytes
