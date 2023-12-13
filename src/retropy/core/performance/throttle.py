from ctypes import *
from enum import Enum


class ThrottleMode(Enum):
    """RETRO_THROTTLE_"""

    NONE = 0
    FRAME_STEPPING = 1
    FAST_FORWARD = 2
    SLOW_MOTION = 3
    REWINDING = 4
    VSYNC = 5
    UNBLOCKED = 6


class ThrottleState(Structure):
    """retro_throttle_state"""

    _fields_ = [
        ("mode", c_uint),
        ("rate", c_float),
    ]

    mode: int
    rate: float
