# libretro.h

from ctypes import *
from enum import IntEnum
from typing import List, Callable

# region 104 - 253

class RETRO_DEVICE(IntEnum):
    NONE = 0
    JOYPAD = 1
    MOUSE = 2
    KEYBOARD = 3
    LIGHTGUN = 4
    ANALOG = 5
    POINTER = 6


class JOYPAD(IntEnum):
    B = 0
    Y = 1
    SELECT = 2
    START = 3
    UP = 4
    DOWN = 5
    LEFT = 6
    RIGHT = 7
    A = 8
    X = 9
    L = 10
    R = 11
    L2 = 12
    R2 = 13
    L3 = 14
    R3 = 15
    MASK = 256


class ANALOG(IntEnum):
    LEFT = 0
    RIGHT = 1
    BUTTON = 2
    X = 0
    Y = 1


class MOUSE(IntEnum):
    X = 0
    Y = 1
    LEFT = 2
    RIGHT = 3
    WHEELUP = 4
    WHEELDOWN = 5
    MIDDLE = 6
    HORIZ_WHEELUP = 7
    HORIZ_WHEELDOWN = 8
    BUTTON_4 = 9
    BUTTON_5 = 10


class LIGHTGUN(IntEnum):
    SCREEN_X = 13
    SCREEN_Y = 14
    IS_OFFSCREEN = 15
    TRIGGER = 2
    RELOAD = 16
    AUX_A = 3
    AUX_B = 4
    START = 6
    SELECT = 7
    AUX_C = 8
    DPAD_UP = 9
    DPAD_DOWN = 10
    DPAD_LEFT = 11
    DPAD_RIGHT = 12


# class POINTER(IntEnum):
#     POINTER_X        = 0
#     POINTER_Y        = 1
#     POINTER_PRESSED  = 2
#     POINTER_COUNT    = 3

# endregion 


# region 2286 - 2303

class retro_controller_description(Structure):
    _fields_ = [
        ('desc', c_char_p),
        ('id', c_uint)
    ]

    desc: bytes
    id: int
    
class retro_controller_info(Structure):
    _fields_ = [
        ('types', POINTER(retro_controller_description)),
        ('num_types', c_uint)
    ]

    types: POINTER(retro_controller_description)
    num_types: int

# endregion


# region 2651 - 2683

retro_location_set_interval_t = CFUNCTYPE(None, c_uint, c_uint)
retro_location_start_t = CFUNCTYPE(c_bool)
retro_location_stop_t = CFUNCTYPE(None)
retro_location_get_position_t = CFUNCTYPE(c_bool, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double))
retro_location_lifetime_status_t = CFUNCTYPE(None)

class retro_location_callback(Structure):
    _fields_ = [
        ('start', retro_location_start_t),
        ('stop', retro_location_stop_t),
        ('get_position', retro_location_get_position_t),
        ('set_interval', retro_location_set_interval_t),
        ('initialized', retro_location_lifetime_status_t),
        ('deinitialized', retro_location_lifetime_status_t),
    ]

    start: Callable[[None], c_bool]
    stop: Callable[[None], None]
    get_position: Callable[[POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)], c_bool]
    set_interval: Callable[[c_uint, c_uint], None]
    initialized: Callable[[None], None]
    deinitialized: Callable[[None], None]

# endregion


# region 2929 - 2935

retro_keyboard_event_t = CFUNCTYPE(None, c_bool, c_uint, c_uint32, c_uint16)

class retro_keyboard_callback(Structure):
    _fields_ = [
        ('callback', retro_keyboard_event_t),
    ]

    callback: Callable[[c_bool, c_uint, c_uint32, c_uint16], None]

# endregion


# region 3346 - 3361

class retro_input_descriptor(Structure):
    _fields_ = [
        ('port', c_uint),
        ('device', c_uint),
        ('index', c_uint),
        ('id', c_uint),
        ('description', c_char_p),
    ]

    port: int
    device: int
    index: int
    id: int
    description: bytes

# endregion
