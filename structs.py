from ctypes import *
from typing import Callable

class retro_system_info(Structure):
    _fields_ = [
        ("library_name", c_char_p),
        ("library_version", c_char_p),
        ("need_fullpath", c_bool),
        ("valid_extensions", c_char_p)
    ]

    library_name: bytes
    library_version: bytes
    need_fullpath: bool
    valid_extensions: bytes

class retro_game_geometry(Structure):
    _fields_ = [
        ("base_width", c_uint32),
        ("base_height", c_uint32),
        ("max_width", c_uint32),
        ("max_height", c_uint32),
        ("aspect_ratio", c_float)
    ]

    base_width: int
    base_height: int
    max_width: int
    max_height: int
    aspect_ratio: float

class retro_system_timing(Structure):
    _fields_ = [
        ("fps", c_double),
        ("sample_rate", c_double)
    ]

    fps: float
    sample_rate: float

class retro_system_av_info(Structure):
    _fields_ = [
        ("geometry", retro_game_geometry),
        ("timing", retro_system_timing)
    ]

    geometry: retro_game_geometry
    timing: retro_system_timing

class retro_game_info(Structure):
    _fields_ = [
        ("path", c_char_p),
        ("data", c_char_p),
        ("size", c_size_t),
        ("meta", c_char_p)
    ]

    path: bytes
    data: bytes
    size: int
    meta: bytes

class retro_variable(Structure):
    _fields_ = [
        ("key", c_char_p),
        ("value", c_char_p)
    ]

    key: bytes
    value: bytes

class retro_input_descriptor(Structure):
    _fields_ = [
        ("port", c_uint32),
        ("device", c_uint32),
        ("index", c_uint32),
        ("id", c_uint32),
        ("description", c_char_p)
    ]

    port: int
    device: int
    index: int
    id: int
    description: bytes

class retro_log_callback(Structure):
    _fields_ = [
        ("log", c_void_p)
    ]

    log: Callable

class retro_audio_buffer_status_callback(Structure):
    _fields_ = [
        ("callback", c_void_p)
    ]

    callback: Callable

class retro_camera_callback(Structure):
    _fields_ = [
        ("caps", c_uint64),
        ("width", c_uint32),
        ("height", c_uint32),
        ("start", c_void_p),
        ("stop", c_void_p),
        ("frame_raw_framebuffer", c_void_p),
        ("frame_opengl_texture", c_void_p),
        ("initialized", c_void_p),
        ("deinitialized", c_void_p)
    ]

    caps: int
    width: int
    height: int
    start: Callable
    stop: Callable
    frame_raw_framebuffer: Callable
    frame_opengl_texture: Callable
    initialized: Callable
    deinitialized: Callable

class retro_memory_descriptor(Structure):
    _fields_ = [
        ("flags", c_uint64),
        ("ptr", c_void_p),
        ("offset", c_size_t),
        ("start", c_size_t),
        ("select", c_size_t),
        ("disconnect", c_size_t),
        ("len", c_size_t),
        ("addrspace", c_char_p)
    ]

    flags: int
    ptr: c_void_p
    offset: int
    start: int
    select: int
    disconnect: int
    len: int
    addrspace: bytes

class retro_memory_map(Structure):
    _fields_ = [
        ("descriptors", retro_memory_descriptor),
        ("num_descriptors", c_uint32)
    ]

    descriptors: retro_memory_descriptor
    num_descriptors: int