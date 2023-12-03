from ctypes import *
from enum import IntFlag, Enum
from typing import Callable

proc_address_t = CFUNCTYPE(None)
"""retro_proc_address_t"""

HW_FRAME_BUFFER_VALID = ...  # ? ((void*)-1)

hw_context_reset_t = CFUNCTYPE(None)
"""retro_hw_context_reset_t"""

hw_get_current_framebuffer_t = CFUNCTYPE(c_ulonglong)
"""retro_hw_get_current_framebuffer_t"""

hw_get_proc_address_t = CFUNCTYPE(proc_address_t, c_char_p)
"""retro_hw_get_proc_address_t"""


class HW_CONTEXT_TYPE(Enum):
    """retro_hw_context_type"""

    NONE = 0
    OPENGL = 1
    OPENGLES2 = 2
    OPENGL_CORE = 3
    OPENGLES3 = 4
    OPENGLES_VERSION = 5
    VULKAN = 6
    D3D11 = 7
    D3D10 = 8
    D3D12 = 9
    D3D9 = 10


class HWRenderCallback(Structure):
    """retro_hw_render_callback"""

    _fields_ = [
        ("context_type", c_int32),
        ("context_reset", hw_context_reset_t),
        ("get_current_framebuffer", hw_get_current_framebuffer_t),
        ("get_proc_address", hw_get_proc_address_t),
        ("depth", c_bool),
        ("stencil", c_bool),
        ("bottom_left_origin", c_bool),
        ("version_major", c_uint),
        ("version_minor", c_uint),
        ("cache_context", c_bool),
        ("context_destroy", hw_context_reset_t),
        ("debug_context", c_bool),
    ]

    context_type: int
    context_reset: Callable[[None], None]
    get_current_framebuffer: Callable[[None], int]
    get_proc_address: Callable[[bytes], Callable[[None], None]]
    depth: bool
    stencil: bool
    bottom_left_origin: bool
    version_major: int
    version_minor: int
    cache_context: bool
    context_destroy: Callable[[None], None]
    debug_context: bool


class HWRenderInterfaceType(Enum):
    """retro_hw_render_interface_type"""

    VULKAN = 0
    D3D9 = 1
    D3D10 = 2
    D3D11 = 3
    D3D12 = 4
    GSKIT_PS2 = 5


class HWRenderInterface(Structure):
    """retro_hw_render_interface"""

    _fields_ = [("interface_type", c_int32), ("interface_version", c_uint)]

    interface_type: c_int32
    interface_version: c_uint


# enum retro_hw_render_context_negotiation_interface_type
# struct retro_hw_render_context_negotiation_interface
