# libretro.h: 

from enum import IntEnum
from ctypes import *

# region 2028 - 2047

class retro_hw_render_interface_type(IntEnum):
    VULKAN     = 0
    D3D9       = 1
    D3D10      = 2
    D3D11      = 3
    D3D12      = 4
    GSKIT_PS2  = 5

class retro_hw_render_interface(Structure):
    _fields_ = [
        ('interface_type', c_int32),
        ('interface_version', c_uint)
    ]

    interface_type: c_int32
    interface_version: c_uint

# endregion

# region 2085 - 2097

# enum retro_hw_render_context_negotiation_interface_type
# struct retro_hw_render_context_negotiation_interface

# endregion
