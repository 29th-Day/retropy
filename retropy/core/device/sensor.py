from ctypes import *
from enum import Enum
from typing import Callable


class SensorAction(Enum):
    """retro_sensor_action"""

    ACCELEROMETER_ENABLE = 0
    ACCELEROMETER_DISABLE = 1
    GYROSCOPE_ENABLE = 2
    GYROSCOPE_DISABLE = 3
    ILLUMINANCE_ENABLE = 4
    ILLUMINANCE_DISABLE = 5


class SensorTypes(Enum):
    """RETRO_SENSOR_"""

    ACCELEROMETER_X = 0
    ACCELEROMETER_Y = 1
    ACCELEROMETER_Z = 2
    GYROSCOPE_X = 3
    GYROSCOPE_Y = 4
    GYROSCOPE_Z = 5
    ILLUMINANCE = 6


set_sensor_state_t = CFUNCTYPE(c_bool, c_uint, c_int32, c_uint)
"""retro_set_sensor_state_t"""

sensor_get_input_t = CFUNCTYPE(c_float, c_uint, c_uint)
"""retro_sensor_get_input_t"""


class SensorInterface(Structure):
    """retro_sensor_interface"""

    _fields_ = [
        ("set_sensor_state", set_sensor_state_t),
        ("get_sensor_state", set_sensor_state_t),
    ]

    set_sensor_state: Callable[[int, int, int], bool]
    get_sensor_state: Callable[[int, int], float]
