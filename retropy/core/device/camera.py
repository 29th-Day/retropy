from ctypes import *
from enum import IntFlag
from typing import Callable


class BufferType(IntFlag):
    """retro_camera_buffer"""

    OPENGL_TEXTURE = 1 << 0
    RAW_FRAMEBUFFER = 1 << 1


camera_start_t = CFUNCTYPE(c_bool)
"""retro_camera_start_t"""

camera_stop_t = CFUNCTYPE(None)
"""retro_camera_stop_t"""

camera_lifetime_status_t = CFUNCTYPE(None)
"""retro_camera_lifetime_status_t"""

camera_frame_raw_framebuffer_t = CFUNCTYPE(
    None, POINTER(c_uint32), c_uint, c_uint, c_size_t
)
"""retro_camera_frame_raw_framebuffer_t"""

camera_frame_opengl_texture_t = CFUNCTYPE(None, c_uint, c_uint, POINTER(c_float))
"""retro_camera_frame_opengl_texture_t"""


class CameraCallback(Structure):
    """retro_camera_callback"""

    _fields_ = [
        ("caps", c_uint64),
        ("width", c_uint),
        ("height", c_uint),
        ("start", camera_start_t),
        ("stop", camera_stop_t),
        ("frame_raw_framebuffer", camera_frame_raw_framebuffer_t),
        ("frame_opengl_texture", camera_frame_opengl_texture_t),
        ("initialized", camera_lifetime_status_t),
        ("deinitialized", camera_lifetime_status_t),
    ]

    caps: int
    width: int
    height: int
    start: Callable[[None], bool]
    stop: Callable[[None], None]
    frame_raw_framebuffer: Callable[[POINTER(c_uint32), int, int, int], None]
    frame_opengl_texture: Callable[[int, int, POINTER(c_float)], None]
    initialized: Callable[[None], None]
    deinitialized: Callable[[None], None]
