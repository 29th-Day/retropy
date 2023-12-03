from ctypes import *
from enum import IntEnum
from typing import Callable

from ..game import GameGeometry


class SystemInfo(Structure):
    """retro_system_info"""

    _fields_ = [
        ("library_name", c_char_p),
        ("library_version", c_char_p),
        ("valid_extensions", c_char_p),
        ("need_fullpath", c_bool),
        ("block_extract", c_bool),
    ]

    library_name: bytes
    library_version: bytes
    valid_extensions: bytes
    need_fullpath: bool
    block_extract: bool


class SystemContenInfoOverride(Structure):
    """retro_system_content_info_override"""

    _fields_ = [
        ("extensions", c_char_p),
        ("need_fullpath", c_bool),
        ("persistent_data", c_bool),
    ]

    extensions: bytes
    need_fullpath: bool
    persistent_data: bool


class SystemTiming(Structure):
    """retro_system_timing"""

    _fields_ = [("fps", c_double), ("sample_rate", c_double)]

    fps: float
    sample_rate: float


class SystemAvInfo(Structure):
    """retro_system_av_info"""

    _fields_ = [("geometry", GameGeometry), ("timing", SystemTiming)]

    geometry: GameGeometry
    timing: SystemTiming


# endregion
