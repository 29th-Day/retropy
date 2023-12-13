from ctypes import *
from enum import Enum
from typing import Callable

location_set_interval_t = CFUNCTYPE(None, c_uint, c_uint)
"""retro_location_set_interval_t"""

location_start_t = CFUNCTYPE(c_bool)
"""retro_location_start_t"""

location_stop_t = CFUNCTYPE(None)
"""retro_location_stop_t"""

location_get_position_t = CFUNCTYPE(
    c_bool, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)
)
"""retro_location_get_position_t"""

location_lifetime_status_t = CFUNCTYPE(None)
"""retro_location_lifetime_status_t"""


class LocationCallback(Structure):
    """retro_location_callback"""

    _fields_ = [
        ("start", location_start_t),
        ("stop", location_stop_t),
        ("get_position", location_get_position_t),
        ("set_interval", location_set_interval_t),
        ("initialized", location_lifetime_status_t),
        ("deinitialized", location_lifetime_status_t),
    ]

    start: Callable[[None], bool]
    stop: Callable[[None], None]
    get_position: Callable[
        [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)],
        c_bool,
    ]
    set_interval: Callable[[int, int], None]
    initialized: Callable[[None], None]
    deinitialized: Callable[[None], None]
