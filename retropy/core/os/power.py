from ctypes import *
from enum import Enum
from typing import Callable


class PowerState(Enum):
    """retro_power_state"""

    UNKOWN = 0
    DISCHARGING = 1
    CHARGING = 2
    CHARGED = 3
    PLUGGED_IN = 4


POWERSTATE_NO_ESTIMATE = -1


class DevicePower(Structure):
    """retro_device_power"""

    _fields_ = [
        ("state", c_int32),
        ("seconds", c_int32),
        ("precent", c_int8),
    ]

    state: int
    seconds: int
    percent: int
