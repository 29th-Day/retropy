# libretro.h

from ctypes import *
from enum import IntEnum
from typing import Callable

# region 4194 - 4272

class POWER_STATE(IntEnum):
    UNKOWN = 0
    DISCHARGING = 1
    CHARGING = 2
    CHARGED = 3
    PLUGGED_IN = 4

POWERSTATE_NO_ESTIMATE = (-1)

class retro_device_power(Structure):
    _fields_ = [
        ('state', c_int32),
        ('seconds', c_int32),
        ('precent', c_int8),
    ]

    state: c_int32
    seconds: c_int32
    percent: c_int8

# endregion
