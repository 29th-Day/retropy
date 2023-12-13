from ctypes import *
from enum import IntFlag, Enum


class PixelFormat(Enum):
    """retro_pixel_format"""

    RGB1555 = 0
    XRGB8888 = 1
    RGB565 = 2


class MEMORY_ACCESS(IntFlag):
    """RETRO_MEMORY_"""

    WRITE = 1 << 0
    READ = 1 << 1


class MEMORY_TYPE(IntFlag):
    """RETRO_MEMORY_TYPE_"""

    MEMORY_TYPE = 1 << 0


class Framebuffer(Structure):
    """retro_framebuffer"""

    _fields_ = [
        ("data", c_void_p),
        ("width", c_uint),
        ("height", c_uint),
        ("pitch", c_size_t),
        ("fromat", c_int32),
        ("access_flags", c_uint),
        ("memory_flags", c_uint),
    ]

    data: c_void_p
    width: int
    height: int
    pitch: int
    fromat: int
    access_flags: int
    memory_flags: int
