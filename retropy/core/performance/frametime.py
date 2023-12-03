from ctypes import *
from typing import Callable

retro_frame_time_callback_t = CFUNCTYPE(None, c_int64)


class FrameTimeCallback(Structure):
    """retro_frame_time_callback"""

    _fields_ = [
        ("callback", retro_frame_time_callback_t),
        ("reference", c_int64),
    ]

    callback: Callable[[int], None]
    reference: int
