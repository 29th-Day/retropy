from ctypes import *
from enum import Enum, IntEnum


class Device(IntEnum):
    """RETRO_DEVICE_"""

    NONE = 0
    JOYPAD = 1
    # MOUSE = 2
    # KEYBOARD = 3
    # LIGHTGUN = 4
    ANALOG = 5
    # POINTER = 6


class Joypad(IntEnum):
    """RETRO_DEVICE_ID_JOYPAD_"""

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
    # MASK = 256


"""
class Mouse(IntEnum):
    # RETRO_DEVICE_ID_

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
"""


class AnalogIdx(IntEnum):
    """RETRO_DEVICE_INDEX_ANALOG_"""

    LEFT_STICK = 0
    RIGHT_STICK = 1
    BUTTONS = 2


class Analog(IntEnum):
    """RETRO_DEVICE_ID_ANALOG_"""

    X = 0
    Y = 1


class InputDescriptor(Structure):
    """retro_input_descriptor"""

    _fields_ = [
        ("port", c_uint),
        ("device", c_uint),
        ("index", c_uint),
        ("id", c_uint),
        ("description", c_char_p),
    ]

    port: int
    device: int
    index: int
    id: int
    description: bytes
