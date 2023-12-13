from ctypes import *


class ControllerDescription(Structure):
    """retro_controller_description"""

    _fields_ = [("desc", c_char_p), ("id", c_uint)]

    desc: bytes
    id: int


class ControllerInfo(Structure):
    """retro_controller_info"""

    _fields_ = [("types", POINTER(ControllerDescription)), ("num_types", c_uint)]

    types: POINTER(ControllerDescription)
    num_types: int
