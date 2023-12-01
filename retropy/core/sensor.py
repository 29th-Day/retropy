# libretro.h

from ctypes import *
from enum import IntEnum
from typing import Callable

# region 2525 - 2558

class Action(IntEnum):
    ACCELEROMETER_ENABLE = 0,
    ACCELEROMETER_DISABLE = 1,
    GYROSCOPE_ENABLE = 2,
    GYROSCOPE_DISABLE = 3,
    ILLUMINANCE_ENABLE = 4,
    ILLUMINANCE_DISABLE = 5,

ACCELEROMETER_X = 0
ACCELEROMETER_Y = 1
ACCELEROMETER_Z = 2
GYROSCOPE_X = 3
GYROSCOPE_Y = 4
GYROSCOPE_Z = 5
ILLUMINANCE = 6

retro_set_sensor_state_t = CFUNCTYPE(c_bool, c_uint, c_int32, c_uint)
retro_sensor_get_input_t = CFUNCTYPE(c_float, c_uint, c_uint)

class retro_sensor_interface(Structure):
    _fields_ = [
        ('set_sensor_state', retro_set_sensor_state_t),
        ('get_sensor_state', retro_set_sensor_state_t),
    ]

    set_sensor_state: Callable[[c_uint, c_int32, c_uint], c_bool]
    get_sensor_state: Callable[[c_uint, c_uint], c_float]

# endregion
