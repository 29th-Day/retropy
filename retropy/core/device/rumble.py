from ctypes import *
from typing import Callable
from enum import IntFlag, Enum

class RumbleEffect(Enum):
    STRONG = 0
    WEAK = 1

set_rumble_state_t = CFUNCTYPE(c_bool, c_uint, c_int, c_uint16)
"""retro_set_rumble_state_t"""

class RumbleInterface(Structure):
    """retro_rumble_interface"""
    _fields_ = [
        ('set_rumble_state', set_rumble_state_t),
    ]

    set_rumble_state: Callable[[int, int, int], bool]
