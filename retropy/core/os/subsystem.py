from ctypes import *
from typing import List


class SubystemMemoryInfo(Structure):
    """retro_subsystem_memory_info"""

    _fields_ = [("extension", c_char_p), ("type", c_uint)]

    extension: bytes
    type: int


class SubsystemRomInfo(Structure):
    """retro_subsystem_rom_info"""

    _fields_ = [
        ("desc", c_char_p),
        ("valid_extensions", c_char_p),
        ("need_fullpath", c_bool),
        ("block_extract", c_bool),
        ("required", c_bool),
        ("memory", POINTER(SubystemMemoryInfo)),
        ("num_memory", c_uint),
    ]

    desc: bytes
    valid_extensions: bytes
    need_fullpath: bool
    block_extract: bool
    required: bool
    memory: POINTER(SubystemMemoryInfo)
    num_memory: int


class SubsystemInfo(Structure):
    """retro_subsystem_info"""

    _fields_ = [
        ("desc", c_char_p),
        ("indent", c_char_p),
        ("roms", POINTER(SubsystemRomInfo)),
        ("num_roms", c_uint),
        ("id", c_uint),
    ]

    desc: bytes
    indent: bytes
    roms: POINTER(SubsystemRomInfo)
    num_roms: int
    id: int
