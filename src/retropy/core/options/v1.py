from ctypes import *

from . import VALUES_MAX, OptionValue


class OptionDefinition(Structure):
    """retro_core_option_definition"""

    _fields_ = [
        ("key", c_char_p),
        ("desc", c_char_p),
        ("info", c_char_p),
        ("values", OptionValue * VALUES_MAX),
        ("default_value", c_char_p),
    ]

    key: bytes
    desc: bytes
    info: bytes
    values: POINTER(OptionValue)
    default_value: bytes


class OptionIntl(Structure):
    """retro_core_options_intl"""

    _fields_ = [
        ("us", POINTER(OptionDefinition)),
        ("local", POINTER(OptionDefinition)),
    ]

    us: POINTER(OptionDefinition)
    local: POINTER(OptionDefinition)
