# libretro.h

from ctypes import *
from enum import IntEnum, IntFlag
from typing import Callable, List

# region 301 - 323

class MEMORY(IntEnum):
    MASK = 0xFF
    SAVE_RAM = 0
    RTC = 1
    SYSTEM_RAM = 2
    VIDEO_RAM = 3

# endregion

# region 2121 - 2282

class MEMDESC(IntFlag):
    CONST      = (1 << 0)
    BIGENDIAN  = (1 << 1)
    SYSTEM_RAM = (1 << 2)
    SAVE_RAM   = (1 << 3)
    VIDEO_RAM  = (1 << 4)
    ALIGN_2    = (1 << 16)
    ALIGN_4    = (2 << 16)
    ALIGN_8    = (3 << 16)
    MINSIZE_2  = (1 << 24)
    MINSIZE_4  = (2 << 24)
    MINSIZE_8  = (3 << 24)

class retro_memory_descriptor(Structure):
    _fields_ = [
        ('flags', c_uint64),
        ('ptr', c_void_p),
        ('offset', c_size_t),
        ('start', c_size_t),
        ('select', c_size_t),
        ('disconnect', c_size_t),
        ('len', c_size_t),
        ('addrspace', c_char_p)
    ]
    
    flags: c_uint64
    ptr: c_void_p
    offset: c_size_t
    start: c_size_t
    select: c_size_t
    disconnect: c_size_t
    len: c_size_t
    addrspace: c_char_p
    
class retro_memory_map(Structure):
    _fields_ = [
        ('descriptors', POINTER(retro_memory_descriptor)),
        ('num_descriptors', c_uint)
    ]

    descriptors: POINTER(retro_memory_descriptor)
    num_descriptors: c_uint

# endregion
