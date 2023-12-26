from ctypes import *
from enum import Enum, IntFlag, IntEnum

from typing import Sequence


class MemoryRegion(IntEnum):
    """RETRO_MEMORY_"""

    # MASK = 0xFF
    SAVE_RAM = 0
    """Memory typically on card ridge. Used to save games aka SRAM"""
    RTC = 1
    """Some card ridges have internal clocks."""
    SYSTEM_RAM = 2
    """Main system working RAM aka HRAM"""
    VIDEO_RAM = 3
    """Main system video RAM aka VRAM, WRAM"""


class MemoryFlags(IntFlag):
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

    def __repr__(self) -> str:
        return str(
            {
                "flags": MemoryFlags(self.flags),
                "ptr": f"0x{self.ptr:08X}",
                "offset": f"0x{self.offset:08X}",
                "start": f"0x{self.start:08X}",
                "select": f"0x{self.select:08X}",
                "disconnect": self.disconnect,
                "len": f"0x{self.len:08X}",
                "addrspace": self.addrspace
                if not self.addrspace
                else self.addrspace.decode(),
            }
        )


class MemoryMap(Structure):
    """retro_memory_map"""

    _fields_ = [
        ("descriptors", POINTER(MemoryDescriptor)),
        ("num_descriptors", c_uint),
    ]

    descriptors: POINTER(MemoryDescriptor)
    num_descriptors: int


"""
Maybe something like this can work

class MemoryMap(Structure):
    # retro_memory_map

    _fields_ = [
        ("descriptors", POINTER(MemoryDescriptor)),
        ("num_descriptors", c_uint),
    ]

    # descriptors: POINTER(MemoryDescriptor)
    num_descriptors: int

    @property
    def descriptors(self) -> Generator[MemoryDescriptor]:
        for i in range(self.num_descriptors):
            yield self.descriptors[i]
"""
