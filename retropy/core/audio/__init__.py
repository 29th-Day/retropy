from ctypes import *
from typing import Callable


audio_callback_t = CFUNCTYPE(None)
"""retro_audio_callback_t"""

audio_set_state_callback_t = CFUNCTYPE(None, c_bool)
"""retro_audio_set_state_callback_t"""

audio_buffer_status_callback_t = CFUNCTYPE(None, c_bool, c_uint, c_bool)
"""retro_audio_buffer_status_callback_t"""


class AudioCallback(Structure):
    """retro_audio_callback"""

    _fields_ = [
        ("callback", audio_callback_t),
        ("set_state", audio_set_state_callback_t),
    ]

    callback: Callable[[None], None]
    set_state: Callable[[bool], None]


class AudioBufferStatusCallback(Structure):
    """retro_audio_buffer_status_callback"""

    _fields_ = [
        ("callback", audio_buffer_status_callback_t),
    ]

    callback: Callable[[bool, int, bool], None]
