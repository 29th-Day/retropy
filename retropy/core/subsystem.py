# libretro.h

from ctypes import *
from typing import List

# region 2316 - 2365

class retro_subsystem_memory_info(Structure):
    _fields_ = [
        ('extension', c_char_p),
        ('type', c_uint)
    ]

    extension: c_char_p
    type: c_uint

class retro_subsystem_rom_info(Structure):
    _fields_ = [
        ('desc', c_char_p),
        ('valid_extensions', c_char_p),
        ('need_fullpath', c_bool),
        ('block_extract', c_bool),
        ('required', c_bool),
        ('memory', POINTER(retro_subsystem_memory_info)),
        ('num_memory', c_uint)
    ]

    desc: c_char_p
    valid_extensions: c_char_p
    need_fullpath: c_bool
    block_extract: c_bool
    required: c_bool
    memory: POINTER(retro_subsystem_memory_info)
    num_memory: c_uint

class retro_subsystem_info(Structure):
    _fields_ = [
        ('desc', c_char_p),
        ('indent', c_char_p),
        ('roms', POINTER(retro_subsystem_rom_info)),
        ('num_roms', c_uint),
        ('id', c_uint)
    ]

    desc: c_char_p
    indent: bytes
    roms: POINTER(retro_subsystem_rom_info)
    num_roms: c_uint
    id: c_uint

# endregion
