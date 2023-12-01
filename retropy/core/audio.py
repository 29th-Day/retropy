# libretro.h

from ctypes import *
from typing import Callable

# region 2053 - 2081

retro_midi_input_enabled_t = CFUNCTYPE(c_bool)
retro_midi_output_enabled_t = CFUNCTYPE(c_bool)
retro_midi_read_t = CFUNCTYPE(c_bool, POINTER(c_uint8))
retro_midi_write_t = CFUNCTYPE(c_bool, c_uint8, c_uint32)
retro_midi_flush_t = CFUNCTYPE(c_bool)


class MidiInterface(Structure):
    _fields_ = [
        ('input_enabled', retro_midi_input_enabled_t),
        ('output_enabled', retro_midi_output_enabled_t),
        ('read', retro_midi_read_t),
        ('write', retro_midi_write_t),
        ('flush', retro_midi_flush_t),
    ]

    interface_type: Callable[[None], c_bool]
    output_enabled: Callable[[None], c_bool]
    read: Callable[[POINTER(c_uint8)], c_bool]
    write: Callable[[c_uint8, c_uint32], c_bool]
    flush: Callable[[None], c_bool]

# endregion

# region 2710 - 2769

retro_audio_callback_t = CFUNCTYPE(None)
retro_audio_set_state_callback_t = CFUNCTYPE(None, c_bool)

class retro_audio_callback(Structure):
    _fields_ = [
        ('callback', retro_audio_callback_t),
        ('set_state', retro_audio_set_state_callback_t),
    ]

    callback: Callable[[None], None]
    set_state: Callable[[bool], None]
    
retro_frame_time_callback_t = CFUNCTYPE(None, c_int64)

class retro_frame_time_callback(Structure):
    _fields_ = [
        ('callback', retro_frame_time_callback_t),
        ('reference', c_int64),
    ]

    callback: Callable[[int], None]
    reference: int

retro_audio_buffer_status_callback_t = CFUNCTYPE(None, c_bool, c_uint, c_bool)

class retro_audio_buffer_status_callback(Structure):
    _fields_ = [
        ('callback', retro_audio_buffer_status_callback_t),
    ]

    callback: Callable[[bool, int, bool], None]

# endregion

# region 3991 - 4192

# MICROPHONE (NOT IMPLEMENTED)

# endregion
