from ctypes import *
from enum import Enum, IntFlag


class MEMORY(Enum):
    """RETRO_MEMORY_"""

    MASK = 0xFF
    SAVE_RAM = 0
    RTC = 1
    SYSTEM_RAM = 2
    VIDEO_RAM = 3


class MEMDESC(IntFlag):
    """RETRO_MEMDESC_"""

    CONST = 1 << 0
    BIGENDIAN = 1 << 1
    SYSTEM_RAM = 1 << 2
    SAVE_RAM = 1 << 3
    VIDEO_RAM = 1 << 4
    ALIGN_2 = 1 << 16
    ALIGN_4 = 2 << 16
    ALIGN_8 = 3 << 16
    MINSIZE_2 = 1 << 24
    MINSIZE_4 = 2 << 24
    MINSIZE_8 = 3 << 24


class MemoryDescriptor(Structure):
    """retro_memory_descriptor"""

    _fields_ = [
        ("flags", c_uint64),
        ("ptr", c_void_p),
        ("offset", c_size_t),
        ("start", c_size_t),
        ("select", c_size_t),
        ("disconnect", c_size_t),
        ("len", c_size_t),
        ("addrspace", c_char_p),
    ]

    flags: int
    ptr: c_void_p
    offset: int
    start: int
    select: int
    disconnect: int
    len: int
    addrspace: bytes


class MemoryMap(Structure):
    """retro_memory_map"""

    _fields_ = [
        ("descriptors", POINTER(MemoryDescriptor)),
        ("num_descriptors", c_uint),
    ]

    descriptors: POINTER(MemoryDescriptor)
    num_descriptors: int
