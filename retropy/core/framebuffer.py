# libretro.h

from ctypes import *
from enum import IntEnum, IntFlag, Enum
from typing import Callable

# region 2367

retro_proc_address_t = CFUNCTYPE(None)

# endregion

# region 2772 - 2910

HW_FRAME_BUFFER_VALID = ... # ? ((void*)-1)

retro_hw_context_reset_t = CFUNCTYPE(None)
retro_hw_get_current_framebuffer_t = CFUNCTYPE(c_ulonglong)
retro_hw_get_proc_address_t = CFUNCTYPE(retro_proc_address_t, c_char_p)

class HW_CONTEXT_TYPE(IntEnum):
    RETRO_HW_CONTEXT_NONE             = 0
    RETRO_HW_CONTEXT_OPENGL           = 1
    RETRO_HW_CONTEXT_OPENGLES2        = 2
    RETRO_HW_CONTEXT_OPENGL_CORE      = 3
    RETRO_HW_CONTEXT_OPENGLES3        = 4
    RETRO_HW_CONTEXT_OPENGLES_VERSION = 5
    RETRO_HW_CONTEXT_VULKAN           = 6
    RETRO_HW_CONTEXT_D3D11            = 7
    RETRO_HW_CONTEXT_D3D10            = 8
    RETRO_HW_CONTEXT_D3D12            = 9
    RETRO_HW_CONTEXT_D3D9             = 10

class retro_hw_render_callback(Structure):
    _fields_ = [
        ('context_type', c_int32),
        ('context_reset', retro_hw_context_reset_t),
        ('get_current_framebuffer', retro_hw_get_current_framebuffer_t),
        ('get_proc_address', retro_hw_get_proc_address_t),
        ('depth', c_bool),
        ('stencil', c_bool),
        ('bottom_left_origin', c_bool),
        ('version_major', c_uint),
        ('version_minor', c_uint),
        ('cache_context', c_bool),
        ('context_destroy', retro_hw_context_reset_t),
        ('debug_context', c_bool)
    ]

    context_type: c_int32
    context_reset: Callable[[None], None]
    get_current_framebuffer: Callable[[None], c_ulonglong]
    get_proc_address: Callable[[c_char_p], Callable[[None], None]]
    depth: c_bool
    stencil: bool
    bottom_left_origin: c_bool
    version_major: c_uint
    version_minor: c_uint
    cache_context: c_bool
    context_destroy: Callable[[None], None]
    debug_context: c_bool

# endregion

# region 3189 - 3211

class PIXEL_FORMAT(Enum):
    RGB1555  = 0
    XRGB8888 = 1
    RGB565   = 2
    
# endregion

# region 3883 - 3911

class MEMORY_ACCESS(IntFlag):
    WRITE = (1 << 0)
    READ = (1 << 1)

class MEMORY_TYPE(IntFlag):
    MEMORY_TYPE = (1 << 0)

# RETRO_MEMORY_ACCESS_WRITE = (1 << 0)
# RETRO_MEMORY_ACCESS_READ = (1 << 1)
# RETRO_MEMORY_TYPE_CACHED = (1 << 0)

class retro_framebuffer(Structure):
    _fields_ = [
        ('data', c_void_p),
        ('width', c_uint),
        ('height', c_uint),
        ('pitch', c_size_t),
        ('fromat', c_int32),
        ('access_flags', c_uint),
        ('memory_flags', c_uint),
    ]

    data: c_void_p
    width: c_uint
    height: c_uint
    pitch: c_size_t
    fromat: c_int32
    access_flags: c_uint
    memory_flags: c_uint

# endregion
